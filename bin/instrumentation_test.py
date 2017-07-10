import cbp.cbp_class as CBP

def altaz():
    cbp = CBP.CBP(altaz=True)
    raw_input("Press enter to continue")
    cbp.altaz.do_steps(motornum=1,val=100)
    cbp.altaz.do_steps(motornum=1, val=-100)

def birger():
    pass

def filter_wheel():
    pass

def lamp():
    pass

def phidget():
    pass

def photodiode():
    pass

def potentiometer():
    pass

def shutter():
    pass


def main():
    altaz()

if __name__ == '__main__':
    main()