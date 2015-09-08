#!/usr/bin/env python

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-m","--motorNum",default=1,type=int)
    parser.add_option("-n","--numSteps",default=0,type=int)
    parser.add_option("-p","--phi",default=0.0,type=float)
    parser.add_option("-t","--theta",default=0.0,type=float)
    parser.add_option("-c","--compile", action="store_true",default=False)
    parser.add_option("--doSteps", action="store_true",default=False)
    parser.add_option("--doAngle", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

def run_stepper(steps,motorNum):
    shutter_command = "picocom -b 57600 /dev/ttyACM0"
    child = pexpect.spawn (shutter_command)
    loop = True
    while loop:
        i = child.expect ([pexpect.TIMEOUT,'\n'], timeout = 2)
        #print child.before, child.after
        if i == 0: # Timeout
            numsteps = np.absolute(steps)
            if steps >= 0:
                dir = 1
            else:
                dir = 2
            argstring = 'args %d %d %d\r'%(numsteps,dir,motorNum)
            print argstring
            child.sendline(argstring)
            loop = False
        if i == 1:
            continue
    child.close()

def receiving(ser):

    buffer_string = ''
    last_received = ''
    while last_received == "":
        buffer_string = buffer_string + ser.read(ser.inWaiting())
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer_string = lines[-1]

    return last_received

def get_LVDT():

    PORT = '/dev/ttyACM1'
    BAUD_RATE = 9600
    ser2 = serial.Serial(PORT, BAUD_RATE)
    conversion = 16777215.0 / 2.048

    success = 0
    while success == 0:
        line = receiving(ser2)
        line = line.replace("\n","").replace("\r","")
        lineSplit = line.split(" ")
        lineSplit = filter(None,lineSplit)

        if not len(lineSplit) == 2:
            continue

        data_out_1 = float(lineSplit[0])
        data_out_2 = float(lineSplit[1])

        data_out_1 = data_out_1 / conversion
        data_out_2 = data_out_2 / conversion

        success = 1

    return data_out_1, data_out_2

# Parse command line
opts = parse_commandline()

if opts.compile:
    steps_command = "cd /home/pi/Arduino/stepper/; ./compile.sh"
    os.system(steps_command)

    steps_command = "cd /home/pi/Arduino/ISE/; ./compile.sh"
    os.system(steps_command)

if opts.doSteps:
    print "Running the stepper motor ..."
    run_stepper(opts.numSteps,opts.motorNum)

if opts.doAngle:
    print "Running the stepper motor ..."
    z = 3.412*np.tan(opts.theta*2*np.pi/360.0)
    y = 3*np.tan(opts.phi*2*np.pi/360.0)    

    # convert to motor
    z = z*1000.0 
    y = y*1000.0

    print z, y

    m1 = int(z/2.0) + int(y/2.0)
    m2 = int(z/2.0) - int(y/2.0)

    print m1
    print m2

    run_stepper(m1,1)
    run_stepper(m2,1)

if opts.doGetPosition:
    stepper_1, stepper_2 = get_LVDT()
    print "LVDT_1: %.5f"%stepper_1
    print "LVDT_2: %.5f"%stepper_2
