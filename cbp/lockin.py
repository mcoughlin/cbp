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

    parser.add_option("--doSR830", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts


class SR830:
    def __init__(self,rm=None,resnum=None):
        if rm is not None and resnum is not None:
            self.rm = rm
            if resnum == 0:
                devtty = 'ASRL/dev/ttyUSB.SR830::INSTR'
            else:
                devtty = rm.list_resources()[resnum]
        else:
            self.rm = visa.ResourceManager('@py')
            devtty = self.rm.list_resources()[0]
        self.io = self.rm.open_resource(devtty)

        self.io.write_termination = '\r'
        self.io.read_termination = '\r'
        self.io.timeout = 5000
        self.io.query_delay = 0.0

        #The OUTX command sets the output interface to RS232 (i=0) or GPIB (i=1)
        if devtty.count("GPIB"):
            self.io.write("OUTX 1")
        print self.io.ask("*IDN?")

        self.sensitivity_dict={'2 nV/fA':0,'50 uV/pA':13,
                     '5 nV/fA':1,'100 uV/pA':14,
                     '10 nV/fA':2,'200 uV/pA':15,
                     '20 nV/fA':3,'500 uV/pA':16,
                     '50 nV/fA':4,'1 mV/nA':17,
                     '100 nV/fA':5,'2 mV/nA':18,
                     '200 nV/fA':6,'5 mV/nA':19,
                     '500 nV/fA':7,'10 mV/nA':20,
                     '1 uV/pA':8,'20 mV/nA':21,
                     '2 uV/pA':9,'50 mV/nA':22,
                     '5 uV/pA':10,'100 mV/nA':23,
                     '10 uV/pA':11,'200 mV/nA':24,
                     '20 uV/pA':12,'500 mV/nA':25,
                     '1 V/uA':26}

        sens_list_utf8=['2 nV/fA','5 nV/fA','10 nV/fA','20 nV/fA','50 nV/fA','100 nV/fA','200 nV/fA','500 nV/fA',
                        '1 uV/pA','2 uV/pA','5 uV/pA','10 uV/pA','20 uV/pA','50 uV/pA','100 uV/pA','200 uV/pA',
                        '500 uV/pA','1 mV/nA','2 mV/nA','5 mV/nA','10 mV/nA','20 mV/nA','50 mV/nA','100 mV/nA',
                        '200 mV/nA','500 mV/nA','1 V/uA']
        
        self.sens_list_num=[2e-9,5e-9,10e-9,20e-9,50e-9,100e-9,200e-9,500e-9,
                        1e-6,2e-6,5e-6,10e-6,20e-6,50e-6,100e-6,200e-6,
                        500e-6,1e-3,2e-3,5e-3,10e-3,20e-3,50e-3,0.1,
                        0.2,0.5,1]
        #the encoding of the python script file is utf8 but the Qt interface is unicode, so conversion is needed
        self.sensitivity=[]
        for txt in sens_list_utf8:
            self.sensitivity.append(unicode(txt,encoding='utf-8'))
        #time constant
        time_cste_list_utf8=['10 us','30 us','100 us','300 us','1 ms','3 ms','10 ms','30 ms','100 ms','300 ms',
                        '1 s','3 s','10 s','30 s','100 s','300 s','1 ks','3 ks','10 ks','30 ks']
        self.time_cste=[]
        for txt in time_cste_list_utf8:
            self.time_cste.append(unicode(txt,encoding='utf-8'))
        #filter slop
        self.filter_slop=map(unicode,['6 dB/oct','12 dB/oct','18 dB/oct','24 dB/oct'])

    def initialize(self):
        return 1      
        
    def query_unit_Id(self):
        return self.io.ask("*IDN?")

    #def set_harmonic(self,i=1):
        #"""set the i-th harmonic to measure"""
        #self.io.write("HARM"+str(i-1))
        ##NB: HARM0 is the fundamental, HARM1 is the 2f harmonic

    #def set_REF_IN_resistance(self,i=1):
        #"""set the input impedance of the reference input: i=1 -> 10kOhm"""
        #self.io.write("REFZ"+str(i))

    #def set_SIGNAL_IN_resistance(self,i=1):
        #"""set the input impedance of the signal input: i=1 -> 1MOhm"""
        #self.io.write("INPZ"+str(i))

    #def query_f_R_theta(self):
        #"""query the frequency, radius and phase of signal"""
        #return self.io.ask_for_values("SNAP?8,3,5")

#commands below works for SR830, todo: check if they are the same for SR844

    def set_ref_mode(self,i):
        """set the reference source. The parameter i selects internal (i=1) or external (i=0)"""
        conv={'Internal':1,'External':0,1:1,0:0}
        self.io.write("FMOD"+str(conv[i]))
        
    def query_ref_mode(self):
        """returns 1 (internal) or 0 (external)"""
        return int(self.io.ask("FMOD?"))
        
    def set_AUX1(self,value):
        if type(value)==float:
            self.io.write('AUXV1,'+str(value))
        else:
            raise TypeError

    def query_AUX1_out(self):
        return float(self.io.ask('AUXV?1'))


    def set_frequency(self,f):
        """set the reference frequency"""
        self.io.write("FREQ"+str(f))

    def query_frequency(self):
        """query the reference frequency"""
        return float(self.io.ask("FREQ?"))

    def set_amplitude(self,value):
        if type(value)==float:
            self.io.write('SLVL'+str(value))
        else:
            raise TypeError

    def query_amplitude(self):
        return float(self.io.ask('SLVL?'))
        
    def query_phase(self):
        return float(self.io.ask('PHAS?'))
    
    def set_phase(self,value):
        if value>=-360.0 and value <=729.99:
            self.io.write('PHAS'+str(value))
    
    def query_f_R_theta(self):
        """query the frequency, radius and phase of signal"""
        return self.io.ask_for_values("SNAP?9,3,4")
        
    def query_R_theta(self):
        """query the radius and phase of signal at the exact same instant"""
        return self.io.ask_for_values("SNAP?3,4")

    def query_XY(self):
        """query the X and Y of signal at the exact same instant"""
        return self.io.ask_for_values("SNAP?1,2")
        
    def set_harmonic(self,i=1):
        """set the i-th harmonic to measure"""
        self.io.write("HARM"+str(i))
        #NB: HARM1 is the fundamental, HARM2 is the 2f harmonic

    def query_sensitivity(self):
        return int(self.io.ask("SENS?"))
    
    def set_sensitivity(self,value=12):
        self.io.write('SENS'+str(value))
    
    def query_time_cste(self):
        return int(self.io.ask("OFLT?"))
    
    def set_time_cste(self,value=10):
        self.io.write('OFLT'+str(value))
        
    def query_filter_slop(self):
        return int(self.io.ask("OFSL?"))     

    def set_filter_slop(self,value=3):
        self.io.write('OFSL'+str(value))
        
    def set_ch1_display(self,x):
        ch1={'X':'0','R':'1','X Noise':'2','Aux In 1':'3','Aux In 2':'4'}
        if x in ch1:
            self.io.write('DDEF1,'+ch1[x]+',0')
            
    def set_ch2_display(self,y):
        ch2={'Y':'0','theta':'1','Y Noise':'2','Aux In 3':'3','Aux In 4':'4'}
        if y in ch2:
            self.io.write('DDEF2,'+ch2[y]+',0')
            
    def query_ch1_display(self):
        return int(self.io.ask_for_values("DDEF?1")[0])
    
    def query_ch2_display(self):
        return int(self.io.ask_for_values("DDEF?2")[0])
        
    def query_ch1_ch2(self,x,y):
        """query the ch1 and ch2 of signal at the same instant"""
        conv={'X':'1','Y':'2','R':'3','theta':'4','Aux In 1':'5','Aux In 2':'6','Aux In 3':'7','Aux In 4':'8','Reference Frequency':'9','CH1 display':'10','CH2 display':'11'}
        return float(self.io.query("OUTP?"+conv[x])),float(self.io.query("OUTP?"+conv[y]))
        #return self.io.ask_for_values("SNAP?"+conv[x]+','+conv[y])

    def get_sr830(self):

        ins = self

        photo = []
        while len(photo) == 0:
            try:
                photo = ins.query_ch1_ch2('R','theta')
            except:
                continue
        return photo[0]


def main(runtype="sr830"):
    sr830 = SR830()
    if runtype == "sr830":
        rm = visa.ResourceManager('@py')
        photo = sr830.get_sr830()
        return photo

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doSR830:
        main(runtype="sr830")

