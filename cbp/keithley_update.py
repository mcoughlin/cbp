"""
.. module:: keithley
    :platform: unix
    :synopsis: This module is for communicating with the keithley instruments.

.. codeauthor:: Michael Coughlin, Eric Coughlin, Nick Mondrik
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
import cbp.shutter
from flipper import Flipper
import time
import logging


def parse_commandline():
    parser = optparse.OptionParser()

    parser.add_option("--doKeithley", action="store_true", default=False)
    parser.add_option("--doSingle", action="store_true", default=False)
    parser.add_option("--doReset", action="store_true", default=False)
    parser.add_option("--doShutter", action="store_true", default=True)
    parser.add_option("-d", "--duration", default=1, type=int)
    parser.add_option("-f", "--photonFile", default='/home/pi/CBP/keithley/test.dat')
    opts, args = parser.parse_args()

    return opts


class Keithley:
    def __init__(self, rm=None, resnum=None, mode='curr', nplc=1, do_reset=False):
        self.status = {0:None,1:None}
        self.nreads = 1  # used to keep track of whether we need to update TRIG:COUN
        try:
            self.rm = visa.ResourceManager('@py')
            print(self.rm.list_resources())
            devtty = self.rm.list_resources()[resnum]
            self.ins = self.rm.open_resource(devtty)
            self.resnum = resnum
        except Exception as e:
            logging.exception(e)
            print(e)

        self.ins.write_termination = '\n'
        self.ins.read_termination = '\n'
        self.ins.timeout = 5000
        self.ins.query_delay = 0.0
        self.dispon(True)

        if do_reset:
            self.ins.write('*RST')
            self.ins.write('INIT')
        self.selectmode(mode, nplc=nplc)

        self.ins.write('SYST:ZCH ON')
        self.ins.write('SYST:ZCH OFF')
        self.ins.write('SYST:ZCOR OFF')
        self.status[resnum] = "connected"
        self.photodiode_reading = {0:None,1:None}

    def zero_check(self, enable=True):
        msg = 'SYST:ZCH '
        msg += 'ON' if enable else 'OFF'
        self.ins.write(msg)

    def check_status(self):
        try:
            self.getread()
        except Exception as e:
            logging.exception(e)
            self.status[self.resnum] = "not connected"

    def selectmode(self, mode, nplc=1):
        """
        :param mode: the mode to switch keithley to.
        :param nplc: Number of power line cycles to average over
        :return: switches the keithley to a particular mode
        """
        assert mode.lower() in ['volt', 'char', 'curr', 'res'], 'No mode {}'.format(mode.lower())
        assert type(nplc) == type(1)  # assert that nplc is an int
        self.zero_check(True) # should always enable zero check before changing modes
        # self.ins.write('CONF:%s' % mode.upper())
        self.ins.write('SENS:%s:NPLC %d' % (mode.upper(), nplc))
        self.ins.write("FUNC '%s'" % (mode.upper()))

    def dispon(self, enable=True):
        """
        :param enable: Tells the display to be on (True) or off (False).
        :return:
        """
        msg = 'DISP: ENAB '
        msg += '1' if enable else '0'
        self.ins.write(msg)

    def getread(self, nreads=1):
        """
        :param nreads: Number of readings to take
        :return: a numpy array of a float from the keithley reading.
        """
        '''Array returned is of the form
            [READING, TIME, STATUS]
            [READING, TIME, STATUS] ...
            Where status is defined in the manual via bitmasks
        '''
        assert type(nreads) == int, 'nreads must be an integer'
        if nreads != self.nreads:
            self.ins.write('TRIG:COUN %d' % nreads)
            self.nreads = nreads
        toto = np.array(self.ins.query('READ?').split(','))
        return toto.astype(np.float).reshape((nreads, 3))

    def getquery(self, query):
        """
        :param query: a query to send to the keithley
        :return: returns the response to the query.
        """
        return self.ins.query(query)

    def close(self):
        """
        closes the connection to the keithley

        :return: a closed connection to the keithley
        """
        self.ins.close()
        self.rm.close()

    def do_reset(self, mode='char', nplc=1, reset_time=True):
        """
        :param mode: Mode to change the instrument to
        :param nplc: Number of power line cycles to average over
        :param reset_time: Boolean - resets timer on keithley, increasing timestamp precision
        :return:
        """
        self.ins.write('*RST')
        self.nreads = 1
        if reset_time:
            self.ins.write('SYST:TIME:RES')
        self.selectmode(mode, nplc=nplc)

    def get_charge_timeseries(self, duration=10, nprepost=10, light=True):
        """
        :param duration:
        :param doShutter:
        :param nprepost: Number of pre and post reads to take (both same)
        :return:
        """
        duration = np.float(duration)
        data = np.empty((0, 3))
        flipper = Flipper()
        flipper.run_flipper(1) # make sure shutter starts closed
        self.do_reset(mode="char", nplc=1)

        self.zero_check(True)
        time.sleep(2)  # let capacitor discharge
        self.zero_check(False)
        data = np.vstack((data, self.getread(nprepost)))
        start = time.time()
        if light:
            flipper.run_flipper(2)  # open shutter
        while time.time() - start < duration:
            data = np.vstack((data, self.getread(1)))
        flipper.run_flipper(1)
        data = np.vstack((data, self.getread(nprepost)))

        return data[:, 1], data[:, 0]  # return times and readings


if __name__ == "__main__":

    # # Parse command line
    opts = parse_commandline()
    rm = Keithley(resnum=0)
    times, photol = rm.get_charge_timeseries(duration=opts.duration)
    fid = open(opts.photonFile,'w')
    for tt,phot in zip(times,photol):
        fid.write('%.5f %.5e\n' % (tt,phot))
    fid.close()

