#!/usr/bin/env python

import serial, sys, time, glob, struct
import optparse
import numpy as np
import FLI
import logging


class FilterWheel:
    """
    This is the class for communicating with the Filter Wheel.
    """
    def __init__(self):
        self.status = None
        self.center_line_filter_wheel = self.initialize_connection()
        self.mask = None
        self.filter = None

    def initialize_connection(self):
        """

        :return: returns the connection to the Filter Wheel.
        """
        try:
            fws = FLI.filter_wheel.USBFilterWheel.find_devices()

            for fw in fws:
                if fw.model == "CenterLine Filter Wheel":
                    fw0 = fw
                    self.status = "Connected"
            return fw0
        except Exception as e:
            logging.exception(e)
            self.status = "not connected"

    def error_raised(self):
        """

        :return: either raises an exception if parameters out of bounds or returns false to continue the program
        """
        if self.mask > 4 or self.mask < 0:
            raise Exception("Mask position must be integer 0-4")
        elif self.filter > 4 or self.filter < 0:
            raise Exception("Filter position must be integer 0-4")
        return False

    def do_position(self, mask, filter):
        """

        :param mask: This is the value of the mask
        :param filter: This is the value of the filter.
        :return: sets the position of the Filter Wheel.
        """
        if self.status != "not connected":
            self.mask = mask
            self.filter = filter
            if not self.error_raised():
                position = 5 * self.mask + self.filter
                self.center_line_filter_wheel.set_filter_pos(position)
                pos = self.center_line_filter_wheel.get_filter_pos()
        else:
            pass

    def get_position(self):
        """

        :return: returns the current mask and filter values of the Filter Wheel.
        """
        if self.status != "not connected":
            pos = self.center_line_filter_wheel.get_filter_pos()

            self.mask = pos / 5
            self.filter = np.mod(pos, 5)

            print("Mask:{0} Filter:{1}".format(self.mask, self.filter))
            return self.mask, self.filter
        else:
            pass

    def check_status(self):
        """

        :return: changes the status of the Filter Wheel depending on location of device in kernel.
        """
        try:
            fws = FLI.filter_wheel.USBFilterWheel.find_devices()
            for fw in fws:
                if fw.model == "CenterLine Filter Wheel":
                    fw0 = fw
                    self.status = "Connected"
        except Exception as e:
            self.status = "not connected"


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-m","--mask",default=0,type=int)
    parser.add_option("-f","--filter",default=0,type=int)
    parser.add_option("--doPosition", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts


def main(runtype = "position", mask = 0, filter = 0):

    fws = FilterWheel()

    if runtype == "position":
        fws.do_position(mask, filter)

    elif runtype == "getposition":
        fws.get_position()

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doPosition:
        main(runtype="position", mask=opts.mask, filter=opts.filter)
    if opts.doGetPosition:
        main(runtype="getposition")
