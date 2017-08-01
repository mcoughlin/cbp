#!/usr/bin/env python
from lxml import etree
import numpy as np

def main(status_log_file):
    status_log_file = status_log_file
    et = etree.parse(status_log_file)
    root = et.getroot()
    instrument_status_dictionary = {}
    times_list = []
    current_list = []
    intensity_array = np.array([])
    wavelength_array = np.array([])
    for child in root:
        if child.tag == "instrument_status":
            instrument_status_dictionary['angle'] = float(child.attrib['angle'])
            instrument_status_dictionary['potentiometer_1'] = float(child.attrib['potentiometer_1'])
            instrument_status_dictionary['potentiometer_2'] = float(child.attrib['potentiometer_2'])
            instrument_status_dictionary['mask'] = int(child.attrib['mask'])
            instrument_status_dictionary['focus'] = float(child.attrib['focus'])
            instrument_status_dictionary['filter'] = int(child.attrib['filter'])
            instrument_status_dictionary['aperture'] = int(child.attrib['aperture'])
            instrument_status_dictionary['wavelength'] = int(child.attrib['wavelength'])
            instrument_status_dictionary['y'] = float(child.attrib['y'])
            instrument_status_dictionary['x'] = float(child.attrib['x'])
            instrument_status_dictionary['z'] = float(child.attrib['z'])
        elif child.tag == "keithley":
            for grandchild in child:
                current_list.append(float(grandchild.attrib['current']))
                times_list.append(float(grandchild.attrib['time']))
        elif child.tag == "spectrograph":
            for grandchild in child:
                intensity_array = np.append(intensity_array, float(grandchild.attrib['intensity']))
                wavelength_array = np.append(wavelength_array, float(grandchild.attrib['wavelength']))

    return instrument_status_dictionary, current_list, times_list, intensity_array, wavelength_array

if __name__ == '__main__':
    status_log_file = ""
    instrument_status_dictionary, current_list, times_list, intensity_array, wavelength_array = main(status_log_file=status_log_file)
    print(instrument_status_dictionary)
    print(current_list)
    print(times_list)
    print(intensity_array)
    print(wavelength_array)