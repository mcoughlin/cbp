import cbp.cbp_class as cbp_instrument


def main():

    wavelength_min=500
    wavelength_max=800
    wavelength_steps = 10
    Naverages = 3
    duration = 5000000
    outputDir = '/home/pi/CBP/keithley/7_15_2017/{0}_{1}/{4}/{2}_{3}/'.format(wavelength_steps,Naverages,wavelength_min,wavelength_max,duration)
    collimated_beam_projector = cbp_instrument.CBP(keithley=True,spectrograph=True,laser=True)
    collimated_beam_projector.keithley_change_wavelength_loop(output_dir=outputDir, wavelength_min=wavelength_min, wavelength_max=wavelength_max, wavelength_steps=wavelength_steps, n_averages=Naverages, duration=duration)

main()
