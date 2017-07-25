#! /usr/bin/env python

import serial
import time
import string
import numpy as np
import optparse


class Monochromater:
    def __init__(self):
        self.status = None
        self.serial = self.open_instance(port_name="/dev/ttyUSB.MONO")

    def open_instance(self,port_name='/dev/ttyUSB0'):
        """
        Opens the monochromator on port pname. Warning: will return ok if any serial instrument is found on the port, so
        check port name carefully.
        """
        try:
            global m
            m = serial.Serial(port_name)
            m.timeout = 2
            # m.rtscts = False
            # m.dsrdtr = False
            m.write("wave?" + "\r\n")
            m.read(100)
            self.status = "Connected"
        except Exception as e:
            print(e)
            self.status = "not connected"
            m = []
        return m

    def get_info(self):
        """Asks the monochromator for its ID info. Returns a string to output window."""
        if self.status != "not connected":
            m = self.serial
            m.write("info?" + "\r\n")
            info = m.read(100)
            info = info[7:]
            result = string.strip(info)
            return result
        else:
            pass

    def gograt(self, grat):
        if self.status != "not connected":
            m = self.serial
            if grat not in [1, 2, 3]:
                raise
            m.write('GRAT %d\r\n' % grat)
            m.read()
            return
        else:
            pass

    def getgrat(self):
        if self.status != "not connected":
            m = self.serial
            m.write('GRAT?\r\n')
            r = m.read(200)
            # print r
            r = r[4]
            result = string.strip(r)
            return result
        else:
            pass

    def gowave(self, wave):
        """
        Checks longpass filter, goes to wavelength wave (nm), and writes wavelength to file filename. Also returns
        result to commander.
        """
        if self.status != "not connected":
            m = self.serial
            m.write("filter?\r\n")
            r = m.read(100)
            # m.write("filter 1\r\n")

            # adjust order blocking filter, if necessary
            if wave < 600:
                if int(r[9:]) != 1:
                    m.write("filter 1\r\n")
                # print "out.monochrom: Moving to filter 1 (no filter)"
                else:
                    # print "out.monochrom: Filter 1 already in place"
                    pass
            elif wave >= 600:
                if int(r[9:]) != 2:
                    m.write("filter 2\r\n")
                # print "out.monochrom: Moving to filter 2"
                else:
                    # print "out.monochrom: Filter 2 already in place"
                    pass
            # elif wave <= 1050:
            #        if int(r[9:]) != 2:
            #                m.write("filter 2\r\n")
            #                print "out.monochrom: Moving to filter 2"
            #        else:
            #                print "out.monochrom: Filter 2 already in place"
            # elif wave > 1050:
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
        else:
            pass

    def askwave(self):
        """Returns current wavelength to commander."""
        if self.status != "not connected":
            m = self.serial
            m.write("wave?" + "\r\n")
            r = m.read(100)
            r = r[7:]
            result = string.strip(r)
            return result
        else:
            pass

    def closeinstance(self):
        """Closes the monochromator connection."""
        if self.status != "not connected":
            m = self.serial
            m.close()
            result = "out.monochrom: Closed monochromator connection."
            return result
        else:
            pass

    def scan(self, start, end, stepsize, sleeptime, filename='test.txt'):
        """Scans from start (nm) to end (nm) in steps of stepsize (nm). Sleeps for sleeptime seconds at each wavelength. Writes list of wavelengths to file filename"""
        if self.status != "not connected":
            self.gowave(start)
            time.sleep(5)
            wave = start
            while wave <= end:
                time.sleep(sleeptime)
                self.gowave(wave + stepsize)
                wave = wave + stepsize
            result = "out.monochrom: Finished scanning from " + str(start) + " to " + str(end) + "nm."
            return result
        else:
            pass

    def gofilter(self, filt):
        """Moves to a filter numbered 1-6 in filter wheel attached to monochromator."""
        if self.status != "not connected":
            m = self.serial
            m.write("filter " + str(filt) + "\r\n")
            m.read(100)
            result = "out.monochrom: Moving to filter " + str(filt)
            return filt
        else:
            pass

    def askfilter(self):
        """Returns current wavelength to commander."""
        if self.status != "not connected":
            m = self.serial
            m.write("filter?" + "\r\n")
            r = m.read(100)
            r = r[9:]
            result = string.strip(r)
            return result
        else:
            pass

    def shutter(self, state):
        """Opens ('O') or closes ('C') the monochromator shutter."""
        if self.status != "not connected":
            m = self.serial
            m.write("shutter " + str(state) + "\r\n")
            r = m.read(100)
            if state == 'O':
                st = "open"
            else:
                st = "closed"
            result = "out.monochrom: Shutter is " + st
            return result
        else:
            pass

    def disconnect(self):
        """Disconnects the monochromator."""
        if self.status != "not connected":
            return "disconnect"
        else:
            pass

    def monowavelength(self, val):
        if self.status != "not connected":
            self.gowave(val)
        else:
            pass

    def monofilter(self, val):
        if self.status != "not connected":
            self.gofilter(val)
        else:
            pass

    def monograting(self, val):
        if self.status != "not connected":
            self.gograt(val)
            grat = self.getgrat()
            print grat
        else:
            pass

    def get_mono(self):
        if self.status != "not connected":
            wave = self.askwave()
            filter = self.askfilter()
            try:
                wave = float(wave)
            except:
                wave = -1
            try:
                filter = float(filter)
            except:
                filter = -1

            print wave, filter
            return wave, filter
        else:
            pass


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-w", "--wavelength", default=600, type=int)
    parser.add_option("-f", "--filter", default=1, type=int)
    parser.add_option("-g", "--grating", default=3, type=int)
    parser.add_option("--doMonoWavelength", action="store_true", default=False)
    parser.add_option("--doMonoFilter", action="store_true", default=False)
    parser.add_option("--doMonoGrating", action="store_true", default=False)
    parser.add_option("--doGetMono", action="store_true", default=False)
    parser.add_option("-v", "--verbose", action="store_true", default=False)

    opts, args = parser.parse_args()

    return opts


def main(runtype="wavelength", val=1000):
    monochromater = Monochromater()

    if runtype == "monowavelength":
        monochromater.monowavelength(val)
    elif runtype == "monofilter":
        monochromater.monofilter(val)
    elif runtype == "monograting":
        monochromater.monograting(val)

    elif runtype == "getmono":
        return monochromater.get_mono()


if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doMonoWavelength:
        main(runtype="monowavelength", val=opts.wavelength)
    if opts.doMonoFilter:
        main(runtype="monofilter", val=opts.filter)
    if opts.doGetMono:
        main(runtype="getmono")
    if opts.doMonoGrating:
        main(runtype="monograting", val=opts.grating)
