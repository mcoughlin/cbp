import cbp.keithley
import visa
import time
import numpy as np
import os

def main():
    num_averages = 10
    keithley_1 = cbp.keithley.Keithley(rm=visa.ResourceManager('@py'),resnum=0,do_reset=True)
    keithley_2 = cbp.keithley.Keithley(rm=visa.ResourceManager('@py'),resnum=1,do_reset=True)
    keithley_1_photosl = []
    keithley_2_photosl = []
    for i in range(num_averages):
        keithley_1.do_reset()
        keithley_1_photosl.append(keithley_1.get_photodiode_reading())
        keithley_2.do_reset()
        keithley_2_photosl.append(keithley_2.get_photodiode_reading())
        if not os.path.exists('/home/pi/CBP/keithley/{0}/{1}/keithley_1/'.format(time.strftime("%m_%d_%Y"),num_averages)):
            os.makedirs('/home/pi/CBP/keithley/{0}/{1}/keithley_1/'.format(time.strftime("%m_%d_%Y"),num_averages))
    if not os.path.exists('/home/pi/CBP/keithley/{0}/{1}/keithley_2/'.format(time.strftime("%m_%d_%Y"),num_averages)):
        os.makedirs('/home/pi/CBP/keithley/{0}/{1}/keithley_2/'.format(time.strftime("%m_%d_%Y"),num_averages))
    keithley_1_current_file = open('/home/pi/CBP/keithley/{0}/{2}/keithley_1/keithley_1_{1}.txt'.format(time.strftime("%m_%d_%Y"),time.strftime("%H_%M"),num_averages),'w')
    keithley_2_current_file = open('/home/pi/CBP/keithley/{0}/{2}/keithley_2/keithley_2_{1}.txt'.format(time.strftime("%m_%d_%Y"),time.strftime("%H_%M"),num_averages),'w')
    keithley_1_averages = np.mean(keithley_1_photosl)
    keithley_2_averages = np.mean(keithley_2_photosl)
    keithley_1_std = np.std(keithley_1_photosl)
    keithley_2_std = np.std(keithley_2_photosl)
    keithley_1_current_file.write("{0}".format(keithley_1_averages))
    keithley_2_current_file.write("{0}".format(keithley_2_averages))
    keithley_1_current_file.close()
    keithley_2_current_file.close()

if __name__ == '__main__':
    main()
