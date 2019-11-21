import serial
import time

class NSR1(object):
    """

    """

    def __init__(self, port, timeout=1.):
        self.baudrate = 115200

        self.instrument = serial.Serial(port, baudrate=self.baudrate, timeout=timeout)
        self.write('1OR')
        self.wait_move_finish(60)

    def close(self):
        """
        Close the serial device
        :return: None
        """
        self.instrument.close()
        return None

    def str2cmd(self, command):
        """
        :type command: string: Command to be written to the device.  str2cmd will reformat the request to conform to
            expected standard form.
        :return serial_command: string: Encoded string that can be used with the NSR1.write function
        """
        if '\r' in command and not command.endswith('\r'):
            raise ValueError('NSR1:str2cmd: command {} not valid.  If command contains \\r, it must be the final character')
        if not command.endswith('\r'):

            command = command + '\r'
        serial_command = command.encode('ascii')
        return serial_command

    def write(self, command):
        """
        Issue a command to the NSR1.
        :param command: Str: Command to be written.
        :return: Ot
        """
        cmd = self.str2cmd(command)
        return self.instrument.write(cmd)

    def read(self):
        """
        :return: msg: str: Decoded device response, with read termination characters stripped.
        """
        msg = self.instrument.read_until('\r\n')
        msg = msg.decode().strip('\r\n')
        return msg

    def get_status(self, full=False):
        """
        :return: msg: str: If full is True, returns full status string from the device.  Else, returns last two characters
            (most relevent ones, typically).
        """
        self.write('1TS?')
        msg = self.read()
        if full:
            return msg
        else:
            return msg[-2:]

    def wait_move_finish(self, timeout=30):
        """
        :param timeout: float: Timeout value [s].
        :return: True if move completed
        """
        start_time = time.time()
        while (time.time() - start_time) / 1000. < timeout:
            status = self.get_status()
            if status == '33' or status == '32':
                return True
            else:
                time.sleep(0.25)
        raise RuntimeError('NSR1:wait_move_finish: Operation timed out...')

    def move_absolute(self, pos, timeout=30):
        """
        :param timeout: float: Timeout value [s].
        :param pos: float: Absolute position (in deg) to rotate the wheel to.
        :return: None
        """
        pos = float(pos)
        command = '1PA{:10.5f}'.format(pos)
        self.write(command)
        self.wait_move_finish(timeout=timeout)
        return None

    def move_relative(self, dist, timeout=30):
        """
        :param timeout: float: Timeout value [s].
        :param dist: float: Relative distance (in deg) to rotate the wheel.
        :return: None
        """
        dist = float(dist)
        command = '1PR{:10.5f}'.format(dist)
        self.write(command)
        self.wait_move_finish(timeout=timeout)
        return None
