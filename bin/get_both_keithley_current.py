import cbp.keithley
import visa
import time

def main():
    duration = 10
    keithley_1 = cbp.keithley.Keithley(rm=visa.ResourceManager('@py'),resnum=0,do_reset=True)
    keithley_2 = cbp.keithley.Keithley(rm=visa.ResourceManager('@py'),resnum=1,do_reset=True)
    keithley_1_times, keithley_1_photosl = keithley_1.get_charge_timeseries(duration=duration)
    keithley_2_times, keithley_2_photosl = keithley_2.get_charge_timeseries(duration=duration)
    keithley_1_current_file = open('/home/pi/CBP/keithley/{0}/keithley_1/keithley_1_{1}.txt'.format(time.strftime("%m_%d_%Y"),time.strftime("%H_%M")))
    keithley_2_current_file = open('/home/pi/CBP/keithley/{0}/keithley_2/keithley_2_{1}.txt'.format(time.strftime("%m_%d_%Y"),time.strftime("%H_%M")))
    for t, photos in zip(keithley_1_times,keithley_1_photosl):
        keithley_1_current_file.write("{0:5} {1:5}\n".format(t,photos))

    for t,photos in zip(keithley_2_times,keithley_2_photosl):
        keithley_2_current_file.write("{0:5} {1:5}\n".format(t,photos))

if __name__ == '__main__':
    main()
