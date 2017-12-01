#!/usr/bin/env python
import cbp.cbp_instrument as CBP
import cbp.shutter

def main():

    print "closed shutter"
    cbp.shutter.main(runtype="shutter", val=1)
    cbp = CBP.CBP(phidget=True,birger=True,potentiometer=True,monochromater=True,filter_wheel=True,keithley=True,spectrograph=True)
    output_dir = '/home/pi/CBP/status_log/'
    duration = 1000000
    cbp.write_status_log(output_dir=output_dir,duration=duration)

if __name__ == '__main__':
    main()
