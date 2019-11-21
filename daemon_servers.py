from __future__ import print_function
import os
import inspect 
import logging
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer, list_public_methods
import xmlrpclib
import datetime
import numpy as np

def convert(v):
    if np.isscalar(v):
        try:
            return v.item()
        except AttributeError:
            return v
    else:
        return [convert(_v) for _v in v]
    
def flatten(args):
    '''non intrusive trick to marshall numpy arrays and other stuff'''
    try:
        return tuple([convert(arg) for arg in args])
    except:
        return args


# daemonization related stuff
def redirect_stream(system_stream, target_stream):
    if target_stream is None:
        target_fd = os.open(os.devnull, os.O_RDWR)
    else:
        target_fd = target_stream.fileno()
    os.dup2(target_fd, system_stream.fileno())

def logged_call(f):
    def inner(*args, **keys):
        logging.debug('Call to ' + str(f))
        return flatten(f(*args, **keys))
    return inner

def setup_logging(name, logfile=None, level=logging.DEBUG):
    if logfile is None:
        now = datetime.datetime.now()
        logdir = os.path.join(os.getenv("HOME"), "logs")
        logname = os.path.join(logdir, 
                               '%s-server-%s.log' % (name, now.date().isoformat()))
        logsymlink = os.path.join(logdir, "%s-server.log" % name)
        if os.path.islink(logsymlink):
            try:
                os.unlink(logsymlink)
                os.symlink(logname, logsymlink)
            except OSError:
                pass
        logfile = logname
    logging.basicConfig(level=level)

def daemonize(options, args, main):
    '''Make the process a true daemon process through double forking'''
    try:
        pid = os.fork()
        if pid > 0:
            # first parent exits
            sys.exit(0)
    except OSError as e:
        print('fork #1 failed: %d (%s)' % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)
    os.setsid()
    
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent 
            print("starting server as daemin with PID %d" % pid)
            sys.exit(0)
    except OSError as e:
        print("fork #2 failed %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)
        
    main(options, args)

class BasicServer(SimpleXMLRPCServer):
    def __init__(self, addr, name, instance):
        self.name=name
        SimpleXMLRPCServer.__init__(self, addr)
        self.instance = instance
        self.instance.exit = self.exit
        self.allow_none = True
        
    def _listMethods(self):
        methods = list_public_methods(self.instance)
        return methods

#    def _methodHelp(self, method):
#        f = getattr(self.instance, method)
#        return inspect.getdoc(f)
#
    def serve_forever(self):
        self.quit = False
        while not self.quit:
            self.handle_request()
         
    def exit(self):
        self.quit = True
        return 'Server shutdown'

    def main(self, options, args):
        logging.basicConfig(filename=options.log_file, 
                            level=logging.DEBUG, 
                            format='%(asctime)s: ' + self.name +': %(message)s')
        if options.daemon:
            redirect_stream(sys.stdin, None)
            redirect_stream(sys.stdout, None)
            redirect_stream(sys.stderr, None)

#        self.register_function(self._listMethods, "__dir__")
#        self.register_function(self._listMethods, "system.listMethods")
#        self.register_function(self._listMethods, "trait_names")
#        self.register_function(self._listMethods, "_getAttributeNames")
#        self.register_function(self._methodHelp, "system.methodHelp")
        self.register_introspection_functions()
        self.register_function(self.exit, "exit")

        #the default behavior is not satisfactory in our case
        #self.register_instance(self.instance)
        logging.info(str(self.instance))
        for method in self._listMethods():
            f = getattr(self.instance, method)
            self.register_function(logged_call(f), method)
            logging.info('registering method '+method)
        
        logging.info("server is up and listening at http://%s:%d." % self.socket.getsockname())
        self.serve_forever()
        self.server_close()
