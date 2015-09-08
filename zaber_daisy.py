#!/usr/bin/env python

import serial, sys, time, glob, struct
import optparse

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-n","--steps",default=1000,type=int)
    parser.add_option("-d","--device",default=1,type=int)
    parser.add_option("-c","--currentpos",default=0,type=int)
    parser.add_option("-p","--position",default=0,type=float)
    parser.add_option("-u","--units", default='mm')
    parser.add_option("--doSteps", action="store_true",default=False)
    parser.add_option("--doHome", action="store_true",default=False)
    parser.add_option("--doPosition", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)
    parser.add_option("--doSetCurrent", action="store_true",default=False)
    parser.add_option("-v","--verbose", action="store_true",default=False)

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

# Parse command line
opts = parse_commandline()

device = opts.device
if device == 1:
    devUSB = "/dev/tty.usbserial"
elif device == 2:
    devUSB = "/dev/tty.usbserial"

# open serial port
# replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
try:
   ser = serial.Serial(devUSB, 9600, 8, 'N', 1, timeout=5)
except:
   print("Error opening com port. Quitting.")
   sys.exit(0)

if opts.verbose:
    print("Opening " + ser.portstr)

zabertomm = 0.49609375 / 1000.0
if opts.units == "mm":
    if opts.position > 450 or opts.position < 0:
        raise Exception("Position must be between 0-75")
else:
    if opts.position > 907086 or opts.position < 0:
        raise Exception("Position must be integer between 0-907086")

#command = 121

#print "Moving in steps..."
#command = 2
#data = 0
#print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
#send(device, command, data)
#time.sleep(10) # wait for 1 second
#reply = receive()

# Reply data is calculated from all reply bytes
#replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
#if reply[5] > 127:
#    replyData -= 256.0**4
#print("Device: " + str(replyData))

#device = int(replyData)
#print device
#device = 1

if opts.doHome:
    #command = 42
    #data = 100000
    #send(device, command, data)
    #print "Sleeping for 60s..."
    #time.sleep(10)

    print "Moving to home..."
    command = 1
    data = 0
    #print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(device, command, data)
    print "Sleeping for 60s..."
    time.sleep(1)

if opts.doSetCurrent:

    print "Setting to %d..."%opts.currentpos
    command = 45
    data = opts.currentpos
    #print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(device, command, data)
    print "Sleeping for 60s..."
    time.sleep(1)

if opts.doPosition:

    if opts.verbose:
        print "Getting position..."
    command = 60
    data = 0
    #print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(device, command, data)
    time.sleep(1) # wait for 1 second
    reply = receive()

    # Reply data is calculated from all reply bytes
    replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
    if reply[5] > 127:
        replyData -= 256.0**4
    pos = int(replyData)

    if opts.units == "mm":
        pos = pos * zabertomm

    if opts.verbose:
        print "Position: %.3f"%pos
        print "Moving to position %.3f from %.3f..."%(opts.position,pos)
    command = 21

    data = opts.position - pos
    if opts.units == "mm":
        data = data / zabertomm

    #print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(device, command, data)
    time.sleep(1) # wait for 1 second
    reply = receive()

if opts.doSteps:
    print "Moving in steps..."
    command = 21
    data = opts.steps
    #print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(device, command, data)
    time.sleep(1) # wait for 1 second
    reply = receive()

if opts.doGetPosition:
    if opts.verbose:
        print "Getting position..."
    command = 60
    data = 0
    #print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(device, command, data)
    time.sleep(1) # wait for 1 second
    reply = receive()

    # Reply data is calculated from all reply bytes
    replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
    if reply[5] > 127:
        replyData -= 256.0**4

    pos = int(replyData)
    if opts.units == "mm":
        pos = pos * zabertomm
    print "Position: %.3f"%pos

if opts.verbose:
    print("Closing " + ser.portstr)
ser.close() 


