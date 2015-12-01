#!/usr/bin/env python

import os, serial, sys, time, glob, struct, subprocess
import numpy as np
import optparse
from threading import Timer
#import FLI

import phidget
import altaz

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doRun", action="store_true",default=False)
    parser.add_option("-i","--instrument",default="phidget")    
    parser.add_option("-n","--steps",default=1000,type=int)
    parser.add_option("-a","--angle",default=2.0,type=float)
    parser.add_option("-c","--doCompile", action="store_true",default=False)
    parser.add_option("--doSteps", action="store_true",default=False)
    parser.add_option("--doAngle", action="store_true",default=False)
    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()

if opts.doRun:

    if opts.instrument == "phidget":
        nave = 10000
        x, y, z, angle = phidget.main(nave)
        print x,y,z,angle
    elif opts.instrument == "altaz":
        if opts.doCompile:
            altaz.main(runtype = "compile")
        if opts.doSteps:
            altaz.main(runtype = "steps", val = opts.steps)
        if opts.doAngle:
            altaz.main(runtype = "angle", val = opts.angle)

