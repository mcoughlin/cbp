import altaz
import birger
import filter_wheel
import keithley
import lamp
import monochromater
import phidget
import photodiode
import potentiometer
import shutter
import spectrograph
import sr830
import temperature
import laser
import numpy as np
import matplotlib

class CBP:
    def __init__(self):
        self.altaz = altaz.Altaz()
        self.birger = birger.Birger()
        self.filter_wheel = filter_wheel.FilterWheel()
        self.keithley = keithley.Keithley()
        self.lamp = lamp.Lamp()
        self.monochromater = monochromater.Monochromater()
        self.phidget = phidget.CbpPhidget()
        self.photodiode = photodiode.Photodiode()
        self.potentiometer = potentiometer.Potentiometer()
        self.shutter = shutter.Shutter()
        self.spectograph = spectrograph.Spectograph()
        self.sr830 = sr830.Sr830()
        self.temperature = temperature.Temperature()
        self.laser = laser.LaserSerialInterface()

    def keithley_change_wavelength_loop(self, wavelength_min=500, wavelength_max=520):
        data_file = open('data.txt','w')
        wavelength_array = np.arange(wavelength_min,wavelength_max)
        for item in wavelength_array:
            self.laser.change_wavelength(item)
            photo1, photo2 = self.keithley.get_keithley()
            line = "{0} {1} {2}\n".format(item, photo1, photo2)
            data_file.write(line)
        data_file.close()

