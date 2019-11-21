#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse

from odemis.driver.tlaptmf import MFF

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-p","--position",default=-1,type=int)
    parser.add_option("--doFlipper", action="store_true",default=False)
    parser.add_option("--doGetFlipper", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts


def run_flipper(position):

    sn = "37873245"
    mff = MFF("MFF101", "flipper", sn=sn)
    mff.MoveJog(position)
    time.sleep(.6)


def get_flipper():
    # FIXME pos always returns zero regardless of flipper position <>
    sn = "37873245"
    mff = MFF("MFF101","flipper",sn=sn)
    pos, status = mff.GetStatus()
    return pos, status


def main(runtype="flipper", val=1):

    if runtype == "flipper":
        #print "Running the flipper ..."
        run_flipper(val)
    elif runtype == "getflipper":
        print "Getting the flipper ..."
        pos, status = get_flipper()
        print "Position: %d"%pos
        print "Status: %d"%status

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doFlipper:
        main(runtype="flipper", val=opts.position)
    if opts.doGetFlipper:
        main(runtype = "getflipper")

