import time
import serial
import binascii


def hex2temp(h, sign):
    """Convert thermometer hex reading to temperature values"""
    if h == '' or sign == b'00':
        return 0
    else:
        if sign == b'1f':
            # negative numbers are relative to b'ffff' = 65535
            return -(65535 - int(h,16))/10.0
        else:
            return int(h, 16)/10.0


class HH806(object):
    """
    Omega HH806AU Thermometer.
    https://github.com/jhellerstedt/instrument-IO/blob/master/omega_HH806AU_logging/omega_HH806AU.py
    """
    def __init__(self, serial_port):
        self.open_connection(serial_port)

    def open_connection(self, serial_port):
        """
        e.g. On Linux: /dev/ttyUSB0
        """
        try:
            self.ser = serial.Serial(serial_port, baudrate=19200, bytesize=8, parity='E', stopbits=1, timeout=1)
            if self.ser.isOpen():
                print('\nConnection OPEN\n')
        except serial.SerialException as e:
            print(e)
            raise
    
    def close_connection(self):
        try:
            self.ser.close()
            print('\nConnection CLOSED\n')
        except Exception as e:
            print(e)
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def read_temp(self):
        """
        read command structure: # LL ID CH N checksum 0D0A
        LL = command length code (# + LL + ID + CH + N + check sum)byte
        ID = identification code, e.g. 00
        CH = channel identification, e.g. 00
        N = data access code, e.g., N
        check sum = hex of np.mod(sum(b"# LL ID CH N"), 256)
        e.g. A2 = hex of np.mod(sum(b"#0A0000N"), 256)
        """
        try:
            command = b"#0A0000NA2\r\n"
            self.ser.reset_input_buffer()
            self.ser.write(command)
            r = self.ser.read(15)
            t1 = hex2temp(binascii.hexlify(r[5:7]), binascii.hexlify(r[4:5]))
            t2 = hex2temp(binascii.hexlify(r[10:12]), binascii.hexlify(r[9:10]))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise
        return t1, t2
            

if __name__ == '__main__':
    ta = time.time()
    tb = time.time()
    serial_port = '/dev/ttyUSB0'
    with HH806(serial_port) as dev:
        while (tb - ta) < 60:
            tb = time.time()
            t1, t2 = dev.read_temp()
            print(t1)
            time.sleep(0.1)
