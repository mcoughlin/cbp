#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-s","--shutter",default=-1,type=int)
    parser.add_option("-c","--compile", action="store_true",default=False)
    parser.add_option("--doShutter", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def run_shutter(shutter):
    shutter_command = "picocom -b 57600 /dev/ttyACM.SHUTTER"
    child = pexpect.spawn (shutter_command)
    loop = True
    while loop:
        i = child.expect ([pexpect.TIMEOUT,'\n'], timeout = 2)
        #print child.before, child.after
        if i == 0: # Timeout
            argstring = 'args %d\r'%(shutter)
            print argstring
            child.sendline(argstring)
            loop = False
        if i == 1:
            continue
    child.close()

# Parse command line
opts = parse_commandline()

if opts.compile:
    steps_command = "cd /home/pi/Arduino/shutter/; ./compile.sh"
    os.system(steps_command)

if opts.doShutter:
    print "Running the shutter ..."
    run_shutter(opts.shutter)


