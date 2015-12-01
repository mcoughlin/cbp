#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import optparse
import pexpect
import numpy as np

import cbp.phidget

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-n","--steps",default=1000,type=int)
    parser.add_option("-a","--angle",default=2.0,type=float)
    parser.add_option("-c","--doCompile", action="store_true",default=False)
    parser.add_option("--doSteps", action="store_true",default=False)
    parser.add_option("--doAngle", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def send(device, command, data=0):
   # send a packet using the specified device number, command number, and data
   # The data argument is optional and defaults to zero
   packet = struct.pack('<BBl', device, command, data)
   ser.write(packet)

def receive():
   # return 6 bytes from the receive buffer
   # there must be 6 bytes to receive (no error checking)
   r = [0,0,0,0,0,0]
   for i in range (6):
       r[i] = ord(ser.read(1))
   return r

def takesteps(mag = 100, direction = 1):
    steps_command = "picocom -b 57600 --nolock /dev/ttyACM0"
    child = pexpect.spawn (steps_command)
    loop = True
    while loop:
        i = child.expect ([pexpect.TIMEOUT,'\n'], timeout = 2)
        #print child.before, child.after
        if i == 0: # Timeout
            argstring = 'args %d %d\r'%(mag,direction)
            print argstring
            child.sendline(argstring)
            loop = False
        if i == 1:
            continue
    child.close()

def main(runtype = "steps", val = 1000):
   
    if runtype == "compile":
        steps_command = "cd /home/mcoughlin/Code/arduino/altaz/; source ./compile.sh"
        os.system(steps_command)
 
    elif runtype == "steps":
    
        print "Moving in steps..."
        steps = abs(val)
        if val<0:
            direction = 1
        else:
            direction = -1 
        mag = steps

        takesteps(mag = mag, direction = direction)    

    elif runtype == "angle":
    
        print "Moving in angle..."
        target_angle = val
        nave = 10000
        x, y, z, angle = cbp.phidget.main(nave)
        current_angle = angle        
        diff_angle = target_angle - current_angle
        print diff_angle

        while np.abs(diff_angle) > 0.1:
            x, y, z, angle = cbp.phidget.main(nave)
            current_angle = angle
            diff_angle = target_angle - current_angle

            print current_angle
            if diff_angle < 0:
                direction = 1
            else:
                direction = -1

            if np.abs(diff_angle) > 10:
                mag = 1000
            elif np.abs(diff_angle) > 1:
                mag = 100
            else:
                mag = 50

            takesteps(mag = mag, direction = direction)
  
if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype = "compile")
    if opts.doSteps:
        main(runtype = "steps", val = opts.steps)
    if opts.doAngle:
        main(runtype = "angle", val = opts.angle)
   
