#!/usr/bin/env python

import os, serial, sys, time, glob, struct, subprocess
import numpy as np
import optparse
from threading import Timer

import cbp.keithley, cbp.monochromater
import cbp.shutter

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()
    parser.add_option("-n","--imnum",default=3,type=int)
    parser.add_option("-d","--duration",default=1,type=int)
    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()
dataDir = '/home/pi/CBP/throughput/data'
dataDir = '/home/pi/CBP/throughput/data3'
dataDir = '/home/pi/CBP/throughput/data4'
dataDir = '/home/pi/CBP/throughput/data5'
dataDir = '/home/pi/CBP/throughput/data6'
dataDir = '/home/pi/CBP/throughput/data7'
dataDir = '/home/pi/CBP/throughput/data8'
dataDir = '/home/pi/CBP/throughput/data'
dataDir = '/home/pi/CBP/throughput/data4'
dataDir = '/home/pi/CBP/throughput/data6'
dataDir = '/home/pi/CBP/throughput/data7'
dataDir = '/home/pi/CBP/throughput/data8'
dataDir = '/home/pi/CBP/throughput/data9'
dataDir = '/home/pi/CBP/throughput/data18'

if not os.path.isdir(dataDir):
    os.mkdir(dataDir)

# set defaults
nvals = opts.imnum

doDark = True
doDark = False
if doDark:
    fid = open("%s/dark.txt"%(dataDir),'w')
    for ii in xrange(nvals):

        photo1,photo2 = cbp.keithley.main(runtype ="keithley", duration = opts.duration)
        print "Keithley 1: %.10e"%photo1
        print "Keithley 2: %.10e"%photo2

        fid.write('%.5e %.5e\n'%(photo1, photo2))
    fid.close()

#continueLoop = True

#while continueLoop:
#    focus = int(raw_input('Focus? '))

doThroughput = False
doThroughput = True
if doThroughput:

    wavelengths = np.arange(400,1005,5)
    #wavelengths = np.arange(400,1001,1)
    #wavelengths = np.arange(427,1001,1)
    #wavelengths = np.arange(740,1001,1)
    #wavelengths = np.arange(400,420,20)
    #wavelengths = np.arange(840,860,20)
    wavelengths = np.arange(790,1005,5)
    #wavelengths = np.arange(790,795,5)
    wavelengths = np.arange(340,500,5)
    wavelengths = np.arange(395,500,5)
    #wavelengths = np.arange(500,505,5)
    wavelengths = np.arange(300,1010,10)
    #wavelengths = np.arange(870,1010,10)
    #wavelengths = np.arange(560,570,10)

    for wavelength in wavelengths:
    
        cbp.monochromater.main(runtype ="monowavelength", val = wavelength)
        time.sleep(5)

        cbp.shutter.main(runtype ="shutter", val = 1)
        time.sleep(5)       
 
        fid = open("%s/%d_dark.txt"%(dataDir,wavelength),'w')
        for ii in xrange(nvals):

            photo1,photo2 = cbp.keithley.main(runtype ="keithley", duration = opts.duration)
            print "Keithley 1: %.10e"%photo1
            print "Keithley 2: %.10e"%photo2

            fid.write('%.5e %.5e\n'%(photo1, photo2))
        fid.close()        

        cbp.shutter.main(runtype ="shutter", val = -1)
        time.sleep(5)

        fid = open("%s/%d.txt"%(dataDir,wavelength),'w')
        for ii in xrange(nvals):
    
            photo1,photo2 = cbp.keithley.main(runtype ="keithley", duration = opts.duration)
            print "Keithley 1: %.10e"%photo1
            print "Keithley 2: %.10e"%photo2
    
            fid.write('%.5e %.5e\n'%(photo1, photo2))
        fid.close()
    
        #val = raw_input('Quit? y/n ')
        #if val == "y":
        #    continueLoop = False

doCombine = True
if doCombine:
    fid1 = open("%s/combine.dat"%(dataDir),'w')
    fid2 = open("%s/combine_dark.dat"%(dataDir),'w')

    files = sorted(glob.glob(os.path.join(dataDir,'*.txt')))
    for file in files:
        wavelength = file.replace(".txt","").split("/")[-1]
        wavelengthSplit = wavelength.split("_")

        data_out = np.loadtxt(file)
        if not data_out.size: continue

        try: 
            photo1 = data_out[:,0]
            photo2 = data_out[:,1]
        except:
            photo1 = data_out[0]
            photo2 = data_out[1]

        indexes = np.where(photo1 < 1e10)
        photo1 = photo1[indexes]
        indexes = np.where(photo2 < 1e10)
        photo2 = photo2[indexes]
        photo1 = photo1[1:]
        photo2 = photo2[1:]

        if len(wavelengthSplit) == 1:
            wavelength = float(wavelengthSplit[0])
            fid1.write('%.5f %.5e %.5e %.5e %.5e\n'%(wavelength,np.median(photo1),np.std(photo1), np.median(photo2),np.std(photo2)))
        elif len(wavelengthSplit) == 2:
            wavelength = float(wavelengthSplit[0])
            fid2.write('%.5f %.5e %.5e %.5e %.5e\n'%(wavelength,np.median(photo1),np.std(photo1), np.median(photo2),np.std(photo2)))

    fid1.close()
    fid2.close()

    
    
