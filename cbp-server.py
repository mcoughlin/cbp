#!/usr/bin/python
# Start with python cbp-server.py -H 134.158.155.9 -d


import datetime
import os
import daemon_servers
#import cbp.cbp_instrument
import cbp.keithley_update as Keithley
import cbp.spectrograph
import cbp.filter_wheel
import cbp.laser_update as Laser
import cbp.newportrotator 
from threading import Thread

def main(options, args):
    threads = [Thread(target=server.main, args=(options,args)) for server in servers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    now = datetime.datetime.now()
    logdir = os.path.join(os.getenv("HOME"), "logs")
    logname = os.path.join(logdir, 
                           'cbp-server-%s.log' % now.date().isoformat())
    logsymlink = os.path.join(logdir, "cbp-server.log")
    if os.path.islink(logsymlink):
        try:
            os.unlink(logsymlink)
            os.symlink(logname, logsymlink)
        except OSError:
            pass

    import optparse 
    parser = optparse.OptionParser(usage="%prog [-l log] [-d]")
    parser.add_option('-d', '--daemon', default=False, 
                      action='store_true', 
                      help='Run as a background daemon')
#    parser.add_option('--dummy', default=False, 
#                      action='store_true', 
#                      help='Run a fake instance instead')
    parser.add_option('-p', '--port', default=8011, 
                      action='store', type='int', 
                      help='Listen on port')
    parser.add_option('-H', '--hostname', default='localhost', 
                      action='store', 
                      help='server address')
    parser.add_option('-l', '--log-file', default=logname, 
                      action='store', 
                      help='specify a log file')
    (options, args) = parser.parse_args()
    
    SERVER_HOSTNAME = options.hostname
    SERVER_PORT = options.port
    
    name = 'cbp-server'
    daemon_servers.setup_logging(name, logfile=options.log_file)
         
    #cbp_inst = cbp.cbp_instrument.CBP(altaz=False, filter_wheel=True, keithley=True, flipper=True, spectrograph=True, laser=False)
    components = {'keithley': (Keithley.Keithley(resnum=4), 1),
                  'spectro': (cbp.spectrograph.Spectrograph(), 2),
                  'filterwheel': (cbp.filter_wheel.FilterWheel(), 4),
                  'laser': (Laser.LaserSerialInterface(port='/dev/ttyUSB0'), 3),
                  'ndfilter': (cbp.newportrotator.NSR1(port='/dev/ttyUSB1'), 5), 
    }
    servers = [daemon_servers.BasicServer((SERVER_HOSTNAME, SERVER_PORT+components[name][1]), name, components[name][0]) for name in components]
    
    if options.daemon:
        daemon_servers.daemonize(options, args, main)
    else:
        main(options, args)
