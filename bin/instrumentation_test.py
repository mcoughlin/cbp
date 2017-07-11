import cbp.cbp_class as CBP


def altaz(test_steps=False,test_altangle=False,test_azangle=False):
    cbp = CBP.CBP(altaz=True)
    raw_input("Press enter to continue: ")
    if test_steps:
        cbp.altaz.do_steps(motornum=1,val=100)
        cbp.altaz.do_steps(motornum=1, val=-100)
    if test_altangle:
        cbp.altaz.do_altangle(motornum=1,val=0)
    if test_azangle:
        cbp.altaz.do_azangle(motornum=1,val=0)
        cbp.altaz.do_azangle(motornum=1,val=0)


def birger(test_focus=False,test_aperture=False,test_status=False):
    cbp = CBP.CBP(birger=True)
    if test_focus:
        cbp.birger.do_focus(val=1000)
    if test_aperture:
        cbp.birger.do_aperture(val=12)
    if test_status:
        print(cbp.birger.do_status())


def filter_wheel(test_position=False,test_get_position=False):
    cbp = CBP.CBP(filter_wheel=True)
    if test_position:
        cbp.filter_wheel.do_position()
    if test_get_position:
        print(cbp.filter_wheel.get_position())


def lamp(test_lamp=False):
    cbp = CBP.CBP(lamp=True)
    if test_lamp:
        cbp.lamp.run_lamp(val=12)


def phidget(test_phidget=False):
    cbp = CBP.CBP(phidget=True)
    if test_phidget:
        cbp.phidget.do_phidget(nave=10000)


def photodiode(test_photodiode=False):
    cbp = CBP.CBP(photodiode=True)
    if test_photodiode:
        cbp.photodiode.photodiode()


def potentiometer(test_potentiometer=False):
    cbp = CBP.CBP(potentiometer=True)
    if test_potentiometer:
        cbp.potentiometer.get_potentiometer()


def shutter(test_shutter=False):
    cbp = CBP.CBP(shutter=True)
    if test_shutter:
        cbp.shutter.run_shutter()


def spectrograph(test_spectrograph):
    cbp = CBP.CBP(spectograph=True)
    if test_spectrograph:
        pass


def sr830(test_sr830=False):
    cbp = CBP.CBP(sr830=True)
    if test_sr830:
        photo = cbp.sr830.get_sr830()
        return photo


def temperature(test_temperature=False):
    cbp = CBP.CBP(temperature=True)
    if test_temperature:
        temp = cbp.temperature.do_photodiode()
        return temp


def main():
    print(potentiometer(test_potentiometer=True))
    


if __name__ == '__main__':
    main()
