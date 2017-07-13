import serial, sys, time, glob, struct, os
import numpy as np
import optparse

import seabreeze
seabreeze.use('pyseabreeze')
import seabreeze.spectrometers as sb


class Spectrograph:
    def __init__(self):
        self.status = None
        self.spectrometer = self.create_connection()

    def create_connection(self):
        devices = sb.list_devices()
        try:
            spec = sb.Spectrometer(devices[0])
            self.status = "connected"
            print("Spectrograph connected")
            return spec
        except Exception as e:
            print(e)
            self.status = "not connected"

    def get_spectograph(self, duration = 1000000, spectrumFile='test.dat'):
        spec = self.spectrometer
        spec.integration_time_micros(duration)
        time.sleep(duration * 1e-6)
        wavelengths = spec.wavelengths()
        intensities = spec.intensities()

        idx1 = np.where(wavelengths >= 350.0)[0]
        idx2 = np.where(wavelengths <= 1100.0)[0]
        idx = np.intersect1d(idx1, idx2)
        wavelengths = wavelengths[idx]
        intensities = intensities[idx]
        print("get_spectrograph done")

        # fid = open(spectrumFile, "w")
        # for wavelength, intensity in zip(wavelengths, intensities):
            # fid.write("%.5e %.5e\n" % (wavelength, intensity))
        # fid.close()

        return wavelengths, intensities

    def do_spectograph(self, duration=10000000, spectrumFile='test.dat'):
        wavelengths, intensities = self.get_spectograph(duration=duration, spectrumFile=spectrumFile)

        return wavelengths, intensities

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


def main(runtype = "spectrograph", duration = 1000000, spectrumFile='test.dat'):
    spectrograph = Spectrograph()

    wavelengths, intensities = spectrograph.get_spectograph(duration=duration, spectrumFile=spectrumFile)

    return wavelengths, intensities

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doSpectrograph:
        wavelengths, intensities = main(runtype = "spectrograph", duration = opts.duration,
                                       spectrumFile = opts.spectrumFile)


