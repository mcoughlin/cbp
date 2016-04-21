#!/usr/bin/env python

import serial, sys, time, glob, struct
import optparse

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
def sendandreceive(command, ser, dt = 1):
    send(command, ser)
    time.sleep(dt) # wait for 1 second
    reply = receive(ser)
    return reply

def send(command, ser):
   # send a packet using the specified device number, command number, and data
   # The data argument is optional and defaults to zero
   ser.write("%s\r\n"%command)

def receive(ser):
   # return 6 bytes from the receive buffer
   # there must be 6 bytes to receive (no error checking)
   out = ''
   while ser.inWaiting() > 0:
       out += ser.read(1)
   return out

def main(runtype = "focus", val = 1000):

    devUSB = "/dev/ttyUSB0"

    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    ser = serial.Serial(devUSB)

    try:
        ser = serial.Serial(devUSB, 115200, 8, 'N', 1, timeout=5)
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)

    #print "Opening %s"%ser.portstr

    # Setup Lens
    command = 'sm12'
    reply = sendandreceive(command,ser)
    #print reply

    # Lens info
    command = 'lc'
    reply = sendandreceive(command,ser)
    #print reply

    command = 'la'
    #reply = sendandreceive(command,ser)
    #print reply

    # Get Bootloader version
    command = 'bv'
    #reply = sendandreceive(command,ser)
    #print reply

    # Get aperture range
    command = 'da'
    #reply = sendandreceive(command,ser)
    #print reply

    # Get zoom range
    command = 'dz'
    #reply = sendandreceive(command,ser)
    #print reply

    if runtype == "focus":

        if (val < 0) or (val > 16383):
            raise Exception("Focus should be integer between 0-16383") 

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
        reply = sendandreceive(command,ser)

    elif runtype == "aperture":

        if (val < 0) or (val > 24):
            raise Exception("Focus should be integer between 0-24")

        command = 'in'
        reply = sendandreceive(command,ser)

        command = 'ma%d'%(val)
        reply = sendandreceive(command,ser)
    elif runtype == "status":

        command = 'fp'
        reply = sendandreceive(command,ser)

        reply = reply.replace("fp\rOK\r","")
        reply_split = reply.split(" ")
        reply_split = filter(None, reply_split)

        fmin = float(reply_split[0].replace("fmin:",""))
        fmax = float(reply_split[1].replace("fmax:",""))
        focus = float(reply_split[2].replace("current:","").replace("\r",""))

        #print reply_split

        print "fmin: %.1f, fmax: %.1f, current: %.1f"%(fmin,fmax,focus)

        command = 'pa'
        reply = sendandreceive(command,ser)

        print reply
        reply_split = reply.split(",")
        reply_split = filter(None, reply_split)

        aperture = float(reply_split[0])
        fstop = float(reply_split[1].replace("f",""))

        print focus, aperture
        return focus, aperture

    ser.close() 

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doFocus:
        main(runtype = "focus", val = opts.focus)
    if opts.doAperture:
        main(runtype = "aperture", val = opts.aperture)
    if opts.doStatus:
        focus, aperture = main(runtype = "status")
