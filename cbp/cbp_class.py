import cbp.altaz
import cbp.birger
import cbp.filter_wheel
import cbp.keithley
import cbp.lamp
import cbp.monochromater
import cbp.phidget
import cbp.photodiode
import cbp.potentiometer
import cbp.shutter
import cbp.spectrograph
import cbp.sr830
import cbp.temperature
import cbp.laser
import numpy as np
import thorlabs
import os

import visa

"""
.. module:: cbp_class
    :platform: unix
    :synopsis: This is a module inside of package cbp which is designed to hold the complete cbp instrumentation inside 
    of class CBP.

.. moduleauthor:: Michael Coughlin
"""


class CBP:
    """
    This is the class that contains all of the written cbp instrument modules.
    """
    def __init__(self):
        #self.altaz = altaz.Altaz()
        #self.birger = birger.Birger()
        #self.filter_wheel = filter_wheel.FilterWheel()
        rm = visa.ResourceManager('@py')
        self.keithley = cbp.keithley.Keithley(rm=rm,resnum=0)
        #self.lamp = lamp.Lamp()
        #self.monochromater = monochromater.Monochromater()
        #self.phidget = phidget.CbpPhidget()
        #self.photodiode = photodiode.Photodiode()
        #self.potentiometer = potentiometer.Potentiometer()
        #self.shutter = shutter.Shutter()
        self.spectograph = cbp.spectrograph.Spectograph()
        #self.sr830 = sr830.Sr830()
        #self.temperature = temperature.Temperature()
        self.laser = cbp.laser.LaserSerialInterface(loop=False)

    def keithley_change_wavelength_loop(self, outputDir='data',wavelength_min=500, wavelength_max=700, wavelength_steps=10,Naverages=3):
        """
        Takes an average from reading photodiode and spectograph with both opening and closing the shutter.

        :param outputDir: This is the root directory where files are written
        :param wavelength_min: This is the starting wavelength
        :param wavelength_max: This is the ending wavelength
        :param wavelength_steps: This is the number of steps that are taken at each wavelength change.
        :param Naverages: This is the number of times that the photodiodes are read which is used to calculate an average.
        :return: Ostensibly doesn't return anything, but writes out data files that show average photodiode and
        spectograph readings at each wavelength.
        """

        shutter_closed_directory = '{0}/closed/'.format(outputDir)
        shutter_opened_directory = '{0}/opened/'.format(outputDir)
        if not os.path.exists(shutter_closed_directory):
            os.makedirs(shutter_closed_directory)
        if not os.path.exists(shutter_opened_directory):
            os.makedirs(shutter_opened_directory)

        shutter_closed_file = open(shutter_closed_directory + 'photo.dat', 'w')
        shutter_open_file = open(shutter_opened_directory + 'photo.dat', 'w')
        spectograph_shutter_closed_file = open(shutter_closed_directory + 'specto.dat', 'w')
        spectograph_shutter_opened_file = open(shutter_opened_directory + 'specto.dat', 'w')

        wavelength_array = np.arange(wavelength_min, wavelength_max, wavelength_steps)
        print("created array")
        for wave in wavelength_array:
 
            thorlabs.thorlabs.main(val=2)
            print("shutter closed")
            print("starting change_wavelength")
            self.laser.change_wavelength(wave)
            photo_diode_list = []
            frequencies_list = []
            for i in range(Naverages):
                photo1, photo2 = self.keithley.get_photodiode_reading()
                photo_diode_list.append(photo1)
                wavelength, frequencies = self.spectograph.do_spectograph()
                frequencies_avg = sum(frequencies)/len(frequencies)
                frequencies_list.append(frequencies_avg)

            photo_diode_avg = sum(photo_diode_list)/len(photo_diode_list)
            frequency_avg = sum(frequencies_list)/len(frequencies_list)
            line = "{0} {1}\n".format(wave, photo_diode_avg)
            line_2 = "{0} {1}\n".format(wavelength[0], frequency_avg)
            shutter_closed_file.write(line)
            spectograph_shutter_closed_file.write(line_2)
 

            thorlabs.thorlabs.main(val=1)
            print("shutter opened")
            photo_diode_list = []
            frequencies_list = []
            for i in range(Naverages):
                photo1, photo2 = self.keithley.get_photodiode_reading()
                photo_diode_list.append(photo1)
                wavelength, frequencies = self.spectograph.do_spectograph()
                frequencies_avg = sum(frequencies)/len(frequencies)
                frequencies_list.append(frequencies_avg)
            photo_diode_avg = sum(photo_diode_list) / len(photo_diode_list)
            frequency_avg = sum(frequencies_list) / len(frequencies_list)
            line = "{0} {1}\n".format(wave, photo_diode_avg)
            line_2 = "{0} {1}\n".format(wavelength[0], frequency_avg)
            shutter_open_file.write(line)
            spectograph_shutter_opened_file.write(line_2)
        shutter_closed_file.close()
        shutter_open_file.close()
        spectograph_shutter_closed_file.close()
        spectograph_shutter_opened_file.close()

