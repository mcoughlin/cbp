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

    parser.add_option("-d","--threshold",default=1000,type=float)
    parser.add_option("-c","--compile", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)

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

def get_potentiometer():

    PORT = '/dev/ttyACM.ADS'
    BAUD_RATE = 57600
    ser2 = serial.Serial(PORT, BAUD_RATE)
    conversion = 360.0/32767.0
    conversion = 1.0/32767.0

    success = 0
    numlines = 5
    linenum = 0
    while success == 0:
        line = receiving(ser2)

        if linenum < numlines:
            linenum = linenum + 1
            continue
        line = line.replace("\n","").replace("\r","")
        lineSplit = line.split(" ")
        lineSplit = filter(None,lineSplit)

        if not len(lineSplit) == 2:
            continue

        data_out_1 = float(lineSplit[0])
        data_out_2 = float(lineSplit[1])

        data_out_1 = data_out_1 * conversion
        data_out_2 = data_out_2 * conversion

        success = 1

    return data_out_1, data_out_2

def main(doCompile = 0):

    if doCompile:
        steps_command = "cd /home/pi/Code/arduino/potentiometer/; ./compile.sh"
        os.system(steps_command)

    potentiometer_1, potentiometer_2 = get_potentiometer()

    return potentiometer_1, potentiometer_2

if __name__ == "__main__":
    doCompile = 0
    potentiometer_1, potentiometer_2 = main(doCompile = doCompile)

    print potentiometer_1, potentiometer_2
