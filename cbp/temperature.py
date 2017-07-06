#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

class Temperature:
    def __init__(self):
        self.serial = self.create_serial()
        self.status = None

    def create_serial(self):
        PORT = '/dev/ttyACM.TEMP'
        BAUD_RATE = 9600
        ser2 = serial.Serial(PORT, BAUD_RATE)
        self.status = "connected"
        return ser2

    def receiving(self):
        ser = self.serial
        buffer_string = ''
        last_received = ''
        while last_received == "":
            buffer_string = buffer_string + ser.read(ser.inWaiting())
            if '\n' in buffer_string:
                lines = buffer_string.split('\n')  # Guaranteed to have at least 2 entries
                last_received = lines[-2]
                # If the Arduino sends lots of empty lines, you'll lose the
                # last filled line, so you could make the above statement conditional
                # like so: if lines[-2]: last_received = lines[-2]
                buffer_string = lines[-1]

        return last_received

    def get_temperature(self):
        ser2 = self.serial
        conversion = 1.0

        success = 0
        numlines = 5
        linenum = 0
        data_out_1 = None
        while success == 0:
            line = self.receiving()
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

    def do_compile(self):
        steps_command = "cd /home/pi/Code/arduino/Temperature/; ./compile.sh"
        os.system(steps_command)

    def do_photodiode(self):
        temp = self.get_temperature()
        conv = (0.5 / 10.0)  # 0.5 mv/1 bit * 1 degree C / 10 mV
        temp = temp * conv
        print "Temperature: %.2f" % temp
        return temp

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-c","--compile", action="store_true",default=False)
    parser.add_option("--doTemperature", action="store_true",default=False)
    parser.add_option("--doCompile", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def main(temperature, runtype = "compile", val = 0):

    if runtype == "compile":
        temperature.do_compile()
    elif runtype == "photodiode":
        temperature.do_photodiode()

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype = "compile")
    if opts.doTemperature:
        main(runtype = "photodiode")
