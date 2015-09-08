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

    parser.add_option("-c","--compile", action="store_true",default=False)
    parser.add_option("--doGetPhotodiode", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def receiving(ser):

    buffer_string = ''
    last_received = ''
    while last_received == "":
        buffer_string = buffer_string + ser.read(ser.inWaiting())
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer_string = lines[-1]

    return last_received

def get_photodiode():

    PORT = '/dev/ttyACM2'
    BAUD_RATE = 9600
    ser2 = serial.Serial(PORT, BAUD_RATE)
    conversion = 1.0

    success = 0
    while success == 0:
        line = receiving(ser2)
        line = line.replace("\n","").replace("\r","")
        lineSplit = line.split(" ")
        lineSplit = filter(None,lineSplit)

        if not len(lineSplit) == 1:
            continue

        data_out_1 = float(lineSplit[0])
        data_out_1 = data_out_1 / conversion

        success = 1

    return data_out_1

# Parse command line
opts = parse_commandline()

if opts.compile:
    steps_command = "cd /home/pi/Arduino/photodiode/; ./compile.sh"
    os.system(steps_command)

if opts.doGetPhotodiode:
    photo = get_photodiode()
    print "Photodiode: %d"%photo
