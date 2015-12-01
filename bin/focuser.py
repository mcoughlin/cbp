#!/usr/bin/env python

import serial, sys, time, glob, struct, subprocess
import optparse
import FLI

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-p","--position",default=0,type=int)
    parser.add_option("--doHome", action="store_true",default=False)
    parser.add_option("--doPosition", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)
    parser.add_option("--doFilterMaskPosition", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()

fws = FLI.focuser.USBFocuser.find_devices()
if not len(fws) == 2:
    raise Exception("Focuser or Filter wheel not connected...")

for fw in fws:
    if fw.model == "Atlas Digital Focuser":
        fw0 = fw

if opts.doFilterMaskPosition:
    sys_command = "python filter_wheel.py --doGetPosition"
    p = subprocess.Popen(sys_command.split(" "),stdout=subprocess.PIPE)
    output = p.communicate()[0]
    lines = output.split("\n")
    for line in lines:
        lineSplit = line.split(" ")
        if lineSplit[0] == "Mask:":
            mask = int(lineSplit[1])
        elif lineSplit[0] == "Filter:":
            filter = int(lineSplit[1])

    maskfile = 'input/masks.txt'
    lines = [line.rstrip('\n') for line in open(maskfile)]
    for line in lines:
        lineSplit = line.split(',')
        num = int(lineSplit[0])
        if num == mask:
            focuser_mask = int(lineSplit[2])

    filterfile = 'input/filters.txt'
    lines = [line.rstrip('\n') for line in open(filterfile)]
    mask = []
    for line in lines:
        lineSplit = line.split(',')
        num = int(lineSplit[0])
        if num == filter:
            focuser_filter = int(lineSplit[2])

    position = focuser_mask + focuser_filter

    pos = fw0.get_stepper_position()
    print "Current Position: %d"%pos

    print "Position: %.3f"%pos
    print "Moving to position %.3f from %.3f..."%(position,pos)

    data = position - pos

    fw0.step_motor(data,blocking=False, force=True)
    pos = fw0.get_stepper_position()
    print "Position: %d"%pos

if opts.doGetPosition:
    pos = fw0.get_stepper_position()
    print "Position: %d"%pos

if opts.doHome:
    fw0.home_focuser()
    pos = fw0.get_stepper_position()
    print "Position: %d"%pos

if opts.doPosition:
    pos = fw0.get_stepper_position()
    print "Current Position: %d"%pos

    print "Position: %.3f"%pos
    print "Moving to position %.3f from %.3f..."%(opts.position,pos)

    data = opts.position - pos

    fw0.step_motor(data,blocking=False, force=True)
    pos = fw0.get_stepper_position()
    print "Position: %d"%pos



