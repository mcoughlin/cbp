import cbp.cbp_class as CBP

def altaz():
    cbp = CBP.CBP(altaz=True)
    raw_input("Press enter to continue")
    cbp.altaz.do_steps(motornum=1,val=10)
    cbp.altaz.do_steps(motornum=1, val=-10)


def main():
    altaz()

if __name__ == '__main__':
    main()