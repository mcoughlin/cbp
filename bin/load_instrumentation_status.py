#!/usr/bin/env python
import cbp.cbp_instrument as CBP

def main():
    cbp = CBP.CBP()
    status_log_file = ''
    instrument_status_dictionary, current_list, times_list, intensity_array, wavelength_array = cbp.load_status_log_xml(status_log_file=status_log_file)

    return instrument_status_dictionary, current_list, times_list, intensity_array, wavelength_array

if __name__ == '__main__':
    instrument_status_dictionary, current_list, times_list, intensity_array, wavelength_array = main()
    print(instrument_status_dictionary)
    print(current_list)
    print(times_list)
    print(intensity_array)
    print(wavelength_array)