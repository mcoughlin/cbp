#!/usr/bin/env python
"""
.. module:: altaz
    :platform: unix
    :synopsis: This is a module for controlling the vertical and horizontal axis of the device.
"""

import optparse
import os
import struct

import numpy as np
import pexpect

import cbp.phidget
import cbp.potentiometer


class Altaz:
    """
    This class is for controlling the motors of the device which move horizontally and vertically.
    """

    def __init__(self):
        self.status = None
        self.altangle = None
        self.azangle = None

    def send(self, device, command, data=0):
        """
        send a packet using the specified device number, command number, and data
        The data argument is optional and defaults to zero

        :param device:
        :param command:
        :param data:
        :return:
        """

        packet = struct.pack('<BBl', device, command, data)
        ser.write(packet)

    def receive(self):
        """
        return 6 bytes from the receive buffer
        there must be 6 bytes to receive (no error checking)

        :return:
        """

        r = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            r[i] = ord(ser.read(1))
        return r

    def takesteps(self, mag=100, direction=1, motornum=1):
        """

        :param mag:
        :param direction:
        :param motornum:
        :return:
        """
        steps_command = "picocom -b 57600 --nolock /dev/ttyACM.MSD"
        child = pexpect.spawn(steps_command)
        loop = True
        while loop:
            i = child.expect([pexpect.TIMEOUT, '\n'], timeout=2)
            # print child.before, child.after
            if i == 0:  # Timeout
                argstring = 'args %d %d %d\r' % (mag, direction, motornum)
                #print argstring
                child.sendline(argstring)
                loop = False
            if i == 1:
                continue
        child.close()

    def do_compile(self):
        """
        Compiles the device

        :return:
        """
        steps_command = "cd /home/mcoughlin/Code/arduino/stepper/; source ./compile.sh"
        os.system(steps_command)

    def do_steps(self, motornum, val):
        """

        :param motornum: the motor number to move the device.
        :param val:
        :return:
        """
        #print "Moving in steps..."
        steps = abs(val)
        if val < 0:
            direction = 1
        else:
            direction = 2
        mag = steps

        self.takesteps(mag=mag, direction=direction, motornum=motornum)

    def do_altangle(self):
        """

        :param val: The angle to move by.
        :param motornum: the motor to move by. 1 is left to right, 2 is up to down.
        :return:
        """
        nave = 10000
        x, y, z, angle = cbp.phidget.main(nave)
        current_angle = angle
        #print(current_angle)
        self.altangle = current_angle
        return current_angle

    def do_azangle(self):
        """

        :param val: The angle to move by
        :param motornum: The axis to move on by motor.
        :return:
        """
        angle_1, angle_2 = cbp.potentiometer.main()
        current_angle = angle_2
        #print(current_angle)
        self.azangle = current_angle
        return current_angle


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-m", "--motornum", default=1, type=int)
    parser.add_option("-n", "--steps", default=1000, type=int)
    parser.add_option("-a", "--angle", default=2.0, type=float)
    parser.add_option("-c", "--doCompile", action="store_true", default=False)
    parser.add_option("--doSteps", action="store_true", default=False)
    parser.add_option("--doAngle", action="store_true", default=False)

    opts, args = parser.parse_args()

    return opts


def main(runtype="steps", val=1000, motornum=1):
    altaz = Altaz()

    if runtype == "angle":
        if motornum == 1:
            runtype = "azangle"
        elif motornum == 2:
            runtype = "altangle"

    if runtype == "compile":
        altaz.do_compile()

    elif runtype == "steps":
        altaz.do_steps(motornum, val)

    elif runtype == "altangle":
        altaz.do_altangle()

    elif runtype == "azangle":
        altaz.do_azangle()


if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doCompile:
        main(runtype="compile")
    if opts.doSteps:
        main(runtype="steps", val=opts.steps, motornum=opts.motornum)
    if opts.doAngle:
        main(runtype="angle", val=opts.angle, motornum=opts.motornum)
