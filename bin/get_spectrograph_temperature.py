import cbp.cbp_class as CBP


def main():
    cbp = CBP.CBP(spectrograph=True)
    temperature = cbp.spectrograph.get_temperature()
    print("{0} degrees C".format(temperature))

if __name__ == '__main__':
    main()