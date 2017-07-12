#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect


class Shutter:
    def __init__(self):
        self.status = None
        self.shutter = self.create_connection()

    def create_connection(self):
        try:
            shutter_command = "picocom -b 57600 /dev/ttyACM.SHUTTER"
            child = pexpect.spawn(shutter_command)
            self.status = "connected"
            return child
        except Exception as e:
            print(e)
            self.status = "not connected"

    def close_connection(self):
        self.shutter.close()

    def run_shutter(self, shutter):
        done = False
        while not done:
            i = self.shutter.expect([pexpect.TIMEOUT, '\n'], timeout=2)
            # print child.before, child.after
            if i == 0:  # Timeout
                argstring = 'args {0:d}\r'.format(shutter)
                # print argstring
                self.shutter.sendline(argstring)
                done = True
            if i == 1:
                continue

    def do_compile(self):
        steps_command = "cd /home/pi/Code/arduino/shutter/; ./compile.sh"
        os.system(steps_command)


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

