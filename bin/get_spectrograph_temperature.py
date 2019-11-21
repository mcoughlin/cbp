#!/usr/bin/env python
import cbp.cbp_instrument as CBP
import time

def main():
    cbp = CBP.CBP(spectrograph=True)
    temperature = cbp.spectrograph.get_temperature()
    print("{0} degrees C".format(temperature))
    set_to_temperature = 10.0
    cbp.spectrograph.set_temperature(set_to_temperature)
    time.sleep(0.5)
    temperature = cbp.spectrograph.get_temperature()
    print("{0} degrees C".format(temperature))

if __name__ == '__main__':
    main()
