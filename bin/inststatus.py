#!/usr/bin/env python

import os, serial, sys, time, glob, struct, subprocess
import numpy as np
import optparse
from threading import Timer
import FLI

import cbp.phidget, cbp.altaz
import cbp.potentiometer, cbp.birger
import cbp.lamp, cbp.shutter
import cbp.photodiode, cbp.filter_wheel
import cbp.monochromater, cbp.keithley

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doStatus", action="store_true",default=False)
    parser.add_option("--doLog", action="store_true",default=False)
    parser.add_option("-i","--instruments",\
        default="phidget,filter_wheel,potentiometer,photodiode,monochromator,birger,keithley")    
    parser.add_option("-n","--imnum",default=0,type=int)
    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def run_cmd(cmd, timeout_sec = 20):
    proc = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        stdout,stderr = proc.communicate()
    finally:
        timer.cancel()
    return stdout

def get_status(opts):

    # set defaults
    acc = -1
    alt = -1
    az = -1
    mask = -1
    filter = -1
    photo = -1
    monofilter = -1
    monowavelength = -1
    focus = -1
    aperture = -1
    photo1 = -1
    photo2 = -1

    instruments = opts.instruments.split(",")
    for instrument in instruments:
        if instrument == "phidget":
            nave = 10000
            x, y, z, angle = cbp.phidget.main(nave)
            acc = angle
        elif instrument == "potentiometer":
            potentiometer_1, potentiometer_2 = cbp.potentiometer.main()
            alt = potentiometer_1
            az = potentiometer_2
        elif instrument == "filter_wheel":
            mask, filter = cbp.filter_wheel.main(runtype = "getposition")
        #elif instrument == "photodiode":
        #    photo = cbp.photodiode.main(runtype = "photodiode")
        elif instrument == "monochromator":
            monowavelength, monofilter = cbp.monochromater.main(runtype = "getmono")
            print monowavelength, monofilter 
        elif instrument == "birger":
            focus, aperture = cbp.birger.main(runtype = "status")
        elif instrument == "keithley":
            photo1,photo2 = cbp.keithley.main(runtype = "keithley", doSingle = True, doReset = True)

    if (alt == -1) or (az == -1):
        print "Potentiometers not responding..."
    if (acc == -1):
        print "Phidget not responding..."
    if (monowavelength == -1) or (monofilter == -1):
        print "Monochrometer not responding..."
    if (mask == -1) or (filter == -1):
        print "Filter wheel not responding..."
    if (focus == -1) or (aperture == -1):
        print "Filter wheel not responding..."
    if (photo1 == -1) or (photo2 == -1):
        print "Keithley not responding..."

    if opts.verbose:
        print "Accelerometer: %.5f"%acc
        print "Altitude: %.5f"%alt
        print "Azimuth: %.5f"%az
        print "Monochromator Wavelength: %.5f"%monowavelength
        print "Monochromator Filter: %.5f"%monofilter
        print "Mask: %d"%mask
        print "Filter: %d"%filter
        print "Focus: %.5f"%focus
        print "Aperture: %.5f"%aperture
        print "Keithley 1: %.10e"%photo1
        print "Keithley 2: %.10e"%photo2

    return acc, alt, az, monowavelength, monofilter, mask, filter, focus, aperture, photo1, photo2

# Parse command line
opts = parse_commandline()

logDir = '/home/pi/CBP/logs'
logNumber = len(glob.glob(os.path.join(logDir,'log_*')))
logFile = os.path.join(os.path.join(logDir,'log_%d.txt'%logNumber))
im = opts.imnum

if opts.doStatus:

    if opts.doLog:
        fid = open(logFile,'w')
        fid.write("IM ACC ALT AZ MWAVE MFILT MASK FILTER FOCUS APERTURE KEITHLEY1 KEITHLEY2 COMMENT\n")

    continueLoop = True
    while continueLoop:
        acc, alt, az, monowavelength, monofilter, mask, filter, focus, aperture, photo1, photo2 = get_status(opts)

        if opts.doLog:
            try: 
                comment = raw_input('Comment? ')
            except:
                comment = "None"

            fid.write('%d,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5e,%.5e,%s\n'%(im, acc, alt, az, monowavelength, monofilter, mask, filter, focus, aperture, photo1, photo2, comment))

        val = raw_input('Quit? y/n ')
        if val == "y":
            continueLoop = False
        else:
            try:
                im = int(raw_input('New image number? '))
            except:
                im = im + 1

    if opts.doLog:
        fid.close()
