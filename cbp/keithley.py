import serial
import visa
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

rm = visa.ResourceManager('@py')
#ins = rm.open_resource(rm.list_resources()[0])
ins = rm.open_resource('ASRL/dev/ttyUSB0::INSTR')
print ins

ins.write_termination = '\n'
ins.read_termination = '\n'
ins.timeout = 5000
ins.query_delay = 0.1 #delay before responding to a query.  I think this has a hand in setting the fundamental
#response rate

chk = ins.write('*RST')
print chk
chk = ins.write('*CLS')
print chk
print ins.query('*IDN?')


ins.write('FORM:ELEM READ')
ins.write('FORM:BORD SWAP')
ins.write('FORM:DATA SRE')
ins.write('TRIG:DEL 0')
ins.write('TRIG:COUN 1')
ins.write('DISP:ENAB OFF')
ins.write('NPLC .01')
ins.write('RANG 2e-9')
ins.write('SYST:ZCH OFF')
ins.write('SYST:AZER:STAT OFF')

tot_time = 0
print ins.query('*OPC?')

#at start of the read, record time.time(), and append this to each measurement
#this will be time in [s] (BUT IM NOT SURE SINCE WHEN, BECAUSE THIS IS BEING WRITTEN ON WINDOWS
#IT MIGHT MATTER WHICH OS THIS IS BEING RUN ON SO BE CAREFUL)

#this time can later be converted to a sensible interpretation via time.ctime(mytimestamp)

dt =  90#time to read for in s
vals = []
#need info for filename construction
#wavelength = sys.argv[1]
#wavelength = int(wavelength)
#light = sys.argv[2]
#if light == "0":
#	light = "dark"
#else:
#	light = "light"
fname = "ut030616." + sys.argv[1] + ".photodiode.txt"
wave = raw_input("WAVELENGTH? >>")
light = raw_input("LIGHT/DARK? >>")
disp = raw_input("DISPERSED? >>")
header = "WAVELENGTH: %s LIGHT/DARK: %s DISP: %s" % (wave,light,disp)

#fname = "%04d_nm_%s.txt" % (wavelength,light)
if os.path.exists(fname):
	print "WARNING: PATH ALREADY EXISTS!!!!!"
	cont = raw_input("CONTINUE? [y/[n]] >>")
	if cont.lower() != "y":
		sys.exit()

tstart = time.time()
i=0
print time.time()
while time.time() - tstart < dt:
	print time.time()
	i += 1
	vals.append([np.float32(ins.query('READ?')),time.time()])
	if i%100 == 0:
		print vals[-1]
vals = np.array(vals)
print vals
print "got " + str(vals.shape[0]) + " readings"
np.savetxt(fname,vals,header=header)
plt.plot([float(v)/1E-9 for v in vals[:,0]],'-k',lw=2)
plt.show(block=False)
a = raw_input(">>Press ENTER to exit<<")
