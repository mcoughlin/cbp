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

class CBP:
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
        #self.spectograph = spectrograph.Spectograph()
        #self.sr830 = sr830.Sr830()
        #self.temperature = temperature.Temperature()
        self.laser = cbp.laser.LaserSerialInterface(loop=False)

    def keithley_change_wavelength_loop(self, outputDir='data',wavelength_min=500, wavelength_max=700, wavelength_steps=10,Naverages=3):

        shutter_closed_directory = '%s/closed/'%outputDir
        shutter_opened_directory = '%s/opened/'%outputDir
        if not os.path.exists(shutter_closed_directory):
            os.makedirs(shutter_closed_directory)
        if not os.path.exists(shutter_opened_directory):
            os.makedirs(shutter_opened_directory)

        shutter_closed_file = open(shutter_closed_directory + 'photo.dat', 'w')
        shutter_open_file = open(shutter_opened_directory + 'photo.dat', 'w')

        wavelength_array = np.arange(wavelength_min, wavelength_max, wavelength_steps)
        print("created array")
        for wave in wavelength_array:
 
            thorlabs.thorlabs.main(val=2)
            print("shutter closed")
            print("starting change_wavelength")
            self.laser.change_wavelength(wave)
            photo_diode_list = []
            for i in range(Naverages):
                photo1, photo2 = self.keithley.get_photodiode_reading()
                photo_diode_list.append(photo1)
            photo_diode_avg = sum(photo_diode_list)/len(photo_diode_list)
            line = "{0} {1}\n".format(wave, photo_diode_avg)
            shutter_closed_file.write(line)
 

            thorlabs.thorlabs.main(val=1)
            print("shutter opened")
            photo_diode_list = []
            for i in range(10):
                photo1, photo2 = self.keithley.get_photodiode_reading()
                photo_diode_list.append(photo1)
            photo_diode_avg = sum(photo_diode_list) / len(photo_diode_list)
            line = "{0} {1}\n".format(wave, photo_diode_avg)
            shutter_open_file.write(line)
        shutter_closed_file.close()
        shutter_open_file.close()

