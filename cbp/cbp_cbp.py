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

class CBP:
    def __init__(self):
        #self.altaz = altaz.Altaz()
        #self.birger = birger.Birger()
        #self.filter_wheel = filter_wheel.FilterWheel()
        self.keithley = keithley.Keithley()
        #self.lamp = lamp.Lamp()
        #self.monochromater = monochromater.Monochromater()
        #self.phidget = phidget.CbpPhidget()
        #self.photodiode = photodiode.Photodiode()
        #self.potentiometer = potentiometer.Potentiometer()
        #self.shutter = shutter.Shutter()
        #self.spectograph = spectrograph.Spectograph()
        #self.sr830 = sr830.Sr830()
        #self.temperature = temperature.Temperature()
        self.laser = laser.LaserSerialInterface(loop=False)

    def keithley_change_wavelength_loop(self, outfile = 'data.txt', wavelength_min=500, wavelength_max=700, dwavelength = 10):
        ins1 = self.keithley
        data_file = open(outfile,'w')
        print("opened file")
        wavelength_array = np.arange(wavelength_min,wavelength_max,dwavelength)
        print("created array")
        for wave in wavelength_array:
            print("starting change_wavelength")
            self.laser.change_wavelength(wave)
            photo1, photo2 = self.keithley.get_photodiode_reading()
            line = "{0} {1}\n".format(wave,photo1)
            data_file.write(line)
        data_file.close()

