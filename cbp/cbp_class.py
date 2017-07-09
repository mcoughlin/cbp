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
    :synopsis: This is a module inside of package cbp which is designed to hold the complete cbp instrumentation inside of class CBP.

.. moduleauthor:: Michael Coughlin
"""


class CBP:
    """
    This is the class that contains all of the written cbp instrument modules.
    """
    def __init__(self,altaz=False,birger=False,filter_wheel=False,keithley=False,lamp=False,monochromater=False,phidget=False,photodiode=False,potentiometer=False,shutter=False,spectograph=False,sr830=False,temperature=False,laser=False,everything=False):
        if altaz:
            self.altaz = cbp.altaz.Altaz()
        if birger:
            self.birger = cbp.birger.Birger()
        if filter_wheel:
            self.filter_wheel = cbp.filter_wheel.FilterWheel()
        rm = visa.ResourceManager('@py')
        if keithley:
            self.keithley = cbp.keithley.Keithley(rm=rm,resnum=0)
        if lamp:
            self.lamp = cbp.lamp.Lamp()
        if monochromater:
            self.monochromater = cbp.monochromater.Monochromater()
        if phidget:
            self.phidget = cbp.phidget.CbpPhidget()
        if photodiode:
            self.photodiode = cbp.photodiode.Photodiode()
        if potentiometer:
            self.potentiometer = cbp.potentiometer.Potentiometer()
        if shutter:
            self.shutter = cbp.shutter.Shutter()
        if spectograph:
            self.spectograph = cbp.spectrograph.Spectograph()
        if sr830:
            self.sr830 = cbp.sr830.SR830(rm=rm)
        if temperature:
            self.temperature = cbp.temperature.Temperature()
        if laser:
            self.laser = cbp.laser.LaserSerialInterface(loop=False)
        if everything:
            self.altaz = cbp.altaz.Altaz()
            self.birger = cbp.birger.Birger()
            self.filter_wheel = cbp.filter_wheel.FilterWheel()
            rm = visa.ResourceManager('@py')
            self.keithley = cbp.keithley.Keithley(rm=rm, resnum=0)
            self.lamp = cbp.lamp.Lamp()
            self.monochromater = cbp.monochromater.Monochromater()
            self.phidget = cbp.phidget.CbpPhidget()
            self.photodiode = cbp.photodiode.Photodiode()
            self.potentiometer = cbp.potentiometer.Potentiometer()
            self.shutter = cbp.shutter.Shutter()
            self.spectograph = cbp.spectrograph.Spectograph()
            self.sr830 = cbp.sr830.SR830(rm=rm)
            self.temperature = cbp.temperature.Temperature()
            self.laser = cbp.laser.LaserSerialInterface(loop=False)


    def keithley_change_wavelength_loop(self, outputDir='data',wavelength_min=500, wavelength_max=700, wavelength_steps=10,Naverages=3,duration=1000000):
        """
        Takes an average from reading photodiode and spectograph with both opening and closing the shutter.

        :param outputDir: This is the root directory where files are written
        :param wavelength_min: This is the starting wavelength
        :param wavelength_max: This is the ending wavelength
        :param wavelength_steps: This is the number of steps that are taken at each wavelength change.
        :param Naverages: This is the number of times that the photodiodes are read which is used to calculate an average.
        :return: Ostensibly doesn't return anything, but writes out data files that show average photodiode and spectograph readings at each wavelength.

        """

        shutter_closed_directory = '{0}/closed/'.format(outputDir)
        shutter_opened_directory = '{0}/opened/'.format(outputDir)
        if not os.path.exists(shutter_closed_directory):
            os.makedirs(shutter_closed_directory)
        if not os.path.exists(shutter_opened_directory):
            os.makedirs(shutter_opened_directory)

        shutter_closed_file = open(shutter_closed_directory + 'photo.dat', 'w')
        shutter_opened_file = open(shutter_opened_directory + 'photo.dat', 'w')

        wavelength_array = np.arange(wavelength_min, wavelength_max+wavelength_steps, wavelength_steps)
        print("created array")
        for wave in wavelength_array:

            spectograph_shutter_closed_file = open(shutter_closed_directory + 'specto_%.0f.dat'%wave, 'w')
            spectograph_shutter_opened_file = open(shutter_opened_directory + 'specto_%.0f.dat'%wave, 'w')

            self.get_photodiode_spectograph_averages(2,wave=wave,Naverages=Naverages,shutter_closed_file=shutter_closed_file,spectograph_shutter_closed_file=spectograph_shutter_closed_file,shutter_open_file=shutter_opened_file,spectograph_shutter_opened_file=spectograph_shutter_opened_file,duration=duration)
            self.get_photodiode_spectograph_averages(2, wave=wave, Naverages=Naverages,shutter_closed_file=shutter_closed_file,spectograph_shutter_closed_file=spectograph_shutter_closed_file,shutter_open_file=shutter_opened_file,spectograph_shutter_opened_file=spectograph_shutter_opened_file,duration=duration)

        shutter_closed_file.close()
        shutter_opened_file.close()

    def get_photodiode_spectograph_averages(self,shutter_position,wave,Naverages, shutter_closed_file,spectograph_shutter_closed_file,shutter_open_file, spectograph_shutter_opened_file,duration):
        thorlabs.thorlabs.main(val=shutter_position)
        if shutter_position == 2:
            print("shutter closed")
        elif shutter_position == 1:
            print("shutter open")
        print("starting change_wavelength")
        self.laser.change_wavelength(wave)
        photodiode_list = []
        for i in range(Naverages):
            photo1, photo2 = self.keithley.get_photodiode_reading()
            photodiode_list.append(photo1)
            wavelength, intensity = self.spectograph.do_spectograph(duration=duration)

            if i == 0:
                intensity_list = intensity
            else:
                intensity_list = np.vstack((intensity_list, intensity))
        photodiode_avg = np.mean(photodiode_list)
        photodiode_std = np.std(photodiode_list)

        intensity_avg = np.mean(intensity_list, axis=0)
        intensity_std = np.std(intensity_list, axis=0)

        line = "{0} {1} {2}\n".format(wave, photodiode_avg, photodiode_std)
        spectograph_shutter_closed_file.write(line)
        if shutter_position == 2:
            shutter_closed_file.write(line)
            for i in xrange(len(wavelength)):
                line = "{0} {1} {2}\n".format(wavelength[i],intensity_avg[i],intensity_std[i])
                spectograph_shutter_closed_file.write(line)
        elif shutter_position == 1:
            shutter_open_file.write(line)
            for i in xrange(len(wavelength)):
                line = "{0} {1} {2}\n".format(wavelength[i],intensity_avg[i],intensity_std[i])
                spectograph_shutter_opened_file.write(line)
        spectograph_shutter_opened_file.close()
        spectograph_shutter_closed_file.close()

    def get_spectograph_average(self,output_dir='/home/pi/CBP/keithley/',Naverages=3, duration=1000000,dark=False):
        if not os.path.exists(output_dir):
           os.makedirs(output_dir)
        if dark:
           spectograph_file = open(output_dir + 'specto_{0}_dark.dat'.format(duration),'w')
        else:
            spectograph_file = open(output_dir + 'specto_{0}_light.dat'.format(duration),'w')
        for i in range(Naverages):
            wavelength, intensity = self.add_spectra(duration=duration)

            if i == 0:
                intensity_list = intensity
            else:
                intensity_list = np.vstack((intensity_list,intensity))

        intensity_avg = np.mean(intensity_list,axis=0)
        intensity_std = np.std(intensity_list,axis=0)

        for i in xrange(len(wavelength)):
            line = "{0} {1} {2}\n".format(wavelength[i],intensity_avg[i],intensity_std[i])
            spectograph_file.write(line)
        spectograph_file.close()

    def add_spectra(self,duration):
        if duration > 60000000:
            duration_in_seconds = duration * (1*10**-6)
            number_of_times = float(duration_in_seconds)/60
            list_of_times = []
            while number_of_times != 0:
                if not number_of_times < 1:
                    number_of_times -= 1
                    list_of_times.append(60*(1*10**6))
                else:
                    list_of_times.append(int((number_of_times * 60)*(1*10**6)))
                    break

            for i,time in enumerate(list_of_times):
                wavelength, intensity = self.spectograph.get_spectograph(duration=time)
                if i == 0:
                    intensity_list = intensity
                else:
                    intensity_list = np.vstack((intensity_list, intensity))
            intensity_list_added = np.sum(intensity_list,axis=0)
            return wavelength, intensity_list_added
        else:
            wavelength, intensity = self.spectograph.get_spectograph(duration=duration)
            return wavelength, intensity

