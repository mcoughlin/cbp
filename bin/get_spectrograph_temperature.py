import cbp.cbp_class as CBP


def main():
    cbp = CBP.CBP(spectrograph=True)
    temperature = cbp.spectrograph.get_temperature()
    print("{0} degrees C".format(temperature))
    set_to_temperature = 2.5
    cbp.spectrograph.set_temperature(set_to_temperature)
    temperature = cbp.spectrograph.get_temperature()
    print("{0} degrees C".format(temperature))

if __name__ == '__main__':
    main()
