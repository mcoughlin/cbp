#! /usr/bin/env python


import serial
import time
import string


#Opens the monochromator
def openinst(pname="/dev/ttyUSB1"):
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
		m="out.monochrom: Instrument not found on system. Check connections and instrument name."
	return m
	
#Queries the monochromator for its info
def hello():
	"""Asks the monochromator for its ID info. Returns a string to output window."""
	m.write("info?" + "\r\n")
	info = m.read(100)
	info  = info[7:]
	result = "out.monochrom: I am " + string.strip(info)
	return result
	
def gowave(wave, filename="test.txt"):
	"""Checks longpass filter, goes to wavelength wave (nm), and writes wavelength to file filename. Also returns result to commander."""
	m.write("filter?\r\n")
	r=m.read(100)
	if wave > 630:
		if int(r[9:]) != 1:
			m.write("filter 1\r\n")
			print "out.monochrom: Moving to filter 1"
		else:
			print "out.monochrom: Filter 1 already in place"
	else:
		if int(r[9:]) == 1:
			m.write("filter 2\r\n")
			print "out.monochrom: Moving to filter 2"
		else:
			if int(r[9:]) == 0:
				print "out.monochrom: Filter 2 already in place"
	m.write("gowave " + str(wave) + "\r\n")
	r = m.read(100)
	f=open(filename, 'a+')
	f.write(str(wave) + "\n")
	f.close()
	result = "commander.tell: " + str(wave)
	return result
	
	
def askwave():
	"""Returns current wavelength to commander."""
	m.write("wave?" + "\r\n")
	r = m.read(100)
	r = r[7:]
	result = "commander.tell: " + string.strip(r) + "nm"
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
def filter(filt):
	"""Moves to a filter numbered 1-6 in filter wheel attached to monochromator."""
	m.write("filter " + str(filt) + "\r\n")
	m.read(100)
	result = "out.monochrom: Moving to filter " + str(filt)
	return filt

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

