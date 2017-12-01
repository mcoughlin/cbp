#!/usr/bin/env python
import cbp.cbp_instrument as cbp_instrument
import cbp_notifications
import os
import time

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--duration",default=1,type=int)
    parser.add_option("--wavelength",default=600,type=int)

    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()


    wavelength_min=400
    wavelength_max=1000
    wavelength_steps = 10
    Naverages = 10
    duration = 100000

    outputDir = '/home/pi/CBP/test'
    collimated_beam_projector = cbp_instrument.CBP(keithley=True,spectrograph=True,laser=True)
    collimated_beam_projector.keithley_change_wavelength_loop(output_dir=outputDir, wavelength_min=wavelength_min, wavelength_max=wavelength_max, wavelength_steps=wavelength_steps, n_averages=Naverages, duration=duration)

main()
