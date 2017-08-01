#!/usr/bin/env python
import cbp.cbp_instrument as cbp_instrument
import cbp_notifications
import os
import time

def main():

    start = time.time()
    wavelength_min=400
    wavelength_max=1000
    wavelength_steps = 10
    Naverages = 10
    duration = 100000
    outputDir = '/home/pi/CBP/keithley/7_23_2017/{0}_{1}/{4}/{2}_{3}/'.format(wavelength_steps,Naverages,wavelength_min,wavelength_max,duration)
    collimated_beam_projector = cbp_instrument.CBP(keithley=True,spectrograph=True,laser=True)
    try:
        keithley_change_wavelength_start_email = cbp_notifications.cbp_email.CbpEmail(msg="The program started",sender="eric.coughlin2014@gmail.com",recipients="eric.coughlin2014@gmail.com",subject="[CBP Notification] Keithley Change Wavelength Start")
        keithley_change_wavelength_start_email.send()
        collimated_beam_projector.keithley_change_wavelength_loop(output_dir=outputDir, wavelength_min=wavelength_min, wavelength_max=wavelength_max, wavelength_steps=wavelength_steps, n_averages=Naverages, duration=duration)
    except Exception as e:
        keithley_change_wavelength_email = cbp_notifications.cbp_email.CbpEmail(msg="The program had a unrecoverable error{0}".format(e),sender="eric.coughlin2014@gmail.com",recipients="eric.coughlin2014@gmail.com",subject="[CBP Notification] Keithley Change Wavelength Error")
        keithley_change_wavelength_email.send()
    end = time.time()
    total_time = end - start
    keithley_change_wavelength_email=cbp_notifications.cbp_email.CbpEmail(msg="The program is complete\n total time: {0}".format(total_time),sender="eric.coughlin2014@gmail.com",recipients="eric.coughlin2014@gmail.com",subject="[CBP Notification] Keithley Change Wavelength Done")
    keithley_change_wavelength_email.send()
    cmd = "tar -zcvf ~/CBP/keithley/keithley_7_23_2017.tar.gz ~/CBP/keithley/7_23_2017/"
    os.system(cmd)

main()
