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


class CBP:
    def __init__(self):
        #self.altaz = altaz.Altaz()
        #self.birger = birger.Birger()
        #self.filter_wheel = filter_wheel.FilterWheel()
        self.keithley = cbp.keithley.Keithley()
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

    def keithley_change_wavelength_loop(self, outfile='data.txt', wavelength_min=500, wavelength_max=700, wavelength_steps=10):
        data_file = open(outfile,'w')
        print("opened file")
        wavelength_array = np.arange(wavelength_min, wavelength_max, wavelength_steps)
        print("created array")
        for wave in wavelength_array:
            print("starting change_wavelength")
            self.laser.change_wavelength(wave)
            #photo1, photo2 = self.keithley.get_photodiode_reading()
            thorlabs.thorlabs.main(runtype="flipper",val=1)
            thorlabs.thorlabs.main(val=2)
            line = "{0} {1}\n".format(wave, '5.3')
            data_file.write(line)
        data_file.close()

