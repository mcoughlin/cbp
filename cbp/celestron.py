#!/usr/bin/env python

"""
.. module:: nexstar
    :platform: unix
    :synopsis: module for communicating with the filter wheel instrument of cbp

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import serial, sys, time, glob, struct
import optparse
import numpy as np
import os
if 'TESTENVIRONMENT' in os.environ:
    import mock
    sys.modules['point'] = mock.Mock()
else:
    from point import NexStar
import logging


class Telescope:
    """
    This is the class for communicating with the Filter Wheel.
    """
    def __init__(self, device='/dev/ttyUSB0'):
        self.status = None
        self.celestron_nexstar = self.initialize_connection()
        self.alt = None
        self.az = None

    def initialize_connection(self):
        """

        :return: returns the connection to the Filter Wheel.
        """
        try:
            ns = NexStar(self.device)
            self.status = "Connected"
            return ns
        except Exception as e:
            logging.exception(e)
            self.status = "not connected"

    def error_raised(self):
        """

        :return: either raises an exception if parameters out of bounds or returns false to continue the program
        """
        if self.alt > 90 or self.alt < -90:
            raise Exception("Altitude outside of limits...")
        elif self.az > 0 or self.az < 360:
            raise Exception("Azimuth outside of limits..")
        return False

    def do_position(self, alt, az):
        """

        :param alt: This is the value of the altitude.
        :param az: This is the value of the azimuth.
        :return: sets the position of the telecope.
        """
        if self.status != "not connected":
            self.az = alt
            self.alt = az
            if not self.error_raised():
                self.celestron_nexstar.goto_azalt(az, alt)
                while self.celestron_nexstar.goto_in_progress():
                    continue
                pos = self.get_position()
        else:
            pass

    def get_position(self):
        """

        :return: returns the current mask and filter values of the Filter Wheel.
        """
        if self.status != "not connected":
            altaz = self.celestron_nexstar.get_azalt()

            self.az = altaz[0]
            self.alt = altaz[1]

            print("Altitude:{0} Azimuth:{1}".format(self.alt, self.az))
            return self.alt, self.az
        else:
            pass

    def check_status(self):
        """

        :return: changes the status of the Filter Wheel depending on location of device in kernel.
        """
        try:
            ns = NexStar(self.device)
            self.status = "Connected"
        except Exception as e:
            self.status = "not connected"


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-a","--alt",default=0,type=int)
    parser.add_option("-z","--azimuth",default=0,type=int)
    parser.add_option("--doPosition", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts


def main(runtype = "position", alt = 0, az = 0):

    ns = FilterWheel()

    if runtype == "position":
        ns.do_position(alt, az)

    elif runtype == "getposition":
        ns.get_position()

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doPosition:
        main(runtype="position", alt=opts.alt, az=opts.az)
    if opts.doGetPosition:
        main(runtype="getposition")
