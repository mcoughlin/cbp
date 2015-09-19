#!/usr/bin/env python

import os, serial, sys, time, glob, struct, subprocess
import numpy as np
import optparse
from threading import Timer
import FLI

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doStatus", action="store_true",default=False)
    parser.add_option("--doLog", action="store_true",default=False)
    parser.add_option("-i","--instruments",\
        default="XY,Focuser,TipTilt,AltAz,FilterWheel,Photodiode")    
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
    posx = -1
    posy = -1
    posz = -1
    lvdt1 = -1
    lvdt2 = -1
    alt = -1
    az = -1
    mask = -1
    filter = -1
    photo = -1

    instruments = opts.instruments.split(",")
    for instrument in instruments:
        if instrument == "XY":
            sys_command = "python zaber.py --doGetPosition -d 1"
            output = run_cmd(sys_command)
            lines = output.split("\n")
            for line in lines:
                lineSplit = line.split(" ")
                if lineSplit[0] == "Position:":
                    posx = float(lineSplit[1])
            sys_command = "python zaber.py --doGetPosition -d 2"
            output = run_cmd(sys_command)
            lines = output.split("\n")
            for line in lines:
                lineSplit = line.split(" ")
                if lineSplit[0] == "Position:":
                    posy = float(lineSplit[1])

        elif instrument == "Focuser":
            sys_command = "python focuser.py --doGetPosition"
            output = run_cmd(sys_command)
            lines = output.split("\n")
            for line in lines:
                lineSplit = line.split(" ")
                if lineSplit[0] == "Position:":
                    posz = float(lineSplit[1])

        elif instrument == "TipTilt":
            sys_command = "python tiptilt.py --doGetPosition"
            output = run_cmd(sys_command)
            lines = output.split("\n")
            for line in lines:
                lineSplit = line.split(" ")
                if lineSplit[0] == "LVDT_1:":
                    lvdt1 = float(lineSplit[1])
                elif lineSplit[0] == "LVDT_2:":
                    lvdt2 = float(lineSplit[1])

        elif instrument == "AltAz":
            sys_command = "python telmount.py --doSSH --doGetPosition"
            output = run_cmd(sys_command)
            lines = output.split("\n")
            for line in lines:
                lineSplit = line.split(" ")
                if lineSplit[0] == "Altitude:":
                    alt = float(lineSplit[1])
                elif lineSplit[0] == "Azimuth:":
                    az = float(lineSplit[1])

        elif instrument == "FilterWheel":
            sys_command = "python filter_wheel.py --doGetPosition"
            output = run_cmd(sys_command)
            lines = output.split("\n")
            for line in lines:
                lineSplit = line.split(" ")
                if lineSplit[0] == "Mask:":
                    mask = int(lineSplit[1])
                elif lineSplit[0] == "Filter:":
                    filter = int(lineSplit[1])

        elif instrument == "Photodiode":
            sys_command = "python photodiode.py --doGetPhotodiode"
            output = run_cmd(sys_command)
            lines = output.split("\n")
            for line in lines:
                lineSplit = line.split(" ")
                if lineSplit[0] == "Photodiode:":
                    photo = int(lineSplit[1])

    if (posx == -1) or (posy == -1):
        print "Zaber stages not responding..."
    if (posz == -1):
        print "Focuser not responding..."
    if (alt == -1) or (az == -1):
        print "Telescope mount not responding..."
    if (lvdt1 == -1) or (lvdt2 == -1):
        print "TipTilt not responding..."
    if (mask == -1) or (filter == -1):
        print "Filter wheel not responding..."
    if (photo == -1):
        print "Photodiode not responding..."

    if opts.verbose:
        print "X: %.5f"%posx
        print "Y: %.5f"%posy
        print "Z: %.5f"%posz
        print "Altitude: %.5f"%alt
        print "Azimuth: %.5f"%az
        print "LVDT 1: %.5f"%lvdt1
        print "LVDT 2: %.5f"%lvdt2
        print "Mask: %d"%mask
        print "Filter: %d"%filter
        print "Photodiode: %d"%photo

    return posx, posy, posz, lvdt1, lvdt2, alt, az, mask, filter, photo 

# Parse command line
opts = parse_commandline()

logDir = '/home/pi/CBP/logs'
logNumber = len(glob.glob(os.path.join(logDir,'log_*')))
logFile = os.path.join(os.path.join(logDir,'log_%d.txt'%logNumber))
im = opts.imnum

if opts.doStatus:

    if opts.doLog:
        fid = open(logFile,'w')
        fid.write("IM X Y Z LVDT1 LVDT2 ALT AZ MASK FILTER PHOTO COMMENT\n")

    continueLoop = True
    while continueLoop:
        posx, posy, posz, lvdt1, lvdt2, alt, az, mask, filter, photo = get_status(opts)

        if opts.verbose: 
            print "X: %.5f"%posx
            print "Y: %.5f"%posy
            print "Z: %.5f"%posz
            print "Altitude: %.5f"%alt
            print "Azimuth: %.5f"%az
            print "LVDT 1: %.5f"%lvdt1
            print "LVDT 2: %.5f"%lvdt2
            print "Mask: %d"%mask
            print "Filter: %d"%filter
            print "Photodiode: %d"%photo
            print "\n\n"

        if opts.doLog:
            try: 
                comment = raw_input('Comment? ')
            except:
                comment = "None"

            fid.write('%d,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%d,%d,%.5f,%s\n'%(im, posx, posy, posz, lvdt1, lvdt2, alt, az, mask, filter, photo,comment))

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
