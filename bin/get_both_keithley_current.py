import cbp.cbp_instrument as cbp_instrument
import cbp_notifications.cbp_email as cbp_notify
import visa
import time
import numpy as np
import os

def main():
    start = time.time()
    wavelength_min = 400
    wavelength_max = 1000
    wavelength_steps = 5
    Naverages = 10
    today = time.strftime("%m_%d_%Y")
    outputDir = '/home/pi/CBP/keithley_both/{4}/{0}_{1}/{2}_{3}/'.format(wavelength_steps, Naverages,wavelength_min, wavelength_max,today)
    collimated_beam_projector = cbp_instrument.CBP(keithley=True, keithley_2=True, laser=True)
    try:
        collimated_beam_projector.both_keithley_change_wavelength(output_dir=outputDir,wavelength_min=wavelength_min,wavelength_max=wavelength_max,wavelength_steps=wavelength_steps,n_averages=Naverages)
    except Exception() as e:
       cbp_email_error = cbp_notify.CbpEmailError(program="get_both_keithley_current.py",error=e)
       cbp_email_error.send()
    end = time.time()
    total_time = end - start
    print(total_time)
    cbp_email_complete = cbp_notify.CbpEmailComplete(program="get_both_keithley_current.py",t=total_time)
    cbp_email_complete.send()
    cmd = 'tar -zcvf /home/pi/CBP/keithley_both/keithley_both_{0}.tar.gz  /home/pi/CBP/keithley_both/{0}/'.format(today)
    os.system(cmd)
if __name__ == '__main__':
    main()
