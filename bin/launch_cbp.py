import cmd
import runinst
import shlex


class LaunchCbp(cmd.Cmd):
    def __init__(self, **kwargs):
        self.prompt = "cbp:// "
        cmd.Cmd.__init__(self, **kwargs)
        self.parser = runinst.create_parser()

    def do_exit(self,line):
        return True

    def _do_phidget(self, args):
        runinst.phidget(args)

    def _do_pententiometer(self, args):
        runinst.pententiometer(args)

    def _do_altaz_compile(self, args):
        runinst.altaz_compile(args)

    def _do_altaz_steps(self, args):
        runinst.altaz_steps(args)

    def _do_altaz_angle(self, args):
        runinst.altaz_angle(args)

    def _do_birger_focus(self, args):
        runinst.birger_focus(args)

    def _do_birger_aperture(self, args):
        runinst.birger_aperture(args)

    def _do_lamp_lamp(self, args):
        runinst.lamp_lamp(args)

    def _do_shutter_shutter(self, args):
        runinst.shutter_shutter(args)

    def _do_photodiode(self, args):
        runinst.photodiode(args)

    def _do_filter_wheel_position(self, args):
        runinst.filter_wheel_position(args)

    def _do_filter_wheel_get_position(self, args):
        runinst.filter_wheel_get_position(args)

    def _do_monochrometer_wavelength(self, args):
        runinst.monochrometer_wavelength(args)

    def _do_monochrometer_get_wavelength(self, args):
        runinst.monochrometer_get_wavelength(args)

    def _do_monochrometer_filter(self, args):
        runinst.monochrometer_filter(args)

    def _do_monochrometer_get_filter(self, args):
        runinst.monochrometer_get_filter(args)

    def _do_keithley(self, args):
        runinst.keithley(args)

    def _do_spectograph(self, args):
        runinst.spectograph(args)

    def _do_laser_laser(self, args):
        runinst.laser_laser(args)

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
    LaunchCbp().cmdloop()

if __name__ == '__main__':
    main()


