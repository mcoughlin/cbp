#!/usr/bin/env python

import os, serial, sys, time, glob, struct, subprocess
import numpy as np
import optparse
from threading import Timer
#import FLI

import cbp.phidget, cbp.altaz
import cbp.potentiometer, cbp.birger
import cbp.lamp, cbp.shutter

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doRun", action="store_true",default=False)

    parser.add_option("-i","--instrument",default="phidget")    
    parser.add_option("-n","--steps",default=1000,type=int)
    parser.add_option("-a","--angle",default=2.0,type=float)
    parser.add_option("-m","--motornum",default=1,type=int)
    parser.add_option("-f","--focus",default=4096,type=int)
    parser.add_option("-p","--aperture",default=0,type=int)
    parser.add_option("-l","--lamp",default=100,type=int)
    parser.add_option("-s","--shutter",default=-1,type=int)

    parser.add_option("-c","--doCompile", action="store_true",default=False)

    parser.add_option("--doShutter", action="store_true",default=False)
    parser.add_option("--doLamp", action="store_true",default=False)
    parser.add_option("--doFocus", action="store_true",default=False)
    parser.add_option("--doAperture", action="store_true",default=False)
    parser.add_option("--doGetFocus", action="store_true",default=False)
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
        x, y, z, angle = cbp.phidget.main(nave)
        print x,y,z,angle
    elif opts.instrument == "potentiometer":
        potentiometer_1, potentiometer_2 = cbp.potentiometer.main()
        print potentiometer_1, potentiometer_2
    elif opts.instrument == "altaz":
        if opts.doCompile:
            cbp.altaz.main(runtype = "compile")
        if opts.doSteps:
            cbp.altaz.main(runtype = "steps", val = opts.steps, motornum = opts.motornum)
        if opts.doAngle:
            cbp.altaz.main(runtype = "angle", val = opts.angle, motornum = opts.motornum)
    elif opts.instrument == "birger":
        if opts.doFocus:
            cbp.birger.main(runtype = "focus", val = opts.focus)
        if opts.doAperture:
            cbp.birger.main(runtype = "aperture", val = opts.aperture)
    elif opts.instrument == "lamp":
        if opts.doLamp:
            cbp.lamp.main(runtype = "lamp", val = opts.lamp)
    elif opts.instrument == "shutter":
        if opts.doShutter:
            cbp.shutter.main(runtype = "shutter", val = opts.shutter)
