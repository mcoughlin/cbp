"""
This is a module that communicates with the ESKPLA laser in the lab via RS232 port.
"""

import serial
import argparse
import string
import numpy as np


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
            except Exception as e:
                print(e)
                self.status = "not connected"
                self.state = "not connected"

    def test_state(self):
        """
        This is a method for testing the state of the laser in a loop-back environment.

        :return:
        """
        responses = ['[PC:OFF=0\NL]', '[PC:BUSY=0\NL]', '[PC:BUSY=0\NL]', '[PC:READY=0\NL]']
        for response in responses:
            say_state_msg = self.commands['say_state_msg']
            self.serial.write(say_state_msg)
            if response in self.states:
                self.state = self.states[response][0]
                print(self.states[response][1])

    def check_state(self):
        """
        This method checks the status of the laser and then sets the state of the laser inside of the class.

        :return:
        """
        say_state_msg = self.commands['say_state_msg']
        self.serial.write(say_state_msg)
        response = self.serial.read(size=25)
        if response == "":
            self.state = "off"
            self.status = "off"
            print("The laser is off")
            return 
        if response in self.states:
            self.state = self.states[response][0]
            print(self.states[response][1])
        else:
            print("Not found.")

    def get_ready_state(self):
        """
        This method calls the :py:meth:`check_state` until a ready state is set by the class.

        :return:
        """
        while self.state != 'ready' and self.state != 'off' and self.state != 'not connected':
            print("checking state...")
            self.check_state()

    def change_wavelength(self, wavelength):
        """
        This method changes the wavelength of the laser.

        :param wavelength: This is the value of the wavelength to be set. Units are in nanometers and limits are 355nm to 2300 nm.

        :return:

        """
        self.get_ready_state()
        if self.state != "off" and self.state != "not connected":
            wavelength_change_msg = '[W0/S{0}]'.format(str(wavelength))
            self.serial.write(wavelength_change_msg)
            check_response = self.check_wavelength(comparison=True)
            if int(wavelength) == check_response:
                print("Wavelength set correctly")
            else:
                print("Something went wrong")
        elif self.state == "off":
            raise Exception('The laser is turned off')
        elif self.state == "not connected":
            raise Exception('The laser is not connected properly')

    def check_wavelength(self, comparison=False):
        if self.state != "not connected":
            wavelength_check_msg = '[W0/?]'
            self.serial.write(wavelength_check_msg)
            response = self.serial.read(size=25)
            if response == "":
               return 0
            print(response)
            if comparison:
                wavelength = self.parse_wavelength(response)
                return wavelength
            else:
                wavelength = self.parse_wavelength(response)
                print(wavelength)
        else:
            raise Exception('The laser is not connected properly')

    @staticmethod
    def parse_wavelength(msg='[MS:W0/S520\NL]'):
        msg_parse = msg
        remove_chars = []
        for char in string.letters:
            remove_chars.append(char)
        for char in string.punctuation:
            remove_chars.append(char)
        split_msg = msg_parse.translate(None, ''.join(remove_chars))
        split_msg = split_msg[1:]
        return int(split_msg)

    def loop_change_wavelength(self, min, max,diagnostic):
            np_array = np.arange(min,max+1)
            for item in np_array:
                try:
                    self.change_wavelength(item)
                except Exception as e:
                    print(e)
                    break
                if not diagnostic:
                    raw_input("Press Enter to continue")
            print("done.")


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
