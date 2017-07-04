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