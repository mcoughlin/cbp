"""
.. module:: laser
    :platform: unix
    :synopsis: This module is for communicating with the laser.

.. codeauthor:: Eric Coughlin

This is a module that communicates with the ESKPLA laser in the lab via RS232 port.
"""

import serial
import argparse
import string
import numpy as np
import logging


class LaserSerialInterface:
    """
    This class is for communicating with the laser through the RS232 serial interface.

    """

    def __init__(self, loop=True):
        self.state = None
        self.error = None
        self.states = {'[PC:READY=0\NL]': ['ready', 'The device is ready'],'[PC:BUSY=0\NL]': ['busy', 'The device is busy'], '[PC:OFF=0\NL]': ['off', 'The device is off'], '[PC:READY=2048\NL]': ['ready', 'The device is ready but with cooling error.'], '': ['off', 'The device is off']}
        self.commands = {'say_state_msg': '[NL:SAY\PC]'}
        self.responses = {'[NL:What\PC]': 'Unrecognized string', '[NL:Ignored\PC]': 'Unrecognized command'}
        if loop:
            self.serial = serial.serial_for_url('loop://')
        else:
            try:
                self.serial = serial.Serial(port='/dev/ttyUSB.LASER', baudrate=19200, timeout=3)
                self.status = "connected"
                self.check_state()
                self.check_wavelength()
            except Exception as e:
                print(e)
                self.status = "not connected"
                self.state = "not connected"

    def test_state(self):
        """
        This is a method for testing the state of the laser in a loop-back environment.

        :return:
        """
        if self.status != "not connected":
            responses = ['[PC:OFF=0\NL]', '[PC:BUSY=0\NL]', '[PC:BUSY=0\NL]', '[PC:READY=0\NL]']
            for response in responses:
                say_state_msg = self.commands['say_state_msg']
                self.serial.write(say_state_msg)
                if response in self.states:
                    self.state = self.states[response][0]
                    print(self.states[response][1])
        else:
            pass

    def check_state(self):
        """
        This method checks the status of the laser and then sets the state of the laser inside of the class.

        :return:
        """

        if self.status != "not connected" and self.status != "off":
            say_state_msg = self.commands['say_state_msg']
            self.serial.write(say_state_msg)
            response = self.serial.read(size=25)
            if response == "":
                self.state = "off"
                self.status = "off"
                logging.info("The laser is off")
                return
            if response in self.states:
                self.state = self.states[response][0]
                print(self.states[response][1])
            else:
                logging.info("Not found.")
        else:
            pass

    def get_ready_state(self):
        """
        This method calls the :py:meth:`check_state` until a ready state is set by the class.

        :return:
        """
        if self.status != "not connected" and self.status != "off":
            while self.state != 'ready' and self.state != 'off' and self.state != 'not connected':
                logging.info("checking state...")
                self.check_state()
        else:
            pass

    def change_wavelength(self, wavelength):
        """
        This method changes the wavelength of the laser.

        :param wavelength: This is the value of the wavelength to be set. Units are in nanometers and limits are 355nm to 2300 nm.

        :return:

        """
        if self.status != "not connected" and self.status != "off":
            self.get_ready_state()
            if self.state != "off" and self.state != "not connected":
                wavelength_change_msg = '[W0/S{0}]'.format(str(wavelength))
                if wavelength < 355 or wavelength > 1100:
                    raise Exception("Wavelength limits exceeded bounds")
                else:
                    self.serial.write(wavelength_change_msg)
                check_response = self.check_wavelength(comparison=True)
                if int(wavelength) == check_response:
                    logging.info("Wavelength set correctly")
                else:
                    logging.info("Something went wrong")
            elif self.state == "off":
                raise Exception('The laser is turned off')
            elif self.state == "not connected":
                raise Exception('The laser is not connected properly')
        else:
            pass

    def check_wavelength(self, comparison=False):
        """

        :param comparison: This is a flag as to whether wavelength values will be compared or not.
        :return:
        """
        if self.status != "not connected" and self.status != "off":
            if self.state != "not connected":
                wavelength_check_msg = '[W0/?]'
                self.serial.write(wavelength_check_msg)
                response = self.serial.read(size=25)
                if response == "":
                   return 0
                logging.info(response)
                if comparison:
                    wavelength = self.parse_wavelength(response)
                    self.wavelength = wavelength
                    return wavelength
                else:
                    wavelength = self.parse_wavelength(response)
                    self.wavelength = wavelength
                    logging.info(wavelength)
            else:
                raise Exception('The laser is not connected properly')
        else:
            self.wavelength = None

    def parse_wavelength(self,msg='[MS:W0/S520\NL]'):
        """

        :param msg: This is the message to parse.
        :return:
        """
        if self.status != "not connected" and self.status != "off":
            msg_parse = msg
            remove_chars = []
            for char in string.letters:
                remove_chars.append(char)
            for char in string.punctuation:
                remove_chars.append(char)
            split_msg = msg_parse.translate(None, ''.join(remove_chars))
            split_msg = split_msg[1:]
            return int(split_msg)
        else:
            pass

    def loop_change_wavelength(self, min, max,diagnostic):
        """

        :param min: The starting wavelength
        :param max: the ending wavelength
        :param diagnostic: whether this loop is going to wait for user input to continue
        :return:
        """
        if self.status != "not connected" and self.status != "not connected":
            np_array = np.arange(min,max+1)
            for item in np_array:
                try:
                    self.change_wavelength(item)
                except Exception as e:
                    logging.exception(e)
                    break
                if not diagnostic:
                    raw_input("Press Enter to continue")
            print("done.")
        else:
            pass


def create_parser():
    parser = argparse.ArgumentParser(description='Program to change the wavelength of the laser using rs232 interface.')
    parser.add_argument('wavelength', nargs=1, help='This is for setting the value of the wavelength of the laser.')
    return parser

def main(wavelength):
    """
    This creates a command line and arguments for the script.

    :return: None
    """

    laser_interface = LaserSerialInterface(loop=False)
    laser_interface.loop_change_wavelength(500, 520, False)
    #laser_interface.change_wavelength(wavelength)

if __name__ == '__main__':
    main(500)
