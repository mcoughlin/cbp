#! /usr/bin/env python

import serial
import time
import string
import numpy as np
import optparse

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-w","--wavelength",default=600,type=int)
    parser.add_option("-f","--filter",default=1,type=int)
    parser.add_option("--doMonoWavelength", action="store_true",default=False)
    parser.add_option("--doMonoFilter", action="store_true",default=False)
    parser.add_option("--doGetMono", action="store_true",default=False)
    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

#Opens the monochromator
def openinst(pname="/dev/ttyUSB0"):
	"""Opens the monochromator on port pname. Warning: will return ok if any serial instrument is found on the port, so check port name carefully."""
	try:
		global m
		m = serial.Serial(pname)
		m.timeout=2
		#m.rtscts = False
		#m.dsrdtr = False
		m.write("wave?" + "\r\n")
		m.read(100)
	except:
		m=[]
	return m
	
#Queries the monochromator for its info
def hello():
	"""Asks the monochromator for its ID info. Returns a string to output window."""
	m.write("info?" + "\r\n")
	info = m.read(100)
	info  = info[7:]
	result = string.strip(info)
	return result
	
def gowave(wave):
	"""Checks longpass filter, goes to wavelength wave (nm), and writes wavelength to file filename. Also returns result to commander."""
	m.write("filter?\r\n")
	r=m.read(100)
        #m.write("filter 1\r\n")

        # adjust order blocking filter, if necessary
	if wave < 450:
                if int(r[9:]) != 1:
                        m.write("filter 1\r\n")
                        print "out.monochrom: Moving to filter 1 (no filter)"
                else:
                        print "out.monochrom: Filter 1 already in place"
        elif wave <= 750:
		if int(r[9:]) != 2:
			m.write("filter 2\r\n")
			print "out.monochrom: Moving to filter 2"
		else:
			print "out.monochrom: Filter 2 already in place"
        #elif wave <= 1050:
        #        if int(r[9:]) != 2:
        #                m.write("filter 2\r\n")
        #                print "out.monochrom: Moving to filter 2"
        #        else:
        #                print "out.monochrom: Filter 2 already in place"
	#elif wave > 1050:
	#	if int(r[9:]) == 3:
	#		m.write("filter 3\r\n")
	#		print "out.monochrom: Moving to filter 3"
	#	else:
	#		if int(r[9:]) == 0:
	#			print "out.monochrom: Filter 3 already in place"
	m.write("gowave " + str(wave) + "\r\n")
	r = m.read(100)
	result = wave
	return result
	
	
def askwave():
	"""Returns current wavelength to commander."""
	m.write("wave?" + "\r\n")
	r = m.read(100)
	r = r[7:]
	result = string.strip(r)
	return result 

def closeinst():
	"""Closes the monochromator connection."""
	m.close()
	result = "out.monochrom: Closed monochromator connection."
	return result

#Scans wavelengths from start to end in steps of stepsize, waiting for sleeptime at each one
def scan(start, end, stepsize, sleeptime, filename='test.txt'):
	"""Scans from start (nm) to end (nm) in steps of stepsize (nm). Sleeps for sleeptime seconds at each wavelength. Writes list of wavelengths to file filename"""
	gowave(start, filename)
	time.sleep(5)
	wave = start
	while wave <= end:
		time.sleep(sleeptime)
		gowave(wave+stepsize, filename)
		wave = wave+stepsize
	result = "out.monochrom: Finished scanning from " + str(start) + " to " + str(end) + "nm."
	return result
	
#Moves to a filter numbered from 1 to 6	
def gofilter(filt):
	"""Moves to a filter numbered 1-6 in filter wheel attached to monochromator."""
	m.write("filter " + str(filt) + "\r\n")
	m.read(100)
	result = "out.monochrom: Moving to filter " + str(filt)
	return filt

def askfilter():
        """Returns current wavelength to commander."""
        m.write("filter?" + "\r\n")
        r = m.read(100)
        r = r[9:]
        result = string.strip(r)
        return result

#Opens and closes the shutter: State is either "C" (closed) or "O" (open)
def shutter(state):	
	"""Opens ('O') or closes ('C') the monochromator shutter."""
	m.write("shutter " + str(state) + "\r\n")
	r = m.read(100)
	if state == 'O':
		st = "open"
	else:
		st = "closed"
	result = "out.monochrom: Shutter is " + st
	return result

#Disconnects	
def disconnect():
	"""Disconnects the monochromator."""
	return "disconnect"

def main(runtype = "wavelength", val = 1000):

    devUSB = "/dev/ttyUSB1"

    m = openinst(pname=devUSB)
    if not m:
        return -1, -1

    out = hello()
    #print out

    if runtype == "monowavelength":
        gowave(val)
    elif runtype == "monofilter":
        gofilter(val)
    elif runtype == "getmono":
        wave = askwave()
        filter = askfilter()
        return wave, filter

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doMonoWavelength:
        main(runtype = "monowavelength", val = opts.wavelength)
    if opts.doMonoFilter:
        main(runtype = "monofilter", val = opts.filter)
    if opts.doGetMono:
        main(runtype = "getmono")


