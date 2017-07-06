import cbp_cbp

cbp = cbp_cbp.CBP()

keithley = cbp.keithley
laser = cbp.laser


def main():
    cbp.keithley_change_wavelength_loop()

main()
