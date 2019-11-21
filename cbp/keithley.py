"""
.. module:: keithley
    :platform: unix
    :synopsis: This module is for communicating with the keithley instruments.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import optparse
import time

import numpy as np
import os
if 'TESTENVIRONMENT' in os.environ:
    import mock
    import sys
    sys.modules['visa'] = mock.Mock()
else:
    import visa
import cbp.monochromater
import cbp.shutter
from flipper import Flipper
#import thorlabs

import logging


def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doKeithley", action="store_true", default=False)
    parser.add_option("--doSingle", action="store_true", default=False)
    parser.add_option("--doReset", action="store_true", default=False)
    parser.add_option("--doShutter", action="store_true", default=True)
    parser.add_option("-t","--analysisType", default="duration")
    parser.add_option("-m","--mode", default='char')
    parser.add_option("-d","--duration", default=1, type=int)
    parser.add_option("-p","--photons", default=100000, type=int)
    parser.add_option("-q","--charge", default=10**-6, type=float)
    parser.add_option("-w","--wavelength", default=550, type=int)
    parser.add_option("-f", "--photonFile", default='/home/pi/CBP/keithley/test.dat')

    opts, args = parser.parse_args()

    return opts


class Keithley:
    """
    This is the class that stores the methods for communicating with the keithley devices.
    """
    def __init__(self, rm=None, resnum=None, mode='curr', nplc=1, do_reset=False):
        #try:
            self.status = {0:None,1:None}
            if rm is not None and resnum is not None:
                self.resnum = resnum
                self.rm = rm
                logging.info("Finding resource")
                if resnum == 0:
                    #devtty = 'ASRL/dev/ttyUSB.KEITHLEY1::INSTR'
                    devtty = 'ASRL/dev/ttyUSB0::INSTR'
                    print("keithley 1 found")
                    logging.info("keithley 1 found")
                elif resnum == 1:
                    devtty = 'ASRL/dev/ttyUSB.KEITHLEY2::INSTR'
                    print("keithley 2 found")
                    logging.info("keithley 2 found")
                else:
                    devtty = rm.list_resources()[resnum]
                try:
                    self.ins = self.rm.open_resource(devtty)
                except Exception as e:
                    logging.exception(e)
                    self.status[resnum] = "not connected"
            else:
                self.rm = visa.ResourceManager('@py')
                #resource = self.rm.list_resources(query='?*KEITHLEY?*::INSTR')[0]
                resource = self.rm.list_resources(query='?*USB0?*::INSTR')[0]
                self.ins = self.rm.open_resource(resource)
                self.resnum = 0
            self.ins.write_termination = '\n'
            self.ins.read_termination = '\n'
            self.ins.timeout = 5000
            self.ins.query_delay = 0.0

            # ins.write('SYST:ZCH OFF')  #see page 2-2
            # ins.write('SYST:AZER:STAT OFF') #see page 2-13+
            # self.selectmode(mode,nplc=nplc)
            # self.ins.write('CURR:RANG:AUTO ON')
            # self.ins.write('CHAR:RANG:AUTO ON')
            # self.ins.write('VOLT:RANG:AUTO ON')
            self.dispon(True)

            if do_reset:
                self.ins.write('*RST')
                self.ins.write('INIT')
            self.selectmode(mode, nplc=nplc)

            self.ins.write('SYST:ZCH ON')
            self.ins.write('SYST:ZCOR ON')
            self.ins.write('SYST:ZCH OFF')
            self.ins.write('SYST:ZCOR OFF')
            self.status[resnum] = "connected"
            self.photodiode_reading = {0:None,1:None}
        #except Exception as e:
        #    logging.exception(e)
        #    self.status[resnum] = "not connected"

    def check_status(self):
        try:
            self.getread()
        except Exception as e:
            logging.exception(e)
            self.status[self.resnum] = "not connected"

    def selectmode(self, mode, nplc):
        """

        :param mode: the mode to switch keithley to.
        :param nplc:
        :return: switches the keithley to a particular mode
        """
        if self.status[self.resnum] != "not connected":
            assert mode.lower() in ['volt', 'char', 'curr', 'res'], "No mode %s" % mode.lower()
            assert type(nplc) == type(1)  # assert that nplc is an int
            # self.ins.write('CONF:%s' % mode.upper())
            # self.ins.write('SENS:%s:NPLC %d' %(mode.upper(),nplc))
            self.ins.write("FUNC '%s'" % (mode.upper()))
        else:
            assert mode.lower() in ['volt', 'char', 'curr', 'res'], "No mode %s" % mode.lower()
            assert type(nplc) == type(1)  # assert that nplc is an int
            # self.ins.write('CONF:%s' % mode.upper())
            # self.ins.write('SENS:%s:NPLC %d' %(mode.upper(),nplc))
            self.ins.write("FUNC '%s'" % (mode.upper()))

    def dispon(self, on):
        """

        :param on: a boolean that tells the display to be on or off.
        :return: a keithley that has a display off or on.
        """
        if self.status[self.resnum] != "not connected":
            if on:
                self.ins.write('DISP:ENAB 1')
            else:
                self.ins.write('DISP:ENAB 0')
        else:
            if on:
                self.ins.write('DISP:ENAB 1')
            else:
                self.ins.write('DISP:ENAB 0')

    def getread(self):
        """

        :return: a numpy array of a float from the keithley reading.
        """
        '''Array returned is of the form
            [READING, TIME, STATUS]
            Where status is defined in the manual via bitmasks
        '''
        if self.status[self.resnum] != "not connected":
            return np.array(self.ins.query('READ?').split(',')).astype(np.float)
        else:
            pass

    def getquery(self, query):
        """

        :param query: a query to send to the keithley
        :return: returns the response to the query.
        """
        if self.status[self.resnum] != "not connected":
            return self.ins.query(query)
        else:
            pass

    def close(self):
        """
        closes the connection to the keithley

        :return: a closed connection to the keithley
        """
        if self.status[self.resnum] != "not connected":
            self.ins.close()
            self.rm.close()
        else:
            pass

    def do_reset(self,mode="curr",nplc=1):
        """

        :param mode:
        :param nplc:
        :return:
        """
        if self.status[self.resnum] != "not connected":
            self.ins.write('*RST')
            self.ins.write('INIT')

            self.selectmode(mode, nplc=nplc)

            self.ins.write('SYST:ZCH ON')
            self.ins.write('SYST:ZCOR ON')
            self.ins.write('SYST:ZCH OFF')
            self.ins.write('SYST:ZCOR OFF')
        else:
            pass

    def get_keithley(self,rm, duration=1, photons=100000, charge=10 ** -6, wavelength=550, mode='curr',
                     analysis_type='duration', do_single=False, do_reset=True, photon_file='test.dat',
                     do_shutter=True):
        if self.status[self.resnum] != "not connected":
            print("starting get_keithley")
            if do_single:
                # QE for NIST and Thorlabs
                filename = '../input/NIST_PD.txt'
                data_out = np.loadtxt(filename)
                qe_nist_pd = np.interp(wavelength, data_out[:, 0], data_out[:, 1])
                filename = '../input/NIST_Thorlabs.txt'
                data_out = np.loadtxt(filename)
                qe_thorlabs_pd = qe_nist_pd * \
                                 np.interp(wavelength, data_out[:, 0], data_out[:, 1] / data_out[:, 2])

                filename = '../input/CBP_throughput.txt'
                data_out = np.loadtxt(filename)
                throughput = np.interp(wavelength, data_out[:, 0], data_out[:, 1])
                throughput = throughput * 1.67  # Vignetting correction

                cbp.monochromater.main(runtype="monowavelength", val=wavelength)

                if True:
                    # try:
                    logging.info("entering true loop")
                    ins1 = Keithley(rm=rm, resnum=0, mode=mode, do_reset=do_reset)
                    if analysis_type == 'duration':
                        start_time = time.time()
                        elapsed_time = time.time() - start_time

                        times = []
                        photo1 = []
                        totphotons = []

                        for ii in xrange(10):
                            thistime = time.time()
                            elapsed_time = thistime - start_time

                            photo = ins1.getread()[0]

                            photo1.append(photo)
                            times.append(thistime)

                            intsphere_charge = photo
                            intsphere_electrons = intsphere_charge / (1.6 * 10 ** (-19))
                            totphoton = intsphere_electrons * throughput / qe_thorlabs_pd
                            totphotons.append(totphoton)

                        if do_shutter:
                            cbp.shutter.main(runtype="shutter", val=-1)
                        else:
                            cbp.shutter.main(runtype="shutter", val=1)
                        while elapsed_time < duration:
                            thistime = time.time()
                            elapsed_time = thistime - start_time
                            photo1.append(photo)
                            times.append(thistime)
                            totphotons.append(totphoton)

                        # time.sleep(duration)
                        cbp.shutter.main(runtype="shutter", val=1)

                        for ii in xrange(10):
                            thistime = time.time()
                            elapsed_time = thistime - start_time

                            photo = ins1.getread()[0]

                            photo1.append(photo)
                            times.append(thistime)

                            intsphere_charge = photo
                            intsphere_electrons = intsphere_charge / (1.6 * 10 ** (-19))
                            totphoton = intsphere_electrons * throughput / qe_thorlabs_pd
                            totphotons.append(totphoton)

                    elif (analysis_type == 'photons') or (analysis_type == 'charge'):

                        times = []
                        photo1 = []
                        totphotons = []
                        start_time = time.time()
                        totphoton = 0
                        intsphere_charge = 0

                        fid = open(photon_file, 'w')
                        for ii in xrange(10):
                            photo = ins1.getread()[0]
                            elapsed_time = time.time() - start_time

                            photo1.append(photo)
                            times.append(elapsed_time)

                            intsphere_charge = photo1
                            intsphere_electrons = intsphere_charge / (1.6 * 10 ** (-19))
                            totphoton = intsphere_electrons * throughput / qe_thorlabs_pd
                            totphotons.append(totphoton)
                            if analysis_type == "photons":
                                print "%.0f/%.0f" % (totphoton, photons)
                            elif analysis_type == "charge":
                                print("%.5e/%.5e" % (intsphere_charge, charge))
                            fid.write("%.10f %.10e %.0f\n" % (elapsed_time, photo1, totphoton))

                        cbp.shutter.main(runtype="shutter", val=-1)
                        if analysis_type == "photons":
                            while totphoton < photons:
                                photo1 = ins1.getread()[0]
                                elapsed_time = time.time() - start_time

                                photos1.append(photo1)
                                times.append(elapsed_time)

                                intsphere_charge = photo1
                                intsphere_electrons = intsphere_charge / (1.6 * 10 ** (-19))
                                totphoton = intsphere_electrons * throughput / qe_thorlabs_pd
                                totphotons.append(totphoton)

                                print "%.0f/%.0f" % (totphoton, photons)
                                fid.write("%.10f %.10e %.0f\n" % (elapsed_time, photo1, totphoton))
                        elif analysis_type == "charge":
                            while intsphere_charge < charge:
                                photo1 = ins1.getread()[0]
                                elapsed_time = time.time() - start_time

                                photos1.append(photo1)
                                times.append(elapsed_time)

                                intsphere_charge = photo1
                                intsphere_electrons = intsphere_charge / (1.6 * 10 ** (-19))
                                totphoton = intsphere_electrons * throughput / qe_thorlabs_pd
                                totphotons.append(totphoton)

                                print "%.5e/%.5e" % (intsphere_charge, charge)
                                fid.write("%.10f %.10e %.0f\n" % (elapsed_time, photo1, totphoton))
                        cbp.shutter.main(runtype="shutter", val=1)

                        for ii in xrange(10):
                            photo1 = ins1.getread()[0]
                            elapsed_time = time.time() - start_time

                            photos1.append(photo1)
                            times.append(elapsed_time)

                            intsphere_charge = photo1
                            intsphere_electrons = intsphere_charge / (1.6 * 10 ** (-19))
                            totphoton = intsphere_electrons * throughput / qe_thorlabs_pd
                            totphotons.append(totphoton)

                            if analysis_type == "photons":
                                print "%.0f/%.0f" % (totphoton, photons)
                            elif analysis_type == "charge":
                                print "%.5e/%.5e" % (intsphere_charge, charge)

                            fid.write("%.10f %.10e %.0f\n" % (elapsed_time, photo1, totphoton))

                        fid.close()
                        photo1 = photos1
                        # except:
                # times = [-1]
                #    photo1 = [-1]
                #    totphotons = [-1]
                # print times, photo1, totphotons
                return times, photo1, totphotons
            else:
                try:
                    logging.info("entering else loop")
                    ins1 = Keithley(rm=rm, resnum=0, mode=mode, do_reset=do_reset)
                    # ins2 = Keithley(rm = rm, resnum = 1, mode = mode, doReset = doReset)
                    time.sleep(duration)
                    photo1 = ins1.getread()
                    # photo2 = ins2.getread()
                    photo2 = [-1, -1, -1]
                except:
                    photo1 = [-1, -1, -1]
                    photo2 = [-1, -1, -1]

                return photo1[0], photo2[0]
        else:
            pass

    def get_photodiode_reading(self):
        """
        This method returns the photodiode reading of the keithley instruments.

        :return:
        """
        if self.status[self.resnum] != "not connected":
            time.sleep(.8)
            photo1 = self.getread()
            print("Diode {0} read".format(self.resnum))
            logging.info("Diode {0} read".format(self.resnum))
            self.photodiode_reading[self.resnum] = photo1[0]
            return photo1[0]
        else:
            return [-1,-1,-1]

    def get_charge_timeseries(self,duration=10,doShutter=True,cbp_inst=None):
        """

        :param duration:
        :return:
        """
        if self.status[self.resnum] != "not connected":
            times = []
            photol = []
            totphotons = []
            start_time = time.time()
            totphoton = 0
            intsphere_charge = 0
            flipper = Flipper()

            self.do_reset(mode="char",nplc=1)
            print "Getting first 10 Keithley at %s..."%time.time()
            #print "closed shutter"
            #cbp.shutter.main(runtype="shutter", val=1)
            for ii in xrange(10):
                photo = self.getread()[0]
                elapsed_time = time.time() - start_time

                photol.append(photo)
                times.append(elapsed_time)

            print "Opening/closing shutters at %s..."%time.time()
            #if doShutter:
            #     
            #    #cbp_inst.flipper.run_flipper(1)
            #    #cbp_inst.shutter.run_shutter(-1)
            #
            #    #thorlabs.thorlabs.main(val=1)
            #    #cbp.shutter.main(runtype="shutter", val=-1)
                #print "opened shutter"
            #else:
            #    cbp_inst.flipper.run_flipper(2)
            #    #cbp_inst.shutter.run_shutter(1)
            #    #cbp.shutter.main(runtype="shutter", val=1)
            #	print "closed shutter"
 
            print "Getting image Keithley at %s..."%time.time()
            elapsed_time_closed = time.time() - start_time 
            if doShutter:
                flipper.run_flipper(2)
            while elapsed_time < duration+elapsed_time_closed:
                photo = self.getread()[0]
                elapsed_time = time.time() - start_time

                photol.append(photo)
                times.append(elapsed_time)
            flipper.run_flipper(1)

            #cbp_inst.shutter.run_shutter(1)
            #cbp.shutter.main(runtype="shutter", val=1)
            #cbp_inst.flipper.run_flipper(2)
            #thorlabs.thorlabs.main(val=2)
            print "Shutter closed at %s..."%time.time()

            print "Getting final 10 Keithley at %s..."%time.time()
            for ii in xrange(10):
                photo = self.getread()[0]
                elapsed_time = time.time() - start_time

                photol.append(photo)
                times.append(elapsed_time)  
            print "Returning Keithley at %s..."%time.time()

            return times, photol
        else:
            pass

def main(runtype="keithley", duration=1, photons=100000, charge=10**-6, wavelength=550, mode='curr',
         analysis_type="duration", do_single=False, do_reset=False, photon_file='test.dat', do_shutter=True):
    keithley = Keithley()

    if runtype == "keithley":
        rm = visa.ResourceManager('@py')
        if do_single:
            times, photos, totphotons = keithley.get_keithley(rm = rm, duration = duration, mode = mode, photons = photons,
                                                     charge = charge, wavelength = wavelength,
                                                     analysis_type= analysis_type, do_single= do_single, do_reset= do_reset,
                                                     photon_file= photon_file, do_shutter= do_shutter)
            print times, photos, totphotons
            return times, photos, totphotons
        else:
            photo1, photo2 = keithley.get_keithley(rm = rm, duration = duration, mode = mode, photons = photons, charge = charge,
                                          wavelength = wavelength, analysis_type= analysis_type, do_single= do_single,
                                          do_reset= do_reset, photon_file= photon_file, do_shutter= do_shutter)
            print photo1, photo2 
            return photo1, photo2

if __name__ == "__main__":

    # # Parse command line
    opts = parse_commandline()
    rm = Keithley(resnum=0)
    times, photol = rm.get_charge_timeseries(duration=opts.duration)
    fid = open(opts.photonFile,'w')
    for tt,phot in zip(times,photol):
        fid.write('%.5f %.5e\n' % (tt,phot))
    fid.close()
    
    if opts.doKeithley:
         main(runtype="keithley", duration=opts.duration, photons=opts.photons, charge=opts.charge,
              wavelength=opts.wavelength, mode=opts.mode, analysis_type=opts.analysisType, do_single=opts.doSingle,
              do_reset=opts.doReset, photon_file=opts.photonFile, do_shutter=opts.doShutter)
   # pass

