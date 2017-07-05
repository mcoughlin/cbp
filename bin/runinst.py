#!/usr/bin/env python

import os, serial, sys, time, glob, struct, subprocess
import numpy as np
import argparse
from threading import Timer
#import FLI

import cbp.phidget, cbp.altaz
import cbp.potentiometer, cbp.birger
import cbp.lamp, cbp.shutter
import cbp.photodiode, cbp.filter_wheel
import cbp.monochromater, cbp.keithley
import cbp.spectrograph
import laser

def create_parser():
    """
    Parse the options given on the command-line.
    """
    parser = argparse.ArgumentParser(description='Run CBP Instruments.')

    subparsers = parser.add_subparsers(help='cbp instrument sub-commands')

    parser_phidget = subparsers.add_parser('phidget', help='prints out phidget position')
    parser_phidget.set_defaults(func=phidget)
    
    parser_pententiometer = subparsers.add_parser('pententiometer',
                                                  help='prints out information about the two pententiometers')
    parser_pententiometer.set_defaults(func=pententiometer)
    
    parser_altaz = subparsers.add_parser('altaz', help='instrument to move camera')
    
    parser_altaz_subparsers = parser_altaz.add_subparsers(help='altaz sub-commands')
    
    parser_altaz_compile = parser_altaz_subparsers.add_parser('compile', help="Does the compile action")
    parser_altaz_compile.set_defaults(func=altaz_compile)
    
    parser_altaz_steps = parser_altaz_subparsers.add_parser('steps', help="Does the steps action")
    parser_altaz_steps.add_argument('steps',default=1000,type=int)
    parser_altaz_steps.add_argument('motornum',default=1,type=int)
    parser_altaz_steps.set_defaults(func=altaz_steps)
    
    parser_altaz_angle = parser_altaz_subparsers.add_parser('angle', help="Does the angle action")
    parser_altaz_angle.add_argument('motornum',default=1,type=int)
    parser_altaz_angle.add_argument('angle', default=2.0, type=float)
    parser_altaz_angle.set_defaults(func=altaz_angle)

    parser_birger = subparsers.add_parser('birger', help='birger instrument')
    
    parser_birger_subparsers = parser_birger.add_subparsers(help='birger sub-commands')

    parser_birger_focus = parser_birger_subparsers.add_parser('focus', help='sets the focus')
    parser_birger_focus.add_argument('focus',default=4096,type=int, help='the value to set the focus to.')
    parser_birger_focus.set_defaults(func=birger_focus)

    parser_birger_aperture = parser_birger_subparsers.add_parser('aperture', help='sets the aperture')
    parser_birger_aperture.add_argument('aperture',default=0,type=int, help='the value to set the aperture to.')
    parser_birger_aperture.set_defaults(func=birger_aperture)

    parser_lamp = subparsers.add_parser('lamp', help='sets the lamp')
    parser_lamp.add_argument('lamp',default=100,type=int)
    parser_lamp.set_defaults(func=lamp_lamp)

    parser_shutter = subparsers.add_parser('shutter', help='sets the shutter')
    parser_shutter.add_argument('shutter',default=-1,type=int)
    parser_shutter.set_defaults(func=shutter_shutter)

    parser_photodiode = subparsers.add_parser('photodiode', help='prints photo')
    parser_photodiode.set_defaults(func=photodiode)

    parser_filter_wheel = subparsers.add_parser('filter wheel', help='filter wheel instrument')

    parser_filter_wheel_subparsers = parser_filter_wheel.add_subparsers(help='filter wheel sub-commands')

    parser_filter_wheel_position = parser_filter_wheel_subparsers.add_parser('position',
                                                                             help='change position of filter wheel.')
    parser_filter_wheel_position.add_argument('mask',default=0,type=int)
    parser_filter_wheel_position.add_argument('filter',default=0,type=int)
    parser_filter_wheel_position.set_defaults(func=filter_wheel_position)

    parser_filter_wheel_get_position = parser_filter_wheel_subparsers.add_parser('get position',
                                                                                 help='get position of filter wheel.')
    parser_filter_wheel_get_position.set_defaults(func=filter_wheel_get_position)
    
    parser_monochrometer = subparsers.add_parser('monochrometer', help='monochrometer instrument')

    parser_monochrometer_subparsers = parser_monochrometer.add_subparsers(help='monochrometer sub-commands')

    parser_monochrometer_wavelength = parser_monochrometer_subparsers.add_parser('wavelength',
                                                                                 help='change the wavelength of the '
                                                                                      'monochrometer')
    parser_monochrometer_wavelength.add_argument('wavelength',default=600,type=int)
    parser_monochrometer_wavelength.set_defaults(func=monochrometer_wavelength)

    parser_monochrometer_get_wavelength = parser_monochrometer_subparsers.add_parser('get wavelength',
                                                                                     help='get the wavelength of the '
                                                                                          'monochrometer')
    parser_monochrometer_get_wavelength.set_defaults(func=monochrometer_get_wavelength)

    parser_monochrometer_filter = parser_monochrometer_subparsers.add_parser('filter',
                                                                             help='change the filter of the '
                                                                                  'monochrometer')
    parser_monochrometer_filter.add_argument('monofilter',default=1,type=int)
    parser_monochrometer_filter.set_defaults(func=monochrometer_filter)

    parser_monochrometer_get_filter = parser_monochrometer_subparsers.add_parser('get filter',
                                                                                 help='get the filter of the '
                                                                                      'monochrometer')
    parser_monochrometer_get_filter.set_defaults(func=monochrometer_get_filter)

    parser_keithley = subparsers.add_parser('keithley', help='keithley instrument')
    parser_keithley.set_defaults(func=keithley)

    parser_spectograph = subparsers.add_parser('spectograph', help='spectograph instrument')
    parser_spectograph.add_argument('duration',default=1000000,type=int)
    parser_spectograph.set_defaults(func=spectograph)

    parser_laser = subparsers.add_parser('laser', help='laser instrument')
    parser_laser_subparsers = parser_laser.add_subparsers(help='laser sub-commands')
    parser_laser_change_wavelength = parser_laser_subparsers.add_parser('change_wavelength', help='change wavelength')
    parser_laser_change_wavelength.add_argument('wavelength', default=500, type=int)
    parser_laser_change_wavelength_loop = parser_laser_subparsers.add_parser('change_wavelength_loop', help='loop through array of wavelengths')
    parser_laser_change_wavelength_loop.add_argument('--diagnostic', action="store_true", help='performs diagnostic')
    parser_laser_change_wavelength_loop.add_argument('wavelength_min',default=500,type=int)
    parser_laser_change_wavelength_loop.add_argument('wavelength_max',default=520,type=int)
    parser_laser_change_wavelength.set_defaults(func=laser_change_wavelength)
    parser_laser_change_wavelength_loop.set_defaults(func=laser_change_wavelength_loop)

    parser.add_argument("-v","--verbose", action="store_true",default=False)

    return parser

