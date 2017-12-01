#!/usr/bin/env python

"""
.. module:: flipper
    :platform: unix
    :synopsis: This module is for communicating with the flipper instrument.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

from odemis.driver.tlaptmf import MFF

class Flipper:
    """
    This is the class for communicating with the flipper

    """
    def __init__(self):
        self.status = None
        self.flipper = self.create_connection()
        self.state = None

    def create_connection(self):
        """
        This method creates a connection by using a child process.

        :return:
        """
        try:
            sn = "37873245"
            child = MFF("MFF101", "flipper", sn=sn)
            self.status = "connected"
            return child
        except Exception as e:
            print(e)
            self.status = "not connected"

    def check_status(self):
        """
        This method checks the status of the flipper

        :return:
        """
        try:
            pos, status = self.flipper.GetStatus() 
        except Exception as e:
            print(e)
            self.status = "not connected"

    def close_connection(self):
        """
        This method closes the flipper

        :return:
        """
        if self.status != "not connected":
            self.flipper.close()

    def run_flipper(self, flipper):
        """
        This method is a duration run of the flipper, -1 can be used to keep flipper open indefinitely or 0 to close it.

        :param flipper: This is the length that the flipper will stay open in milliseconds.
        :return:
        """
        if self.status != "not connected":
            self.flipper.MoveJog(flipper)
        else:
            pass

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-p","--flipper",default=1,type=int)
    parser.add_option("-c","--doCompile", action="store_true",default=False)
    parser.add_option("--doFlipper", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts


def main(runtype = "compile", val = 0):
    flipper = Flipper()

    if runtype == "compile":
        flipper.do_compile()
    elif runtype == "flipper":
        #print "Running the flipper ..."
        flipper.run_flipper(val)

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype="compile")
    if opts.doFlipper:
        main(runtype="flipper", val = opts.flipper)

