#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse

def parse_commandline():
    """ 
    Parse the options given on the command-line.
    """ 
    parser = optparse.OptionParser()

    parser.add_option("-p","--position",default=180,type=int)
    parser.add_option("--doPolarizer", action="store_true",default=False)
    parser.add_option("--doHomePolarizer", action="store_true",default=False)
    parser.add_option("--doGetPolarizer", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def run_polarizer(position):
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        timeout=1.0,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
    pastr = "1PA%d\r\n"%(position)
    to_send = bytes(pastr.encode())
    ser.write(to_send)

def get_polarizer():
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        timeout=1.0,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
    to_send = bytes("1TP?\r\n".encode())
    ser.write(to_send)
    out = ser.read(10)
    out = float(out.replace("1TP",""))

    return out

def home_polarizer():

    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        timeout=1.0,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )

    to_send = bytes("1OR\r\n".encode())
    ser.write(to_send)

def main(runtype = "polarizer", val = 1):

    if runtype == "polarizer":
        print "Running the polarizer ..."
        run_polarizer(val)
    elif runtype == "homepolarizer":
        print "Home the polarizer ..."
        home_polarizer()
    elif runtype == "getpolarizer":
        print "Getting the polarizer ..."
        pos = get_polarizer()
        print pos

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doHomePolarizer:
        main(runtype = "homepolarizer")
    if opts.doPolarizer:
        main(runtype = "polarizer", val = opts.position)
    if opts.doGetPolarizer:
        main(runtype = "getpolarizer")

