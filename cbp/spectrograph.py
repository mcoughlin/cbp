import serial, sys, time, glob, struct, os
import numpy as np
import optparse

import seabreeze
seabreeze.use('pyseabreeze')
import seabreeze.spectrometers as sb

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("--doSpectrograph", action="store_true",default=False)
    parser.add_option("-d", "--duration", help="exposure length",default=1000000,type=int)
    parser.add_option("-f","--spectrumFile",default='/home/pi/CBP/spectra/test.dat')

    opts, args = parser.parse_args()

    return opts

def get_spectrograph(spec, duration = 1000000, spectrumFile = 'test.dat'):

    spec.integration_time_micros(duration)
    time.sleep(duration*1e-6)
    wavelengths = spec.wavelengths()
    intensities = spec.intensities()

    idx1 = np.where(wavelengths >= 350.0)[0]
    idx2 = np.where(wavelengths <= 1100.0)[0]
    idx = np.intersect1d(idx1,idx2)
    wavelengths = wavelengths[idx]
    intensities = intensities[idx]

    fid = open(spectrumFile,"w")
    for wavelength,intensity in zip(wavelengths,intensities):
        fid.write("%.5e %.5e\n"%(wavelength,intensity))
    fid.close()

    return wavelengths,intensities

def main(runtype = "spectrograph", duration = 1000000, spectrumFile = 'test.dat'): 

    devices = sb.list_devices()
    spec = sb.Spectrometer(devices[0])

    wavelengths,intensities = get_spectrograph(spec, duration = duration, spectrumFile = spectrumFile)
    return wavelengths,intensities

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doSpectrograph:
        wavelengths,intensities = main(runtype = "spectrograph", duration = opts.duration, spectrumFile = opts.spectrumFile) 


