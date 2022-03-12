import time
import serial


class SG386(object):
    """
    Stanford Research Systems Model SG386 DC to 6.075 GHz Signal Generator.
    https://www.thinksrs.com/downloads/pdfs/manuals/SG380m.pdf
    """
    def __init__(self, serial_port):
        self.open_connection(serial_port)

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
            print(r)
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