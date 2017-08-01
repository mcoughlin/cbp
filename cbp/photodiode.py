#!/usr/bin/env python

"""
.. module:: photodiode
    :platform: unix
    :synopsis: This module is for communicating with the photodiode instrument.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

class Photodiode:
    """
    This is the class for the photodiode
    """
    def __init__(self):
        self.status = None
        self.serial = self.create_serial()

    def create_serial(self):
        """
        This method initializes the serial connection to the photodiode

        :return:
        """
        try:
            PORT = '/dev/ttyACM.PD'
            BAUD_RATE = 9600
            ser2 = serial.Serial(PORT, BAUD_RATE)
            self.status = "connected"
            return ser2
        except Exception as e:
            print(e)
            self.status = "not connected"

    def check_status(self):
        """
        This method checks the status of the photodiode

        :return:
        """
        try:
            self.receiving()
        except Exception as e:
            self.status = "not connected"

    def get_photodiode(self):
        """
        This method returns the reading of the photodiode

        :return:
        """
        if self.status != "not connected":
            conversion = 1.0

            success = 0
            numlines = 5
            linenum = 0
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
        else:
            pass

    def receiving(self):
        """
        This returns the last received message from the serial connection

        :return:
        """
        if self.status != "not connected":
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
        else:
            pass

    def compile(self):
        """
        This method compiles the photodiode arduino code

        :return:
        """
        if self.status != "not connected":
            steps_command = "cd /home/pi/Code/arduino/PD/; ./compile.sh"
            os.system(steps_command)
        else:
            pass

        # If the Arduino sends lots of empty lines, you'll lose the
        # last filled line, so you could make the above statement conditional
        # like so: if lines[-2]: last_received = lines[-2]
    def photodiode(self):
        """
        This method returns a photodiode reading converted.

        :return:
        """
        if self.status != "not connected":
            photo = self.get_photodiode()
            conv = (1.0 / 2.0) * (1.0 / 10.0)
            photo = photo * conv
            # print "Photodiode: %d"%photo
            return photo
        else:
            pass


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


def main(runtype = "compile", val = 0):
    photodiode = Photodiode()

    if runtype == "compile":
        photodiode.compile()
    elif runtype == "photodiode":
        photodiode.photodiode()

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype="compile")
    if opts.doPhotodiode:
        main(runtype="photodiode")

