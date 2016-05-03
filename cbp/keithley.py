import visa
import numpy as np

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import pexpect

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doKeithley", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

class Keithley:
	def __init__(self,rm=None,resnum=None,mode='char',nplc=1):
		if rm is not None and resnum is not None:
			self.rm = rm
			self.ins = self.rm.open_resource(rm.list_resources()[resnum])
		else:
			self.rm = visa.ResourceManager('@py')
			self.ins = self.rm.open_resource(self.rm.list_resources()[0])
		self.ins.write_termination = '\n'
		self.ins.read_termination = '\n'
		self.ins.timeout = 5000
		self.ins.query_delay = 0.0

		#ins.write('SYST:ZCH OFF')  #see page 2-2
		#ins.write('SYST:AZER:STAT OFF') #see page 2-13+
		self.selectmode(mode,nplc=nplc)
                #self.ins.write('CURR:RANG:AUTO ON')
                #self.ins.write('CHAR:RANG:AUTO ON')
                #self.ins.write('VOLT:RANG:AUTO ON')
		#self.dispon(True)

                self.ins.write('*RST')
                self.ins.write('SYST:ZCH ON')
                self.ins.write('CURR:RANG 2e-9')
                self.ins.write('INIT') 
                self.ins.write('SYST:ZCOR:ACQ') 
                self.ins.write('SYST:ZCOR ON')
                #self.ins.write('CURR:RANG:AUTO ON')
                self.ins.write('SYST:ZCH OFF')
	
	def selectmode(self,mode,nplc):
		assert mode.lower() in ['volt','char','curr','res'], "No mode %s" % mode.lower()
		assert type(nplc) == type(1) #assert that nplc is an int
		#self.ins.write('CONF:%s' % mode.upper())
		self.ins.write('SENS:%s:NPLC %d' %(mode.upper(),nplc))

	def dispon(self,on):
		if on:
			self.ins.write('DISP:ENAB 1')
		else:
			self.ins.write('DISP:ENAB 0')

	def getread(self):
		'''Array returned is of the form 
			[READING, TIME, STATUS]
			Where status is defined in the manual via bitmasks
		'''
		return np.array(self.ins.query('READ?').split(',')).astype(np.float)
		
	def getquery(self,query):
		return self.ins.query(query)
		
	def close(self):
		self.ins.close()
		self.rm.close()

def get_keithley(rm):

    try:
        ins1 = Keithley(rm = rm, resnum = 0)
        ins1.ins.write("SYST:ZCH ON")
        ins1.ins.write("SYST:ZCH OFF")

        #ins1.selectmode("VOLT",10)

        print ins1
        photo1 = ins1.getread()
    except:
        photo1 = [-1,-1,-1]

    try:
        ins2 = Keithley(rm = rm, resnum = 1)
        ins2.ins.write("SYST:ZCH ON")
        ins2.ins.write("SYST:ZCH OFF")

        ins2.selectmode("VOLT",10)

        photo2 = ins2.getread()
    except:
        photo2 = [-1,-1,-1]

    return photo1, photo2

def main(runtype = "keithley"):

    if runtype == "keithley":
        rm = visa.ResourceManager('@py')
        print rm.list_resources()
        photo1, photo2 = get_keithley(rm = rm)
        print photo1, photo2
        return photo1[0], photo2[0]

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doKeithley:
        main(runtype = "keithley")

