import time
import serial


class SG386(object):
    """
    Stanford Research Systems Model SG386 DC to 6.075 GHz Signal Generator.
    https://www.thinksrs.com/downloads/pdfs/manuals/SG380m.pdf
    """
    def __init__(self, serial_port):
        self.open_connection(serial_port)
        self.max_amp = 100

    def open_connection(self, serial_port):
        """
        e.g. On Linux: /dev/ttyUSB0
        """
        try:
            self.ser = serial.Serial(serial_port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=True, timeout=1)
            print('Connection is Open: ', self.ser.isOpen())
        except serial.SerialException as e:
            print(e)
            raise

    def close_connection(self):
        try:
            self.ser.close()
        except Exception as e:
            print(e)
            raise

    def get_identity(self):
        """
        b'Stanford Research Systems,SG386,s/n001671,ver1.21.26\r\n'
        """
        try:
            self.ser.reset_input_buffer()
            self.ser.write(b'*IDN?\n')
            r = self.ser.readline()
            return r
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
            self.ser.write(b'TYPE {}\n'.format(mtype))
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
            self.ser.write(b'MFNC {}\n'.format(mfunc))
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
            self.ser.write(b'FREQ {}\n'.format(freq))
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
            self.ser.write(b'RPER {}\n'.format(bit_per))
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
            self.ser.write(b'PRBS {}\n'.format(bit_len))
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
            self.ser.write(b'MODL {}\n'.format(mstate))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise

    def get_RF_amplitude(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.write(b'AMPR?\n')
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
            if amp < self.max_amp:
                self.ser.write(b'AMPR {}\n'.format(amp))
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
            self.ser.write(b'ENBR {}\n'.format(rfstate))
        except serial.SerialException as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise
            

if __name__ == '__main__':
    serial_port = '/dev/ttyUSB0'
    dev = SG386(serial_port)
    dev.get_identity()
    dev.close_connection()