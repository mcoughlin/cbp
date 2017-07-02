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
import cbp.spectrograph

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doStatus", action="store_true",default=False)
    parser.add_option("--doLog", action="store_true",default=False)
    parser.add_option("-i","--instruments",\
        default="phidget,filter_wheel,potentiometer,photodiode,monochromator,birger,keithley,spectrograph")    
    parser.add_option("-f","--filename",default="/tmp/test.dat")
    parser.add_option("-n","--imnum",default=0,type=int)
    parser.add_option("-w","--wavelength",default=550,type=int)
    parser.add_option("-t","--analysisType",default="photons")
    parser.add_option("-p","--photons",default=100000,type=int)
    parser.add_option("-q","--charge",default=10**-6,type=float)
    parser.add_option("-d","--duration",default=60.0,type=float)
    parser.add_option("-e","--specduration",default=1000000.0,type=float)
    parser.add_option("-s","--shutter",default=1,type=int)
    parser.add_option("-c","--comment",default="comment")
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

    instruments = opts.instruments.split(",")
    for instrument in instruments:
        if instrument == "phidget":
            #try:
            #    nave = 10000
            #    #x, y, z, angle = cbp.phidget.main(nave)
            #    acc = angle
            #except:
            #    acc = -1
            acc = -1
        elif instrument == "potentiometer":
            #try:
            #    potentiometer_1, potentiometer_2 = cbp.potentiometer.main()
            #    alt = potentiometer_1
            #    az = potentiometer_2
            #except:
            #    alt = -1
            #    az = -1
            alt = -1
            az = -1
        elif instrument == "filter_wheel":
            try:
                mask, filter = cbp.filter_wheel.main(runtype = "getposition")
            except:
                mask = -1
                filter = -1
        #elif instrument == "photodiode":
        #    photo = cbp.photodiode.main(runtype = "photodiode")
        elif instrument == "monochromator":
            try:
                monowavelength, monofilter = cbp.monochromater.main(runtype = "getmono")
            except:
                monowavelength = -1
                monofilter = -1
        elif instrument == "birger":
            #try:
            #    focus, aperture = cbp.birger.main(runtype = "status")
            #except:
            #    focus = -1
            #    aperture = -1
            focus = -1
            aperture = -1
        elif instrument == "keithley":
            #try:
            #    times,photo1,totphotons = cbp.keithley.main(runtype = "keithley",doSingle=True)
            #except:
            #    times = [-1]
            #    photo1 = [-1]
            #    totphotons = [-1]
            times = -1
            photo1 = -1
            totphotons = -1

    if opts.verbose:
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
        if (photo1 == -1):
            print "Keithley not responding..."

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

    return acc, alt, az, monowavelength, monofilter, mask, filter, focus, aperture, photo1

# Parse command line
opts = parse_commandline()

im = opts.imnum

if opts.shutter == 1:
    doShutter = True
elif opts.shutter == 0:
    doShutter = False

times, photos, totphotons = cbp.keithley.main(runtype = "keithley",photons = opts.photons, charge = opts.charge, duration = opts.duration, wavelength = opts.wavelength, mode = 'char', analysisType = opts.analysisType, doSingle = True, doReset = True, doShutter = doShutter)



fid = open(opts.filename,'w')
fid.write("IM ACC ALT AZ MWAVE MFILT MASK FILTER FOCUS APERTURE COMMENT\n")
acc, alt, az, monowavelength, monofilter, mask, filter, focus, aperture, photo1 = get_status(opts)

fid.write('%d,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%s\n'%(im, acc, alt, az, monowavelength, monofilter, mask, filter, focus, aperture,opts.comment))
fid.write("#Time, Charge, nphotons\n") 
#print times,photos,totphotons
for elapsed_time, photo, totphoton in zip(times,photos,totphotons):
    #print elapsed_time,photo,totphoton
    fid.write("%.10f %.10e %.10e\n"%(elapsed_time,photo,totphoton)) 
fid.close()


