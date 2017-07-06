import cbp_cbp

cbp = cbp_cbp.CBP()

keithley = cbp.keithley
laser = cbp.laser


def main():
    outfile = '/home/pi/CBP/keithley/data.dat'
    wavelength_min=500
    wavelength_max=700
    dwavelength = 10
    cbp.keithley_change_wavelength_loop(wavelength_min=wavelength_min,wavelength_max=wavelength_max,dwavelength=dwavelength,outfile=outfile)

main()
