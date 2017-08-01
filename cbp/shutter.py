#!/usr/bin/env python

"""
.. module:: shutter
    :platform: unix
    :synopsis: This module is for communicating with the shutter instrument.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect


class Shutter:
    """
    This is the class for communicating with the shutter

    """
    def __init__(self):
        self.status = None
        self.shutter = self.create_connection()
        self.state = None

    def create_connection(self):
        """
        This method creates a connection by using a child process.

        :return:
        """
        try:
            shutter_command = "picocom -b 57600 /dev/ttyACM.SHUTTER2"
            child = pexpect.spawn(shutter_command)
            self.status = "connected"
            return child
        except Exception as e:
            print(e)
            self.status = "not connected"

    def check_status(self):
        """
        This method checks the status of the shutter

        :return:
        """
        try:
            shutter_command = "picocom -b 57600 /dev/ttyACM.SHUTTER2"
            child = pexpect.spawn(shutter_command)
        except Exception as e:
            print(e)
            self.status = "not connected"

    def close_connection(self):
        """
        This method closes the shutter

        :return:
        """
        if self.status != "not connected":
            self.shutter.close()

    def run_shutter(self, shutter):
        """
        This method is a duration run of the shutter, -1 can be used to keep shutter open indefinitely or 0 to close it.

        :param shutter: This is the length that the shutter will stay open in milliseconds.
        :return:
        """
        if self.status != "not connected":
            done = False
            while not done:
                i = self.shutter.expect([pexpect.TIMEOUT, '\n'], timeout=2)
                # print child.before, child.after
                if i == 0:  # Timeout
                    argstring = 'args {0:d}\r'.format(shutter)
                    # print(argstring)
                    self.shutter.sendline(argstring)
                    done = True
                if i == 1:
                    continue
        else:
            pass

    def do_compile(self):
        """
        This method compiles the shutter arduino code.

        :return:
        """
        if self.status != "not connected":
            steps_command = "cd /home/pi/Code/arduino/shutter/; ./compile.sh"
            os.system(steps_command)
        else:
            pass


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-s","--shutter",default=-1,type=int)
    parser.add_option("-c","--doCompile", action="store_true",default=False)
    parser.add_option("--doShutter", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts


def main(runtype = "compile", val = 0):
    shutter = Shutter()

    if runtype == "compile":
        shutter.do_compile()
    elif runtype == "shutter":
        #print "Running the shutter ..."
        shutter.run_shutter(val)

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype="compile")
    if opts.doShutter:
        main(runtype="shutter", val = opts.shutter)

