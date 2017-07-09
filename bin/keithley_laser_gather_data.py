import cbp.cbp_class as cbp_instrument


def main():

    outputDir = '/home/pi/CBP/keithley/'
    wavelength_min = 450
    wavelength_max = 950
    wavelength_steps = 5
    Naverages = 3
    duration = 5000000
    collimated_beam_projector = cbp_instrument.CBP(keithley=True,spectograph=True,laser=True)
    collimated_beam_projector.keithley_change_wavelength_loop(outputDir=outputDir,wavelength_min=wavelength_min, wavelength_max=wavelength_max,wavelength_steps=wavelength_steps,Naverages=Naverages, duration=duration)

main()
