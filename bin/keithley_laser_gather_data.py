import cbp.cbp

cbp = cbp.cbp.CBP()

keithley = cbp.keithley
laser = cbp.laser


def main():
    cbp.keithley_change_wavelength_loop()

main()