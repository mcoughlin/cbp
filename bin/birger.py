#!/usr/bin/env python

import optparse

import serial
import sys
import time


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-f", "--focus", default=4096, type=int)
    parser.add_option("-a", "--aperture", default=0, type=int)
    parser.add_option("--doFocus", action="store_true", default=False)
    parser.add_option("--doAperture", action="store_true", default=False)
    parser.add_option("--doGetFocus", action="store_true", default=False)
    parser.add_option("-v", "--verbose", action="store_true", default=False)

    opts, args = parser.parse_args()

    return opts


def sendandreceive(command, dt=1):
    send(command)
    time.sleep(dt)  # wait for 1 second
    reply = receive()
    return reply


def send(command):
    # send a packet using the specified device number, command number, and data
    # The data argument is optional and defaults to zero
    ser.write("%s\r\n" % command)


def receive():
    # return 6 bytes from the receive buffer
    # there must be 6 bytes to receive (no error checking)
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    return out


# Parse command line
opts = parse_commandline()

devUSB = "/dev/ttyUSB0"

# open serial port
# replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
ser = serial.Serial(devUSB)

try:
    ser = serial.Serial(devUSB, 115200, 8, 'N', 1, timeout=5)
except:
    print("Error opening com port. Quitting.")
    sys.exit(0)

if opts.verbose:
    print("Opening " + ser.portstr)

# Setup Lens
command = 'sm12'
reply = sendandreceive(command)
print reply

# Lens info
command = 'lc'
reply = sendandreceive(command)
print reply

command = 'la'
# reply = sendandreceive(command)
# print reply

# Get Bootloader version
command = 'bv'
# reply = sendandreceive(command)
# print reply

# Get aperture range
command = 'da'
reply = sendandreceive(command)
print reply

# Get zoom range
command = 'dz'
reply = sendandreceive(command)
print reply

if opts.doGetFocus:
    command = 'fp'
    reply = sendandreceive(command)
    print reply

    reply_split = reply.split(" ")
    reply_split = filter(None, reply_split)

    fmin = float(reply_split[0].replace("fmin:", ""))
    fmax = float(reply_split[1].replace("fmax:", ""))
    current = float(reply_split[2].replace("current:", "").replace("\r", ""))

    print "fmin: %.1f, fmax: %.1f, current: %.1f" % (fmin, fmax, current)

if opts.doFocus:
    focus = opts.focus
    focusstr = ("%04x" % (focus)).replace("0x", "")

    checksum = 0x0000
    mask = 0x1000
    for i in xrange(4):
        checksum = checksum ^ (focus / mask)
        mask = mask >> 4
    checksum = checksum & 0x0F
    checksumstr = ("%x" % checksum).replace("0x", "")

    command = 'eh%s,%s' % (focusstr, checksumstr)
    reply = sendandreceive(command)

if opts.doAperture:
    command = 'in'
    reply = sendandreceive(command)

    command = 'ma%d' % (opts.aperture)
    reply = sendandreceive(command)

ser.close()
