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
import cbp.lockin
import cbp.temperature
import cbp.laser
import numpy as np
import thorlabs
import os
import time

import visa

"""
.. module:: cbp_class
    :platform: unix
    :synopsis: This is a module inside of package cbp which is designed to hold the complete cbp instrumentation inside of class CBP.

.. moduleauthor:: Michael Coughlin, Eric Coughlin
"""


class CBP:
    """
    This is the class that contains all of the written cbp instrument modules.
    """
    def __init__(self,altaz=False,birger=False,filter_wheel=False,keithley=False,lamp=False,monochromater=False,phidget=False,photodiode=False,potentiometer=False,shutter=False,spectrograph=False,lockin=False,temperature=False,laser=False,everything=False):
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
        if spectrograph:
            self.spectograph = cbp.spectrograph.Spectrograph()
        if lockin:
            self.lockin = cbp.lockin.LockIn(rm=rm)
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
            self.monochromater = cbp.monochromater.Monochromater()
            self.phidget = cbp.phidget.CbpPhidget()
            if self.phidget.status == "connected":
                self.altaz.status = "connected"
            self.potentiometer = cbp.potentiometer.Potentiometer()
            self.shutter = cbp.shutter.Shutter()
            self.spectrograph = cbp.spectrograph.Spectrograph()
            self.lockin = cbp.lockin.LockIn(rm=rm)
            self.temperature = cbp.temperature.Temperature()
            self.laser = cbp.laser.LaserSerialInterface(loop=False)


    def keithley_change_wavelength_loop(self, output_dir='data', wavelength_min=500, wavelength_max=700, wavelength_steps=10, n_averages=3, duration=1000000):
        """
        Takes an average from reading photodiode and spectograph with both opening and closing the shutter.

        :param output_dir: This is the root directory where files are written
        :param wavelength_min: This is the starting wavelength
        :param wavelength_max: This is the ending wavelength
        :param wavelength_steps: This is the number of steps that are taken at each wavelength change.
        :param n_averages: This is the number of times that the photodiodes are read which is used to calculate an average.
        :param duration: This is the length of time that the spectrograph will sleep for per reading.
        :return: Ostensibly doesn't return anything, but writes out data files that show average photodiode and spectograph readings at each wavelength.

        """

        shutter_closed_directory = '{0}/closed/'.format(output_dir)
        shutter_opened_directory = '{0}/opened/'.format(output_dir)
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

            self.get_photodiode_spectograph_averages(2, wave=wave, n_averages=n_averages, shutter_closed_file=shutter_closed_file, spectograph_shutter_closed_file=spectograph_shutter_closed_file, shutter_open_file=shutter_opened_file, spectograph_shutter_opened_file=spectograph_shutter_opened_file, duration=duration)
            self.get_photodiode_spectograph_averages(2, wave=wave, n_averages=n_averages, shutter_closed_file=shutter_closed_file, spectograph_shutter_closed_file=spectograph_shutter_closed_file, shutter_open_file=shutter_opened_file, spectograph_shutter_opened_file=spectograph_shutter_opened_file, duration=duration)

        shutter_closed_file.close()
        shutter_opened_file.close()

    def get_photodiode_spectograph_averages(self, shutter_position, wave, n_averages, shutter_closed_file, spectograph_shutter_closed_file, shutter_open_file, spectograph_shutter_opened_file, duration):
        thorlabs.thorlabs.main(val=shutter_position)
        if shutter_position == 2:
            print("shutter closed")
        elif shutter_position == 1:
            print("shutter open")
        print("starting change_wavelength")
        self.laser.change_wavelength(wave)
        photodiode_list = []
        for i in range(n_averages):
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

    def get_spectograph_average(self, output_dir='/home/pi/CBP/keithley/', n_averages=3, duration=1000000, dark=False):
        if not os.path.exists(output_dir):
           os.makedirs(output_dir)
        if dark:
           spectograph_file = open(output_dir + 'specto_{0}_{1}_dark.dat'.format(duration, n_averages), 'w')
        else:
            spectograph_file = open(output_dir + 'specto_{0}_{1}_light.dat'.format(duration, n_averages), 'w')
        for i in range(n_averages):
            wavelength, intensity = self._add_spectra(duration=duration)

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

    def _add_spectra(self,duration):
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
                wavelength, intensity = self.spectrograph.get_spectograph(duration=time)
                if i == 0:
                    intensity_list = intensity
                else:
                    intensity_list = np.vstack((intensity_list, intensity))
            intensity_list_added = np.sum(intensity_list,axis=0)
            return wavelength, intensity_list_added
        else:
            wavelength, intensity = self.spectograph.get_spectograph(duration=duration)
            return wavelength, intensity

    def write_status_log(self,output_dir='/home/pi/CBP/status_logs/',duration=1000000):
        date_at_run = time.strftime("%m_%d_%Y")
        time_at_run = time.strftime("%m_%d_%Y_%H_%M")
        if not os.path.exists(output_dir + '{0}/{1}/keithley/'.format(date_at_run,time_at_run)):
            os.makedirs(output_dir + '{0}/{1}/keithley/'.format(date_at_run,time_at_run))
        if not os.path.exists(output_dir + '{0}/{1}/spectrograph/'.format(date_at_run,time_at_run)):
            os.makedirs(output_dir + '{0}/{1}/spectrograph/'.format(date_at_run,time_at_run))
        status_directory = output_dir + '{0}/{1}/'.format(date_at_run,time_at_run)
        keithley_directory = status_directory + 'keithley/'
        spectrograph_directory = status_directory + 'spectrograph/'
        x,y,z,angle = self.phidget.do_phidget()
        potentiometer1, potentiometer2 = self.potentiometer.get_potentiometer()
        mask, filter = self.filter_wheel.get_position()
        birger_status = self.birger.do_status()
        keithley_status = self.keithley.get_charge_timeseries()
        spectrograph_status = self.spectrograph.do_spectograph(duration=duration)
        status_log_file = open(status_directory + '{0}_status.dat'.format(time_at_run), 'w')
        headings_line = "{0:5} {1:5} {2:5} {3:5} {4:5} {5:5} {6:5} {7:5} {8:5} {9:5}\n".format("X", "Y", "Z", "ANGLE","POTENTIOMETER 1", "POTENTIOMETER 2", "MASK", "FILTER", "WAVELENGTH", "INTENSITIES")
        status_log_file.write(headings_line)
        data_line = "{0:5} {1:5} {2:5} {3:5} {4:5} {5:5} {6:5} {7:5} {8:5} {9:5}\n".format(x,y,z,angle,potentiometer1,potentiometer2,mask,filter,birger_status[0], birger_status[1])
        status_log_file.write(data_line)
        status_log_file.close()
        status_keithley_log_file = open(keithley_directory + '{0}_keithley_status.dat'.format(time_at_run),'w')
        keithley_headings_line = "{0:5} {1:5}\n".format("TIME", "PHOTODIODE CURRENT")
        status_keithley_log_file.write(keithley_headings_line)
        for things, stuff in zip(keithley_status[0], keithley_status[1]):
            keithley_data_line = "{0:5} {1:5}\n".format(things, stuff)
            status_keithley_log_file.write(keithley_data_line)
        status_keithley_log_file.close()
        status_spectrograph_log_file = open(spectrograph_directory + '{0}_spectrograph_status'.format(time_at_run),'w')
        spectrograph_headings_line = "{0:5} {1:5}\n".format("WAVELENGTH", "INTENSITY")
        status_spectrograph_log_file.write(spectrograph_headings_line)
        for wavelength, intensity in zip(spectrograph_status[0], spectrograph_status[1]):
            spectrograph_data_line = "{0:5} {1:5}\n".format(wavelength, intensity)
            status_spectrograph_log_file.write(spectrograph_data_line)
        status_spectrograph_log_file.close()

if __name__ == '__main__':
    pass
