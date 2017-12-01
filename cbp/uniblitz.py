#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse

def parse_commandline():
    """ 
    Parse the options given on the command-line.
    """ 
    parser = optparse.OptionParser()

    parser.add_option("-p","--position",default=-1,type=int)
    parser.add_option("--doShutter", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def run_shutter(position):

    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
    print ser.portstr       # check which port was really used
    if position == 1:
        # Open
        to_send = bytes("@\r\n".encode())
        ser.write(to_send)
    elif position == 2:
        # Close
        to_send = bytes("A\r\n".encode())
        ser.write(to_send)
    else:
       print("I do not know what position you want!")
    ser.close()             # close port

def main(runtype = "shutter", val = 1):

    if runtype == "shutter":
        print "Running the shutter ..."
        run_shutter(val)

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doShutter:
        main(runtype = "shutter", val = opts.position)

