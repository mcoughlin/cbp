import serial
import numpy as np
class CBPMount(object):
    def __init__(self, port='/dev/ttyACM2'):
        self.port = port
        self.ser = serial.Serial(port, baudrate=57600, timeout=.1)
        self.alt = 0
        self.az = 0
        
    def get_alt(self):
        return self.alt
    
    def get_az(self):
        return self.az

    def set_freq(self, freq):
        com = 'freq %d\r' % freq
        return self.send(com)

    def set_alt(self, alt):
        dir = 1 if alt > self.alt else 2
        step = np.abs(alt - self.alt)
        self.alt = alt
        com = 'args %d %d 2\r\n' % (step, dir)
        return self.send(com)
        
    def set_az(self, az):
        dir = 1 if az > self.az else 2
        step = np.abs(az - self.az)
        self.az = az
        com = 'args %d %d 1\r\n' % (step, dir)
        return self.send(com)
    
    def send(self, com):
        self.ser.write(com)
        return self.ser.readall()

if __name__ == '__main__':
    m = CBPMount()

