#!/usr/bin/env python

import serial, sys, time, glob, struct
import optparse


class Birger:
    def __init__(self):
        self.ser = self.open_serial()
        self.status = None

    def open_serial(self):
        devUSB = "/dev/ttyUSB.BIRGER"

        # open serial port
        # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
        ser = serial.Serial(devUSB)

        try:
            ser = serial.Serial(devUSB, 115200, 8, 'N', 1, timeout=5)
            return ser
        except:
            print("Error opening com port. Quitting.")
            sys.exit(0)

    def send_and_receive(self, command, dt = 1):
        self.send(command)
        time.sleep(dt)  # wait for 1 second
        reply = self.receive()
        return reply

    def send(self, command):
        self.ser.write("{0}\r\n".format(command))

    def receive(self):
        out = ''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)
        return out

    def setup_lens(self):
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

    def do_focus(self, val):
        self.setup_lens()
        if (val < 0) or (val > 16383):
            raise Exception("Focus should be integer between 0-16383")

        print(val)
        focus = val
        focusstr = ("%04x"%(focus)).replace("0x","")

        checksum = 0x0000
        mask = 0x1000
        for i in xrange(4):
            checksum = checksum ^ (focus/mask)
            mask = mask >> 4
        checksum = checksum & 0x0F
        checksumstr = ("%x"%checksum).replace("0x","")

        command = 'eh%s,%s'%(focusstr,checksumstr)
        reply = self.send_and_receive(command)

    def do_aperture(self, val):
        self.setup_lens()
        if (val < 0) or (val > 24):
            raise Exception("Focus should be integer between 0-24")

        command = 'in'
        reply = self.send_and_receive(command)

        command = 'ma%d'%(val)
        reply = self.send_and_receive(command)

    def do_status(self):
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
        except:
            aperture = 0

        return focus, aperture


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-f","--focus",default=4096,type=int)
    parser.add_option("-a","--aperture",default=0,type=int)
    parser.add_option("--doFocus", action="store_true",default=False)
    parser.add_option("--doAperture", action="store_true",default=False)
    parser.add_option("--doStatus", action="store_true",default=False)
    parser.add_option("-v","--verbose", action="store_true",default=False)

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
