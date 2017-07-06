import cbp.CBPClass as CBP


def main():

    outputDir = '/home/pi/CBP/keithley/'
    wavelength_min=400
    wavelength_max=1000
    wavelength_steps = 5
    Naverages = 3
    collimated_beam_projector = CBP.CBP()
    collimated_beam_projector.keithley_change_wavelength_loop(outputDir=outputDir,wavelength_min=wavelength_min, wavelength_max=wavelength_max,wavelength_steps=wavelength_steps,Naverages=Naverages)

main()
