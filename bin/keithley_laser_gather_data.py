from cbp.CBP import CBP


def main():

    outfile = '/home/pi/CBP/keithley/data.dat'
    wavelength_min=500
    wavelength_max=700
    wavelength_steps = 10
    colluminated_beam_projector = CBP()
    colluminated_beam_projector.keithley_change_wavelength_loop(wavelength_min=wavelength_min, wavelength_max=wavelength_max,
                                                                wavelength_steps=wavelength_steps)

main()
