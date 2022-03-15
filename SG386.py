import time
import serial


class SG386(object):
    """
    Stanford Research Systems Model SG386 DC to 6.075 GHz Signal Generator.
    https://www.thinksrs.com/downloads/pdfs/manuals/SG380m.pdf
    """
    def __init__(self, serial_port):
        self.open_connection(serial_port)
        self.max_amp = 0.3  # Volt RMS

    def open_connection(self, serial_port):
        """
        e.g. On Linux: /dev/ttyUSB0
        """
        try:
            self.ser = serial.Serial(serial_port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=True, timeout=1)
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

    def get_identity(self):
        """
        b'Stanford Research Systems,SG386,s/n001671,ver1.21.26\r\n'
        """
        try:
            self.ser.reset_input_buffer()
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
            self.ser.reset_input_buffer()
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
            self.ser.reset_input_buffer()
            self.ser.write('TYPE {}\n'.format(mtype).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_modulation_function(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.write(b'MFNC?\n')
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
            self.ser.reset_input_buffer()
            self.ser.write('MFNC {}\n'.format(mfunc).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_frequency(self):
        try:
            self.ser.reset_input_buffer()
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
            self.ser.reset_input_buffer()
            self.ser.write('FREQ {}\n'.format(freq).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_PRBS_pulse_period(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.write(b'RPER?\n')
            r = self.ser.readline()
            return float(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_PRBS_pulse_period(self, bit_per):
        try:
            self.ser.reset_input_buffer()
            self.ser.write('RPER {}\n'.format(bit_per).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_PRBS_pulse_length(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.write(b'PRBS?\n')
            r = self.ser.readline()
            return float(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_PRBS_pulse_length(self, bit_len):
        try:
            self.ser.reset_input_buffer()
            self.ser.write('PRBS {}\n'.format(bit_len).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_modulation_state(self):
        try:
            self.ser.reset_input_buffer()
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
            self.ser.reset_input_buffer()
            self.ser.write('MODL {}\n'.format(mstate).encode('utf-8'))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_RF_amplitude(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.write(b'AMPR? RMS\n')
            r = self.ser.readline()
            return float(r)
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def set_RF_amplitude(self, amp):
        try:
            self.ser.reset_input_buffer()
            if abs(float(amp)) <= self.max_amp:
                self.ser.write('AMPR {} RMS\n'.format(amp).encode('utf-8'))
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
            self.ser.reset_input_buffer()
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
            self.ser.reset_input_buffer()
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
            'PRBS Pulse Period': self.get_PRBS_pulse_period(),
            'PRBS Pulse Length': self.get_PRBS_pulse_length(),
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
