#!/usr/bin/env python

"""
.. module:: potentiometer
    :platform: unix
    :synopsis: This module is for communicating with the potentiometer instrument.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect


class Potentiometer:
    """
    This is a class for communicating with the potentiometer

    """
    def __init__(self):
        self.status = None
        self.serial = self.create_serial()

    def create_serial(self):
        """
        This method creates the serial connection to the potentiometer.

        :return:
        """
        try:
            PORT = '/dev/ttyACM.ADS'
            BAUD_RATE = 57600
            ser2 = serial.Serial(PORT, BAUD_RATE)
            self.status = "connected"
            return ser2
        except:
            self.status = "not connected"

    def check_status(self):
        """
        This method checks the status of the potentiometer

        :return:
        """
        try:
            self.receiving()
        except Exception as e:
            self.status = "not connected"

    def receiving(self):
        """
        This method returns the last received message from the potentiometer

        :return:
        """
        if self.status != "not connected":
            ser = self.serial
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
        else:
            pass

    def get_potentiometer(self):
        """
        This method returns the data from the potentiometer

        :return:
        """
        if self.status != "not connected":
            conversion = 360.0 / 32767.0

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

                if not len(lineSplit) == 2:
                    continue

                data_out_1 = float(lineSplit[0])
                data_out_2 = float(lineSplit[1])

                data_out_1 = 90.0 - (data_out_1 * conversion)
                data_out_2 = data_out_2 * conversion

                success = 1

            return data_out_1, data_out_2
        else:
            pass

    def do_compile(self):
        """
        This method compiles the arduino code of the potentiometer

        :return:
        """
        if self.status != "not connected":
            steps_command = "cd /home/pi/Code/arduino/potentiometer/; ./compile.sh"
            os.system(steps_command)
        else:
            pass


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


def main(doCompile=0):
    potentiometer = Potentiometer()

    if doCompile:
        potentiometer.do_compile()

    potentiometer_1, potentiometer_2 = potentiometer.get_potentiometer()

    return potentiometer_1, potentiometer_2

if __name__ == "__main__":
    doCompile = 0
    potentiometer_1, potentiometer_2 = main(doCompile=doCompile)

    print potentiometer_1, potentiometer_2
