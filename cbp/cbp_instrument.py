"""
.. module:: cbp_instrument
    :platform: unix
    :synopsis: This is a module inside of package cbp which is designed to hold the complete cbp instrumentation inside of class CBP.

.. codeauthor:: Michael Coughlin, Eric Coughlin

"""

import cbp.altaz
import cbp.birger
import cbp.filter_wheel
import cbp.keithley
import cbp.lamp
import cbp.monochromater
import cbp.phidget
import cbp.photodiode
import cbp.potentiometer
import cbp.flipper
import cbp.shutter
import cbp.spectrograph
import cbp.lockin
import cbp.temperature
import cbp.laser
import numpy as np
import os
import time
from lxml import etree
if 'TESTENVIRONMENT' in os.environ:
    import sys
    import mock
    sys.modules['thorlabs'] = mock.Mock()
    sys.modules['visa'] = mock.Mock()
else:
    import thorlabs
    import visa


class CBP:
    """
    This is the class that contains all of the written cbp instrument modules.
    """
    def __init__(self,altaz=False,birger=False,filter_wheel=False,keithley=False,keithley_2=False,lamp=False,monochromater=False,phidget=False,photodiode=False,potentiometer=False,shutter=False,flipper=False,spectrograph=False,lockin=False,temperature=False,laser=False,everything=False):
        self.instrument_connected_list = []
        self.instrument_dictionary = {}
        if altaz:
            self.altaz = cbp.altaz.Altaz()
            self.instrument_connected_list.append("altaz")
            self.instrument_dictionary["altaz"] = self.altaz
        if birger:
            self.birger = cbp.birger.Birger()
            self.instrument_connected_list.append("birger")
            self.instrument_dictionary["birger"] = self.birger
        if filter_wheel:
            self.filter_wheel = cbp.filter_wheel.FilterWheel()
            self.instrument_connected_list.append("filter wheel")
            self.instrument_dictionary["filter wheel"] = self.filter_wheel
        rm = visa.ResourceManager('@py')
        if keithley:
            self.keithley = cbp.keithley.Keithley(rm=rm, resnum=0, do_reset=True,mode='char')
            self.instrument_connected_list.append("keithley")
            self.instrument_dictionary["keithley"] = self.keithley
        if keithley_2:
            self.keithley_2 = cbp.keithley.Keithley(rm=rm, resnum=1, do_reset=True,mode='char')
            self.instrument_connected_list.append("keithley_2")
            self.instrument_dictionary["keithley_2"] = self.keithley_2
        if lamp:
            self.lamp = cbp.lamp.Lamp()
            self.instrument_connected_list.append("lamp")
            self.instrument_dictionary["lamp"] = self.lamp
        if monochromater:
            self.monochromater = cbp.monochromater.Monochromater()
            self.instrument_connected_list.append("monochromater")
            self.instrument_dictionary["monochromater"] = self.monochromater
        if phidget:
            self.phidget = cbp.phidget.CbpPhidget()
            self.instrument_connected_list.append("phidget")
            self.instrument_dictionary["phidget"] = self.phidget
        if photodiode:
            self.photodiode = cbp.photodiode.Photodiode()
            self.instrument_connected_list.append("photodiode")
            self.instrument_dictionary["photodiode"] = self.photodiode
        if potentiometer:
            self.potentiometer = cbp.potentiometer.Potentiometer()
            self.instrument_connected_list.append("potentiometer")
            self.instrument_dictionary["potentiometer"] = self.potentiometer
        if shutter:
            self.shutter = cbp.shutter.Shutter()
            self.instrument_connected_list.append("shutter")
            self.instrument_dictionary["shutter"] = self.shutter
        if flipper:
            self.flipper = cbp.flipper.Flipper()
            self.instrument_connected_list.append("flipper")
            self.instrument_dictionary["flipper"] = self.flipper
        if spectrograph:
            self.spectrograph = cbp.spectrograph.Spectrograph()
            self.instrument_connected_list.append("spectrograph")
            self.instrument_dictionary["spectrograph"] = self.spectrograph
        if lockin:
            self.lockin = cbp.lockin.LockIn(rm=rm)
            self.instrument_connected_list.append("lockin")
            self.instrument_dictionary["lockin"] = self.lockin
        if temperature:
            self.temperature = cbp.temperature.Temperature()
            self.instrument_connected_list.append("temperature")
            self.instrument_dictionary["temperature"] = self.temperature
        if laser:
            self.laser = cbp.laser.LaserSerialInterface(loop=False)
            self.instrument_connected_list.append("laser")
            self.instrument_dictionary["laser"] = self.laser
        if everything:
            self.altaz = cbp.altaz.Altaz()
            self.birger = cbp.birger.Birger()
            self.filter_wheel = cbp.filter_wheel.FilterWheel()
            rm = visa.ResourceManager('@py')
            self.keithley = cbp.keithley.Keithley(rm=rm, resnum=0, do_reset=True)
            self.phidget = cbp.phidget.CbpPhidget()
            if self.phidget.status == "connected":
                self.altaz.status = "connected"
            self.potentiometer = cbp.potentiometer.Potentiometer()
            self.spectrograph = cbp.spectrograph.Spectrograph()
            self.lockin = cbp.lockin.LockIn(rm=rm)
            self.temperature = cbp.temperature.Temperature()
            self.laser = cbp.laser.LaserSerialInterface(loop=False)
            self.lamp = cbp.lamp.Lamp()
            for instrument in ["altaz","birger","filter wheel","keithley","phidget","potentiometer","shutter","spectrograph","lockin","temperature","laser","lamp"]:
                self.instrument_connected_list.append(instrument)
                if instrument == "altaz":
                    self.instrument_dictionary[instrument] = self.altaz
                if instrument == "birger":
                    self.instrument_dictionary[instrument] = self.birger
                if instrument == "filter wheel":
                    self.instrument_dictionary[instrument] = self.filter_wheel
                if instrument == "keithley":
                    self.instrument_dictionary[instrument] = self.keithley
                if instrument == "phidget":
                    self.instrument_dictionary[instrument] = self.phidget
                if instrument == "potentiometer":
                    self.instrument_dictionary[instrument] = self.potentiometer
                if instrument == "spectrograph":
                    self.instrument_dictionary[instrument] = self.spectrograph
                if instrument == "lockin":
                    self.instrument_dictionary[instrument] = self.lockin
                if instrument == "temperature":
                    self.instrument_dictionary[instrument] = self.temperature
                if instrument == "laser":
                    self.instrument_dictionary[instrument] = self.laser
                if instrument == "lamp":
                    self.instrument_dictionary[instrument] = self.lamp

    def check_status(self):
        """
        This methods calls the check status of each instrument.

        :return:
        """
        self.birger.check_status()
        self.filter_wheel.check_status()
        self.keithley.check_status()
        self.phidget.check_status()
        if self.phidget.status == "connected":
            self.altaz.status = "connected"
        self.potentiometer.check_status()
        self.shutter.check_status()
        self.lockin.check_status()
        self.temperature.check_status()
        self.laser.check_state()

    def keithley_change_wavelength(self, output_dir='data', wavelength = 600, n_averages=1, duration=1000000):
        """
        Takes an average from reading photodiode and spectograph with both opening and closing the shutter.

        :param output_dir: This is the root directory where files are written
        :param wavelength: This is the wavelength
        :param n_averages: This is the number of times that the photodiodes are read which is used to calculate an average.
        :param duration: This is the length of time that the spectrograph will sleep for per reading.
        :return: Ostensibly doesn't return anything, but writes out data files that show average photodiode and spectograph readings at each wavelength.

        """

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        shutter_file = open(output_dir + '/photo.dat', 'w')
        spectograph_file = open(output_dir + '/specto.dat', 'w')

        print("starting change_wavelength")
        self.laser.change_wavelength(wavelength)

        self._get_photodiode_spectograph_averages(2, wave=wave, n_averages=n_averages, shutter_closed_file=shutter_closed_file, spectograph_shutter_closed_file=spectograph_shutter_closed_file, shutter_open_file=shutter_opened_file, spectograph_shutter_opened_file=spectograph_shutter_opened_file, duration=duration)

        spectograph_file.close()
        shutter_file.close()

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

            print("starting change_wavelength")
            self.laser.change_wavelength(wave)

            self._get_photodiode_spectograph_averages(2, wave=wave, n_averages=n_averages, shutter_closed_file=shutter_closed_file, spectograph_shutter_closed_file=spectograph_shutter_closed_file, shutter_open_file=shutter_opened_file, spectograph_shutter_opened_file=spectograph_shutter_opened_file, duration=duration)
            self._get_photodiode_spectograph_averages(1, wave=wave, n_averages=n_averages, shutter_closed_file=shutter_closed_file, spectograph_shutter_closed_file=spectograph_shutter_closed_file, shutter_open_file=shutter_opened_file, spectograph_shutter_opened_file=spectograph_shutter_opened_file, duration=duration)
        
            spectograph_shutter_opened_file.close()
            spectograph_shutter_closed_file.close()
        shutter_closed_file.close()
        shutter_opened_file.close()

    def both_keithley_change_wavelength(self,output_dir='data', wavelength_min=500, wavelength_max=700, wavelength_steps=10, n_averages=3):
        shutter_closed_directory = '{0}/closed/'.format(output_dir)
        shutter_opened_directory = '{0}/opened/'.format(output_dir)
        if not os.path.exists(shutter_closed_directory):
            os.makedirs(shutter_closed_directory)
        if not os.path.exists(shutter_opened_directory):
            os.makedirs(shutter_opened_directory)

        shutter_closed_file = open(shutter_closed_directory + 'photo.dat', 'w')
        shutter_opened_file = open(shutter_opened_directory + 'photo.dat', 'w')
        wavelength_array = np.arange(wavelength_min, wavelength_max + wavelength_steps, wavelength_steps)
        print("created array")
        for wave in wavelength_array:
            print("starting change_wavelength")
            self.laser.change_wavelength(wave)
            print(self.laser.wavelength)
            self._get_photodiode_averages(2,wave=wave,n_averages=n_averages,shutter_closed_file=shutter_closed_file,shutter_open_file=shutter_opened_file)
        shutter_opened_file.close()
        shutter_closed_file.close()

    def _get_photodiode_averages(self, shutter_position, wave, n_averages, shutter_closed_file, shutter_open_file):
        photodiode_list = []
        photodiode_2_list = []
        for i in range(n_averages + 1):
            retry = 0
            retry_2 = 0
            while retry <= 10:
                try:
                    photo1 = self.keithley.get_photodiode_reading()
                    break
                except Exception as e:
                    print(e)
                    retry += 1
            if retry > 10:
                raise Exception('Keithley failed to read in the alloted number of retries')
            while retry_2 <= 10:
                try:
                    photo2 = self.keithley_2.get_photodiode_reading()
                    break
                except Exception as e:
                    print(e)
                    retry_2 += 1
            if retry_2 > 10:
                raise Exception('Keithley 2 failed to read in the alloted numberof retries')

            photodiode_list.append(photo1)
            photodiode_2_list.append(photo2)
        photodiode_avg = np.mean(photodiode_list)
        photodiode_std = np.std(photodiode_list)
        photodiode_2_avg = np.mean(photodiode_2_list)
        photodiode_2_std = np.std(photodiode_2_list)
        line = "{0} {1} {2}\n".format(wave, photodiode_avg, photodiode_std)
        line_2 = "{0} {1} {2}\n".format(wave, photodiode_2_avg, photodiode_2_std)
        shutter_closed_file.write(line)
        shutter_open_file.write(line_2)

    def _get_photodiode_spectograph_averages(self, shutter_position, wave, n_averages, shutter_closed_file, spectograph_shutter_closed_file, shutter_open_file, spectograph_shutter_opened_file, duration):
        thorlabs.thorlabs.main(val=shutter_position)
        if shutter_position == 2:
            print("shutter closed")
        elif shutter_position == 1:
            print("shutter open")
        photodiode_list = []
        for i in range(n_averages + 1):
            self.keithley.do_reset()
            retry = 0
            while retry <= 10:
                try:
                    photo1, photo2 = self.keithley.get_photodiode_reading()
                    print photo1, photo2
                    break
                except Exception as e:
                    print(e)
                    retry += 1
            if retry > 10:
                raise Exception('Keithley failed to read in the alloted number of retries')

            photodiode_list.append(photo1)
            wavelength, intensity = self._add_spectra(duration=duration)
 
            print(photo1)

            if i == 0:
                pass
            elif i == 1:
                intensity_list = intensity
            else:
                intensity_list = np.vstack((intensity_list, intensity))
        photodiode_avg = np.mean(photodiode_list)
        photodiode_std = np.std(photodiode_list)

        intensity_avg = np.mean(intensity_list, axis=0)
        intensity_std = np.std(intensity_list, axis=0)

        line = "{0} {1} {2}\n".format(wave, photodiode_avg, photodiode_std)
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

    def get_spectograph_average(self, output_dir='/home/pi/CBP/keithley/', n_averages=3, duration=1000000, dark=False):
        """
        This method calculates the spectrograph average and writes out the results to files.

        :param output_dir: This is the output directory of where the spectrograph file goes.
        :param n_averages: This is the number of averages for the spectrograph
        :param duration: This is the amount of time in microseconds that the spectrograph will measure light
        :param dark: This is a flag that specifies whether the light source is on or off.
        :return:
        """
        if not os.path.exists(output_dir):
           os.makedirs(output_dir)
        if dark:
           spectograph_file = open(output_dir + 'specto_{0}_{1}_dark.dat'.format(duration, n_averages), 'w')
        else:
            spectograph_file = open(output_dir + 'specto_{0}_{1}_light.dat'.format(duration, n_averages), 'w')
        self.spectrograph.spectrometer.tec_set_enable(True)
        for i in range(n_averages + 1):
            wavelength, intensity = self._add_spectra(duration=duration)
            if i == 0:
                pass
            elif i == 1:
                intensity_list = intensity
            else:
                intensity_list = np.vstack((intensity_list,intensity))

        intensity_avg = np.mean(intensity_list,axis=0)
        intensity_std = np.std(intensity_list,axis=0)

        for i in xrange(len(wavelength)):
            line = "{0} {1} {2}\n".format(wavelength[i],intensity_avg[i],intensity_std[i])
            spectograph_file.write(line)
        spectograph_file.close()
        self.spectrograph.spectrometer.tec_set_enable(False)

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
            wavelength, intensity = self.spectrograph.get_spectograph(duration=duration)
            return wavelength, intensity

    def write_status_log(self,output_dir='/home/pi/CBP/status_logs/',duration=1):
        """

        :param output_dir: This is where the status log will be written to.
        :param duration: This is the length of the measuring of the light by the spectropgraph.
        :return:
        """
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
        keithley_status = self.keithley.get_charge_timeseries(cbp_inst=self)
        spectrograph_status = self.spectrograph.do_spectograph(duration=duration*1e6)
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

    def write_status_log_xml(self,outfile='/tmp/test.xml',duration=1,doShutter=True):
        """
        This method writes out the status log file but in xml format.

        :param output_dir: This is where the status log will be written to.
        :param duration: This is the length of the measuring of the light by the spectropgraph.
        :return:
        """

        try:
            x, y, z, angle = self.phidget.do_phidget()
        except:
            x, y, z, angle = 0.0, 0.0, 0.0, 0.0
 
        try:
            potentiometer1, potentiometer2 = self.potentiometer.get_potentiometer()
        except:
            potentiometer1, potentiometer2 = 0.0, 0.0
        
        try:
            mask, filter = self.filter_wheel.get_position()
        except:
            mask, filter = 0.0, 0.0

        try:
            birger_status = self.birger.do_status()
        except:
            birger_status = [0.0,0.0]

        try:
            wavelength = self.laser.check_wavelength()
        except:
            wavelength = 0.0

        keithley_status = self.keithley.get_charge_timeseries(duration=duration,doShutter=doShutter, cbp_inst=self)
        #spectrograph_status = self.spectrograph.do_spectrograph(duration=duration*1e3,doShutter=doShutter)
        time.sleep(10.0)

        #spectrograph_status = self.spectrograph.do_spectrograph(duration=1e7,doShutter=doShutter, cbp_inst=self)

        #spectrograph_status = self.spectrograph.do_spectrograph(duration=8000,doShutter=doShutter, cbp_inst=self)
        spectrograph_status = []
        spectrograph_status.append([0])
        spectrograph_status.append([0])
        status_log_file = open(outfile, 'w')
        root = etree.Element('log')
        instrument_status = etree.SubElement(root,'instrument_status',x=str(x),y=str(y),z=str(z),angle=str(angle),potentiometer_1=str(potentiometer1),potentiometer_2=str(potentiometer2),mask=str(mask),filter=str(filter),focus=str(birger_status[0]),aperture=str(birger_status[1]),wavelength=str(wavelength))
        keithley = etree.SubElement(root,'keithley')
        for t, current in zip(keithley_status[0], keithley_status[1]):
            keithley_element = etree.SubElement(keithley,'keithley_element',time=str(t),current=str(current))
        spectrograph = etree.SubElement(root,'spectrograph')
        for wavelength, intensity in zip(spectrograph_status[0], spectrograph_status[1]):
            spectrograph_element = etree.SubElement(spectrograph,'spectrum',wavelength=str(wavelength),intensity=str(intensity))
        et = etree.ElementTree(root)
        et.write(status_log_file,pretty_print=True, xml_declaration=True, encoding='utf-8')

    def load_status_log_xml(self,status_log_file):
        """
        This is a method to load the status log xml file

        :param status_log_file: This is location of the status log file to load.
        :return:
        """
        status_log_file = status_log_file
        et = etree.parse(status_log_file)
        root = et.getroot()
        instrument_status_dictionary = {}
        times_list = []
        current_list = []
        intensity_array = np.array([])
        wavelength_array = np.array([])
        for child in root:
            if child.tag == "instrument_status":
                instrument_status_dictionary['angle'] = float(child.attrib['angle'])
                instrument_status_dictionary['potentiometer_1'] = float(child.attrib['potentiometer_1'])
                instrument_status_dictionary['potentiometer_2'] = float(child.attrib['potentiometer_2'])
                instrument_status_dictionary['mask'] = int(child.attrib['mask'])
                instrument_status_dictionary['focus'] = float(child.attrib['focus'])
                instrument_status_dictionary['filter'] = int(child.attrib['filter'])
                instrument_status_dictionary['aperture'] = int(child.attrib['aperture'])
                instrument_status_dictionary['wavelength'] = int(child.attrib['wavelength'])
                instrument_status_dictionary['y'] = float(child.attrib['y'])
                instrument_status_dictionary['x'] = float(child.attrib['x'])
                instrument_status_dictionary['z'] = float(child.attrib['z'])
            elif child.tag == "keithley":
                for grandchild in child:
                    current_list.append(float(grandchild.attrib['current']))
                    times_list.append(float(grandchild.attrib['time']))
            elif child.tag == "spectrograph":
                for grandchild in child:
                    intensity_array = np.append(intensity_array, float(grandchild.attrib['intensity']))
                    wavelength_array = np.append(wavelength_array, float(grandchild.attrib['wavelength']))

        return instrument_status_dictionary, current_list, times_list, intensity_array, wavelength_array


if __name__ == '__main__':
    pass
