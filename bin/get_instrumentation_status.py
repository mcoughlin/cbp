import cbp.cbp_class as CBP

def main():
    cbp = CBP.CBP(phidget=True,birger=True,potentiometer=True,monochromater=True,filter_wheel=True,keithley=True,spectrograph=True)
    output_dir = '/home/pi/CBP/status_log/'
    duration = 1000000
    cbp.write_status_log(output_dir=output_dir,duration=duration)

if __name__ == '__main__':
    main()
