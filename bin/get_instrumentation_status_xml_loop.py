#!/usr/bin/env python

import os, sys, optparse, time
import cbp.cbp_instrument as CBP
import cbp
import cbp.shutter
import thorlabs

print "Initializing..."
laser_interface = cbp.laser.LaserSerialInterface(loop=False)

cbp_inst = CBP.CBP(phidget=False,birger=False,potentiometer=False,laser=False,filter_wheel=False,keithley=True,spectrograph=True,shutter=False,flipper=True)
cbp_inst.flipper.run_flipper(2)
cbp.shutter.main(runtype="shutter", val=-1)

print "Done initializing"

commandFile = "/tmp/command.dat"

print "Looping...."
while True:
    if os.path.isfile(commandFile): 
        print "Found file at %s..."%time.time()
        lines = [line.rstrip('\n') for line in open(commandFile)]
        if not len(lines) == 4: continue

        filename = lines[3]
        shutter = int(lines[2])
        duration = int(lines[1])
        wavelength = int(lines[0])
        print "Running %d %d %d %s"%(wavelength,duration,shutter,filename)

        if shutter == 1:
            doShutter = True
        elif shutter == 0:
            doShutter = False

        laser_interface.change_wavelength(wavelength)
        cbp_inst.write_status_log_xml(outfile=filename,duration=duration,doShutter=doShutter)
        os.system("rm %s"%commandFile)
        print "Finished..."
