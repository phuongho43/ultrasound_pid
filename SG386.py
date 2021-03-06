import time
import serial


class SG386(object):
    """
    Stanford Research Systems Model SG386 DC to 6.075 GHz Signal Generator.
    https://www.thinksrs.com/downloads/pdfs/manuals/SG380m.pdf
    """
    def __init__(self, serial_port):
        self.open_connection(serial_port)
        self.max_amp = 0.5000  # Volt Vpp

    def open_connection(self, serial_port):
        """
        e.g. On Linux: /dev/ttyUSB0
        """
        try:
            self.ser = serial.Serial(serial_port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=True, timeout=1)
            if self.ser.isOpen():
                print('\nConnection OPEN\n')
            self.ser.write(b'*RST\n')
            self.ser.write(b'ENBL 0\n')
            self.ser.write(b'*CLS\n')
            self.ser.write(b'REMT\n')
            self.ser.write(b'DISP 6\n')
        except serial.SerialException as e:
            print(e)
            raise

    def close_connection(self):
        try:
            self.ser.write(b'ENBL 0\n')
            self.ser.write(b'ENBR 0\n')
            self.ser.write(b'LCAL\n')
            self.ser.close()
            print('\nConnection CLOSED\n')
        except Exception as e:
            print(e)
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def get_identity(self):
        """
        b'Stanford Research Systems,SG386,s/n001671,ver1.21.26\r\n'
        """
        try:
            self.ser.write(b'*IDN?\n')
            r = self.ser.readline()
            return r.decode('utf-8').strip()
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_modulation_type(self):
        try:
            self.ser.write(b'TYPE?\n')
            r = self.ser.readline()
            return int(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_modulation_type(self, mtype):
        try:
            self.ser.write('TYPE {}\n'.format(mtype).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_modulation_function(self):
        try:
            self.ser.write(b'PFNC?\n')
            r = self.ser.readline()
            return int(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_modulation_function(self, mfunc):
        try:
            self.ser.write('PFNC {}\n'.format(mfunc).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_frequency(self):
        try:
            self.ser.write(b'FREQ?\n')
            r = self.ser.readline()
            return float(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_frequency(self, freq):
        try:
            self.ser.write('FREQ {}\n'.format(freq).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_pulse_period(self):
        try:
            self.ser.write(b'PPER?\n')
            r = self.ser.readline()
            return float(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_pulse_period(self, bit_per):
        try:
            self.ser.write('PPER {}\n'.format(bit_per).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_pulse_duty_factor(self):
        try:
            self.ser.write(b'PDTY?\n')
            r = self.ser.readline()
            return float(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_pulse_duty_factor(self, bit_len):
        try:
            self.ser.write('PDTY {}\n'.format(bit_len).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_modulation_state(self):
        try:
            self.ser.write(b'MODL?\n')
            r = self.ser.readline()
            return int(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_modulation_state(self, mstate):
        try:
            self.ser.write('MODL {}\n'.format(mstate).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_RF_amplitude(self):
        try:
            self.ser.write(b'AMPR? Vpp\n')
            r = self.ser.readline()
            return float(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_RF_amplitude(self, amp):
        amp = float(amp)
        try:
            if abs(amp) <= self.max_amp:
                self.ser.write('AMPR {} Vpp\n'.format(amp).encode('utf-8'))
                # self.ser.write(b'DISP 6\n')
            else:
                print('Output amplitude too high!')
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_RF_state(self):
        try:
            self.ser.write(b'ENBR?\n')
            r = self.ser.readline()
            return int(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_RF_state(self, rfstate):
        try:
            self.ser.write('ENBR {}\n'.format(rfstate).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def display_status(self):
        status = {
            'Device Identity': self.get_identity(),
            'Modulation Type': self.get_modulation_type(),
            'Modulation Function': self.get_modulation_function(),
            'Signal Frequency': self.get_frequency(),
            'Pulse Period': self.get_pulse_period(),
            'Pulse Duty Factor': self.get_pulse_duty_factor(),
            'Modulation State': self.get_modulation_state(),
            'RF Amplitude': self.get_RF_amplitude(),
            'RF State': self.get_RF_state()
        }
        print("{:<25} {:<10}".format('Parameter','Value'))
        print('='*80)
        for k, v in status.items():
            # print(k, v)
            print("{:<25} {:<10}".format(k, v))
            

if __name__ == '__main__':
    serial_port = '/dev/ttyUSB0'
    with SG386(serial_port) as dev:
        dev.display_status()