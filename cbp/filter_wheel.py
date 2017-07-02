#!/usr/bin/env python

import serial, sys, time, glob, struct
import optparse
import numpy as np
import FLI

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

    fws = FLI.filter_wheel.USBFilterWheel.find_devices()
    #if not len(fws) == 2:
    #    raise Exception("Focuser or Filter wheel not connected...")

    for fw in fws:
        if fw.model == "CenterLine Filter Wheel":
            fw0 = fw

    if mask > 4 or mask < 0:
        raise Exception("Mask position must be integer 0-4")
    elif filter > 4 or filter < 0:
        raise Exception("Filter position must be integer 0-4")

    if runtype == "position":

        position = 5 * mask + filter
        fw0.set_filter_pos(position)
        pos = fw0.get_filter_pos()

        mask = pos/5
        filt = np.mod(pos,5)

        #print "Mask: %d"%mask
        #print "Filter: %d"%filt

    elif runtype == "getposition":

        pos = fw0.get_filter_pos()

        mask = pos/5
        filt = np.mod(pos,5)

        print mask, filt
        return mask, filt

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doPosition:
        main(runtype = "position", mask = opts.mask, filter = opts.filter)
    if opts.doGetPosition:
        main(runtype = "getposition")
