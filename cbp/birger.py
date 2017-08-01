#!/usr/bin/env python

"""
.. module:: birger
    :platform: unix
    :synopsis: This is a module for controlling the birger instrument for cbp.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import optparse

import serial
import sys
import time
import logging


class Birger:
    """
    This is a class for communicating with the Birger instrument.
    """
    def __init__(self):
        self.status = None
        self.ser = self.open_serial()
        self.focus = None
        self.aperture = None

    def open_serial(self):
        """

        :return: returns the open serial port otherwise exits the program with a error code.
        """
        dev_usb = "/dev/ttyUSB.BIRGER"

        # open serial port
        # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
        # ser = serial.Serial(dev_usb)

        try:
            ser = serial.Serial(dev_usb, 115200, 8, 'N', 1, timeout=5)
            self.status = "connected"
            return ser
        except Exception as e:
            logging.exception(e)
            self.status = "not connected"

    def check_status(self):
        """
        This methods checks the status of the birger

        :return:
        """
        if self.status != "not connected":
            try:
                reply = self.send_and_receive('fp')
                if reply != "":
                    self.status = "connected"
                else:
                    self.status = "not connected"
            except Exception as e:
                logging.exception(e)
        else:
            pass

    def send_and_receive(self, command, dt=1):
        """

        :param command: The command to send.
        :param dt: The time to wait for the response.
        :return: returns the response of the device.
        """
        if self.status != "not connected":
            self.send(command)
            time.sleep(dt)  # wait for 1 second
            reply = self.receive()
            return reply
        else:
            pass

    def send(self, command):
        """
        Sends a command to the birger through the port

        :param command: This is the command to send to the birger
        :return:
        """
        if self.status != "not connected":
            self.ser.write("{0}\r\n".format(command))
        else:
            pass

    def receive(self):
        """
        receives a message from the birger port

        :return: returns the message from the port
        """
        if self.status != "not connected":
            out = ''
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1)
            return out
        else:
            pass

    def setup_lens(self):
        """
        Method that sets up the lenses

        :return:
        """
        if self.status != "not connected":
            # Setup Lens
            command = 'sm12'
            reply = self.send_and_receive(command)

            # Lens info
            command = 'lc'
            reply = self.send_and_receive(command)

            command = 'la'
            reply = self.send_and_receive(command)

            # Get Bootloader version
            command = 'bv'
            reply = self.send_and_receive(command)

            # Get aperture range
            command = 'da'
            reply = self.send_and_receive(command)

            # Get zoom range
            command = 'dz'
            reply = self.send_and_receive(command)
        else:
            pass

    def do_focus(self, val):
        """

        :param val: This is the value that the focus will be set to.
        :return: sets the focus of the birger.
        """
        if self.status != "not connected":
            self.setup_lens()
            if (val < 0) or (val > 16383):
                raise Exception("Focus should be integer between 0-16383")

            print(val)
            focus = val
            focusstr = ("%04x" % (focus)).replace("0x", "")

            checksum = 0x0000
            mask = 0x1000
            for i in xrange(4):
                checksum = checksum ^ (focus / mask)
                mask = mask >> 4
            checksum = checksum & 0x0F
            checksumstr = ("%x" % checksum).replace("0x", "")

            command = 'eh%s,%s' % (focusstr, checksumstr)
            reply = self.send_and_receive(command)
            self.focus = val
        else:
            pass

    def do_aperture(self, val):
        """

        :param val: This is the value of the aperture
        :return:
        """
        if self.status != "not connected":
            self.setup_lens()
            if (val < 0) or (val > 24):
                raise Exception("Focus should be integer between 0-24")

            command = 'in'
            reply = self.send_and_receive(command)

            command = 'ma%d' % (val)
            reply = self.send_and_receive(command)
            self.aperture = val
        else:
            pass

    def do_status(self):
        """

        :return: This returns the focus and aperture of the birger.
        """
        if self.status != "not connected":
            self.setup_lens()
            command = 'fp'
            reply = self.send_and_receive(command)

            reply = reply.replace("fp\rOK\r", "")
            reply_split = reply.split(" ")
            reply_split = filter(None, reply_split)

            fmin = float(reply_split[0].replace("fmin:", ""))
            fmax = float(reply_split[1].replace("fmax:", ""))
            focus = float(reply_split[2].replace("current:", "").replace("\r", ""))

            command = 'pa'
            reply = self.send_and_receive(command)

            try:
                reply_split = reply.split(",")
                reply_split = filter(None, reply_split)

                aperture = float(reply_split[0])
                fstop = float(reply_split[1].replace("f", ""))
            except Exception as e:
                logging.exception(e)
                aperture = 0

            return focus, aperture
        else:
            pass


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-f", "--focus", default=4096, type=int)
    parser.add_option("-a", "--aperture", default=0, type=int)
    parser.add_option("--doFocus", action="store_true", default=False)
    parser.add_option("--doAperture", action="store_true", default=False)
    parser.add_option("--doStatus", action="store_true", default=False)
    parser.add_option("-v", "--verbose", action="store_true", default=False)

    opts, args = parser.parse_args()

    return opts


def main(runtype="focus", val=1000):
    birger = Birger()
    if runtype == "focus":
        birger.do_focus(val)
    elif runtype == "aperture":
        birger.do_aperture(val)
    elif runtype == "status":
        return birger.do_status()


if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doFocus:
        main(runtype="focus", val=opts.focus)
    if opts.doAperture:
        main(runtype="aperture", val=opts.aperture)
    if opts.doStatus:
        focus, aperture = main(runtype="status")
