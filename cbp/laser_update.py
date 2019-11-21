"""
.. module:: laser
    :platform: unix
    :synopsis: This module is for communicating with the laser.

.. codeauthor:: Eric Coughlin

This is a module that communicates with the ESKPLA laser in the lab via RS232 serial port.
"""

import serial
import argparse
import string
import numpy as np
import logging
import time


#  Error hex mask reported by manual.  See pg. 2-1-3 of NT-242 manual
class LaserError:
    def __init__(self, hex_val, status_msg):
        self.hex_val = hex_val
        self.status_msg = status_msg

SafetyI = LaserError(0x0001, 'Protective housing interlock circuit is open')
LDDerr = LaserError(0x0100, 'LD driver error')
CoolingErr = LaserError(0x0800, 'Cooling system failure')
Interlock = LaserError(0x1000, 'Remote interlock circuit is open')
BreakSwitch = LaserError(0x2000, 'Kill switch pressed')
KeySwitch = LaserError(0x4000, 'Key switch in off position')

error_list = [SafetyI, LDDerr, CoolingErr, Interlock, BreakSwitch, KeySwitch]

class LaserSerialInterface:
    """
    This class is for communicating with the laser through the RS232 serial interface.

    """

    def __init__(self, port='/dev/ttyUSB.LASER', interlock_okay=False):
        self.state = None
        self.active_errors = []
        self.commands = {'say_state_msg': '[NL:SAY\PC]'}
        self.responses = {'[NL:What\PC]': 'Unrecognized string', '[NL:Ignored\PC]': 'Unrecognized command'}
        self.serial = serial.Serial(port=port, baudrate=19200, timeout=2)
        self.status = 'connected'
        self.check_state()
        #self.get_wavelength()

    def check_state(self):
        """
        This method checks the status of the laser and then sets the state of the laser inside of the class.

        :return:
        """
        say_state_msg = self.commands['say_state_msg']
        self.serial.write(say_state_msg)
        response = self.serial.read(size=25)
        print('check_state response: {}'.format(response))
        if response == '':
            self.state = 'off'
            self.status = 'off'
            logging.info('check_state: Empty response')
            return
        
        try:
            #  Code returned by the laser is a hex bit mask
            mask = int(response.split('=')[-1].split('\\')[0])
            resp_str = response.split(':')[-1].split('=')[0]
            active_errors = []
            for error in error_list:  
                if mask & error.hex_val:
                    active_errors.append(error)
                    print('check_state: error present: {}'.format(error.status_msg))
                    logging.info('check_state: error present: {}'.format(error.status_msg))
            self.active_errors = active_errors
            if resp_str == 'READY':
                self.state = 'ready'
            else:
                self.state = resp_str.lower()
        except:
            self.state = 'error'
            print('Problem parsing response {}'.format(response))
            logging.info('Problem parsing reponse {}'.format(response))

    def wait_ready_state(self, timeout=10.):
        """
        This method calls the :py:meth:`check_state` until a ready state is set by the class.
        :param timeout: Timeout value in seconds
        :return:
        """
        start = time.time()
        if self.status in ['not connected', 'off']:
            logging.info('wait_ready_state: Laser not connected or off. Aborting.')
            raise RuntimeError('wait_ready_state: Laser not connected or off.  Aborting.')
        else:
            while self.state != 'ready':
                self.check_state()
                logging.info('wait_ready_state: Current state: {}'.format(self.state))
                if time.time() - start > timeout:
                    logging.info('wait_ready_state: Timeout')
                    raise RuntimeError('wait_ready_state: Timeout')

    def set_pump_level(self, pump_level, pmin=88, pmax=92):
        """
        Set the energy of the pump laser.  The Ekspla expects an integer between 0...1000, which is multiplied by
        0.1 to achieve a percentage power between 0.0 and 100.0.
        :param pump_level: Pump level to set in percentage.  Should generally not be less than 88 or more than 92.
        :param pmin: Minimum pump level.  Generally not less than 88.
        :param pmax: Maximum pump level.  Generally not more than 92.

        :return: None
        """
        self.wait_ready_state()
        if pump_level < pmin or pump_level > pmax:
            logging.info('set_pump_level: Pump level {} out of bounds {} to {}'.format(pump_level, pmin, pmax))
            raise ValueError('set_pump_level: Pump level {} out of bounds {} to {}'.format(pump_level, pmin, pmax))
        pump_level = int(pump_level * 10)
        assert pmin*10 <= pump_level <= pmax*10, 'Error converting pump_level to int'
        pump_level_msg = '[NL:I0/S{:d}\PC]'.format(pump_level)
        self.serial.write(pump_level_msg)
        logging.info('set_pump_level: Sent change pump level message "{}"'.format(pump_level_msg))

    def change_wavelength(self, wavelength, wmin=320, wmax=1500):
        """
        This method changes the wavelength of the laser.

        :param wavelength: This is the value of the wavelength to be set. Units are in nanometers.
        :param wmin: Minimum wavelength requestable
        :param wmax: Maximum wavelength requestable

        :return:
        """
        self.wait_ready_state()
        wavelength = np.float(wavelength)
        wavelength_change_msg = '[W0/S{:.1f}]'.format(wavelength)
        if wavelength < wmin or wavelength > wmax:
            logging.info('change_wavelength: Wavelength {} out of bounds {} to {}'.format(wavelength, wmin, wmax))
            raise ValueError('change_wavelength: Wavelength {} out of bounds {} to {}'.format(wavelength, wmin, wmax))
        self.serial.write(wavelength_change_msg)
        logging.info('change_wavelength: Sent change wavelength change request for {}'.format(wavelength))

    def get_wavelength(self):
        """
        :return wavelength: wavelength of laser
        """
        self.wait_ready_state()
        wavelength_check_msg = '[W0/?]'
        self.serial.write(wavelength_check_msg)
        response = self.serial.read(size=25)
        if response == '':
            raise RuntimeError('get_wavelength: No response to wavelength check')
        logging.info('get_wavelength: Laser response: {}'.format(response))
        wavelength = self.parse_wavelength(response)
        logging.info('get_wavelength: Laser wavelength: {}'.format(wavelength))
        return wavelength

    def parse_wavelength(self, msg, as_int=True):
        """
        This method parses through the message to get back the value of the wavelength

        :param msg: The message to parse.
        :param as_int: If True, return the wavelength as an integer.  Else, as a float.

        :return: returns the value of the wavelength as parsed.
        """
        self.wait_ready_state()
        wavelength = msg.split('S')[-1].split('\\')[0]
        if as_int:
            return np.int(wavelength)
        else:
            return np.float(wavelength)


def create_parser():
    parser = argparse.ArgumentParser(description='Changes the wavelength of the laser using rs232 interface.')
    parser.add_argument('wavelength', nargs=1, help='Sets the value of the wavelength of the laser.', type=float)
    return parser


def main(wavelength, port):
    """
    This creates a command line and arguments for the script.

    :return: None
    """

    laser_interface = LaserSerialInterface(port=port)
    laser_interface.change_wavelength(wavelength)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    wavelength = np.float(args.wavelength[0])
    main(wavelength, port='/dev/ttyUSB0')
