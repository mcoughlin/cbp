#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

class Photodiode:
    def __init__(self):
        self.serial = self.create_serial()

    def create_serial(self):
        PORT = '/dev/ttyACM.PD'
        BAUD_RATE = 9600
        ser2 = serial.Serial(PORT, BAUD_RATE)
        return ser2

    def get_photodiode(self):
        conversion = 1.0

        success = 0
        numlines = 5
        linenum = 0
        while success == 0:
            line = receiving(self.serial)
            if linenum < numlines:
                linenum = linenum + 1
                continue
            line = line.replace("\n", "").replace("\r", "")
            lineSplit = line.split(" ")
            lineSplit = filter(None, lineSplit)

            if not len(lineSplit) == 1:
                continue

            data_out_1 = float(lineSplit[0])
            data_out_1 = data_out_1 / conversion

            success = 1

        return data_out_1

    def receiving(self):
        ser = self.serial

        buffer_string = ''
        last_received = ''
        while last_received == "":
            buffer_string = buffer_string + ser.read(ser.inWaiting())
            if '\n' in buffer_string:
                lines = buffer_string.split('\n')  # Guaranteed to have at least 2 entries
                last_received = lines[-2]
                buffer_string = lines[-1]

        return last_received

    def compile(self):
        steps_command = "cd /home/pi/Code/arduino/PD/; ./compile.sh"
        os.system(steps_command)

        # If the Arduino sends lots of empty lines, you'll lose the
        # last filled line, so you could make the above statement conditional
        # like so: if lines[-2]: last_received = lines[-2]
    def photodiode(self):
        photo = self.get_photodiode()
        conv = (1.0 / 2.0) * (1.0 / 10.0)
        photo = photo * conv
        # print "Photodiode: %d"%photo
        return photo

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-c","--compile", action="store_true",default=False)
    parser.add_option("--doPhotodiode", action="store_true",default=False)
    parser.add_option("--doCompile", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts


def main(photodiode, runtype = "compile", val = 0):

    if runtype == "compile":
        photodiode.compile()
    elif runtype == "photodiode":
        photodiode.photodiode()

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype = "compile")
    if opts.doPhotodiode:
        main(runtype = "photodiode")

