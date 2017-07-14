import cmd
import initialize_cbp
import shlex
import cbp.cbp_class as CBP


class LaunchCbp(cmd.Cmd):
    def __init__(self, cbp, **kwargs):
        self.prompt = "cbp:// "
        cmd.Cmd.__init__(self, **kwargs)
        self.parser = initialize_cbp.create_parser()
        self.cbp = cbp

    def do_exit(self,line):
        return True

    def _do_phidget(self, args):
        initialize_cbp.phidget(self.cbp,args)

    def _do_potentiometer(self, args):
        initialize_cbp.potentiometer(self.cbp,args)

    def _do_altaz_compile(self, args):
        initialize_cbp.altaz_compile(self.cbp,args)

    def _do_altaz_steps(self, args):
        initialize_cbp.altaz_steps(self.cbp,args)

    def _do_altaz_angle(self, args):
        initialize_cbp.altaz_angle(self.cbp,args)

    def _do_birger_focus(self, args):
        initialize_cbp.birger_focus(self.cbp,args)

    def _do_birger_aperture(self, args):
        initialize_cbp.birger_aperture(self.cbp,args)

    def _do_lamp_lamp(self, args):
        initialize_cbp.lamp_lamp(self.cbp,args)

    def _do_shutter_shutter(self, args):
        initialize_cbp.shutter_shutter(self.cbp,args)

    def _do_photodiode(self, args):
        initialize_cbp.photodiode(self.cbp,args)

    def _do_filter_wheel_position(self, args):
        initialize_cbp.filter_wheel_position(self.cbp,args)

    def _do_filter_wheel_get_position(self, args):
        initialize_cbp.filter_wheel_get_position(self.cbp,args)

    def _do_monochrometer_wavelength(self, args):
        initialize_cbp.monochrometer_wavelength(self.cbp,args)

    def _do_monochrometer_get_wavelength(self, args):
        initialize_cbp.monochrometer_get_wavelength(self.cbp,args)

    def _do_monochrometer_filter(self, args):
        initialize_cbp.monochrometer_filter(self.cbp,args)

    def _do_monochrometer_get_filter(self, args):
        initialize_cbp.monochrometer_get_filter(self.cbp,args)

    def _do_keithley(self, args):
        initialize_cbp.keithley(self.cbp,args)

    def _do_spectograph(self, args):
        initialize_cbp.spectograph(self.cbp,args)

    def _do_laser_change_wavelength(self, args):
        initialize_cbp.laser_change_wavelength(self.cbp,args)

    def _do_laser_change_wavelength_loop(self, args):
        initialize_cbp.laser_change_wavelength_loop(self.cbp,args)

    def _do_laser_check_wavelength(self, args):
        initialize_cbp.laser_check_wavelength(self.cbp, args)

    def do_status(self,line):
        print("altaz: {0}".format(self.cbp.altaz.status))
        print("birger: {0}".format(self.cbp.birger.status))
        print("filter wheel: {0}".format(self.cbp.filter_wheel.status))
        print("keithley: {0}".format(self.cbp.keithley.status))
        print("lamp: {0}".format(self.cbp.lamp.status))
        print("laser: {0}".format(self.cbp.laser.status))
        print("lockin: {0}".format(self.cbp.lockin.status))
        print("phidget: {0}".format(self.cbp.phidget.status))
        print("potentiometer: {0}".format(self.cbp.potentiometer.status))
        print("shutter: {0}".format(self.cbp.shutter.status))
        print("spectrograph: {0}".format(self.cbp.spectrograph.status))
        print("temperature: {0}".format(self.cbp.temperature.status))

    def default(self, line):
        try:
            args = self.parser.parse_args(shlex.split(line))
            if hasattr(args, 'func'):
                args.func(args)
            else:
                cmd.Cmd.default(self, line)
        except SystemExit as err:
            if err.code == 2:
                print(err)


def main():
    cbp = CBP.CBP(everything=True)
    LaunchCbp(cbp=cbp).cmdloop()

if __name__ == '__main__':
    main()