def phidget(opts):
    nave = 10000
    x, y, z, angle = cbp.phidget.main(nave)
    print(x,y,z,angle)

def pententiometer(opts):
    potentiometer_1, potentiometer_2 = cbp.potentiometer.main()
    print potentiometer_1, potentiometer_2

def altaz_compile(opts):
    cbp.altaz.main(runtype = "compile")
    
def altaz_steps(opts):
    cbp.altaz.main(runtype = "steps", val = opts.steps, motornum = opts.motornum)
    
def altaz_angle(opts):
    cbp.altaz.main(runtype = "angle", val = opts.angle, motornum = opts.motornum)

def birger_focus(opts):
    cbp.birger.main(runtype = "focus", val = opts.focus)
    
def birger_aperture(opts):
    cbp.birger.main(runtype = "aperture", val = opts.aperture)

def lamp_lamp(opts):
    cbp.lamp.main(runtype = "lamp", val = opts.lamp)

def shutter_shutter(opts):
    cbp.shutter.main(runtype = "shutter", val = opts.shutter)

def photodiode(opts):
    photo = cbp.photodiode.main(runtype = "photodiode")
    print photo

def filter_wheel_position(opts):
    cbp.filter_wheel.main(runtype = "position", mask = opts.mask, filter = opts.filter)

def filter_wheel_get_position(opts):
    cbp.filter_wheel.main(runtype = "getposition")

def monochrometer_wavelength(opts):
    cbp.monochromater.main(runtype = "monowavelength", val = opts.wavelength)

def monochrometer_get_wavelength(opts):
    cbp.monochromater.main(runtype = "getmonowavelength")

def monochrometer_filter(opts):
    cbp.monochromater.main(runtype = "monofilter", val = opts.monofilter)

def monochrometer_get_filter(opts):
    cbp.monochromater.main(runtype = "getmonofilter")

def keithley(opts):
    photo1, photo2 = cbp.keithley.main(runtype = "keithley", doReset = 1, doSingle = 1)
    print(photo1, photo2)

def spectograph(opts):
    wavelengths, intensities = cbp.spectrograph.main(runtype = "spectrograph", duration = opts.duration)
    print(wavelengths, intensities)

def laser_change_wavelength(opts):
    laser_interface = laser.LaserSerialInterface(loop=False)
    laser_interface.change_wavelength(opts.wavelength)

def laser_change_wavelength_loop(opts):
    laser_interface = laser.LaserSerialInterface(loop=False)
    laser_interface.loop_change_wavelength(opts.wavelength_min,opts.wavelength_max, opts.diagnostic)

def main():
    parser = create_parser()
    opts = parser.parse_args()
    opts.func(opts)

if __name__ == '__main__':
    main()
