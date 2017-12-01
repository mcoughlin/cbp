"""
.. module:: spectrograph
    :platform: unix
    :synopsis: This module is for communicating with the spectrograph instrument.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""

import serial, sys, time, glob, struct, os
import numpy as np
import optparse
import cbp.shutter
import thorlabs

if 'TESTENVIRONMENT' in os.environ:
    import mock
    sys.modules['seabreeze'] = mock.Mock()
else:
    import seabreeze
    seabreeze.use('pyseabreeze')
    import seabreeze.spectrometers as sb


class Spectrograph:
    """
    This is the class for communicating with the spectrograph
    """
    def __init__(self):
        self.status = None
        self.spectrometer = self.create_connection()
        self.temperature = self.get_temperature()

    def create_connection(self):
        """
        This method creates a connection to the spectrograph

        :return:
        """
        devices = sb.list_devices()
        #print(devices)
        try:
            spec = sb.Spectrometer(devices[0])
            self.status = "connected"
            print("Spectrograph connected")
            spec.tec_set_enable(True)
            return spec
        except Exception as e:
            print(e)
            self.status = "not connected"

    def get_spectrograph(self, duration = 1000000, spectrumFile='test.dat'):
        """
        This method returns the wavelength and intensities measured during the duration.

        :param duration:
        :param spectrumFile:
        :return:
        """
        if self.status != "not connected":
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
            #print("get_spectrograph done")

            # fid = open(spectrumFile, "w")
            # for wavelength, intensity in zip(wavelengths, intensities):
                # fid.write("%.5e %.5e\n" % (wavelength, intensity))
            # fid.close()

            return wavelengths, intensities
        else:
            pass

    def get_temperature(self):
        """
        This method returns the temperature of the spectrograph

        :return:
        """
        if self.status != "not connected":
            return self.spectrometer.tec_get_temperature_C()

    def set_temperature(self,temperature):
        """
        This method sets a temperature in c for the spectrograph

        :param temperature:
        :return:
        """
        if self.status != "not connected":
            self.spectrometer.tec_set_temperature_C(temperature)

    def enable_temperature_control(self):
        """
        This method enables the powered temperature control of the spectrograph

        :return:
        """
        if self.status != "not connected":
            self.spectrometer.tec_set_enable(True)

    def disable_temperature_control(self):
        """
        This method turns off the powered temperature control of the spectrograph

        :return:
        """
        if self.status != "not connected":
            self.spectrometer.tec_set_enable(False)

    def do_spectrograph(self, duration=10000000, spectrumFile='test.dat',doShutter=True, n_averages = 10, cbp_inst = None):
        """
        This method does the spectrograph reading.

        :param duration:
        :param spectrumFile:
        :return:
        """
        if self.status != "not connected":

            if doShutter:
                cbp_inst.flipper.run_flipper(1)
                #cbp_inst.shutter.run_shutter(-1)

                #thorlabs.thorlabs.main(val=1)
                #cbp.shutter.main(runtype="shutter", val=-1)
                #print "opened shutter"
            else:
                cbp_inst.flipper.run_flipper(2)
                #cbp_inst.shutter.run_shutter(1)
                #cbp.shutter.main(runtype="shutter", val=1)
                #print "closed shutter"

            cnt = 0
            for i in range(n_averages + 1):
                try:
                    wavelength, intensity = self.get_spectrograph(duration=duration,spectrumFile=spectrumFile)
                    if cnt == 0:
                        pass
                    elif cnt == 1:
                        intensity_list = intensity
                    else:
                        intensity_list = np.vstack((intensity_list,intensity))
                    cnt = cnt + 1 
                except:
                    continue

            intensities = np.mean(intensity_list,axis=0)
            wavelengths = wavelength

            #wavelengths, intensities = self.get_spectrograph(duration=duration, spectrumFile=spectrumFile)

            #cbp.shutter.main(runtype="shutter", val=1)
            cbp_inst.flipper.run_flipper(2)
            #cbp_inst.shutter.run_shutter(1)
            #thorlabs.thorlabs.main(val=2)

            return wavelengths, intensities
        else:
            pass

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

    wavelengths, intensities = spectrograph.get_spectrograph(duration=duration, spectrumFile=spectrumFile)

    return wavelengths, intensities

if __name__ == "__main__":

    # Parse command line
    opts = parse_commandline()

    if opts.doSpectrograph:
        wavelengths, intensities = main(runtype = "spectrograph", duration = opts.duration,
                                       spectrumFile = opts.spectrumFile)


