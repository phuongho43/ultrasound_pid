import time
import serial
from serial.tools import list_ports
from HH806 import HH806
from SG386 import SG386


def get_ports():
    ports = [port.device for port in list_ports.comports()]
    return ports


if __name__ == '__main__':
    # ports = get_ports()
    # print(ports)
    sig_gen_serial_port = '/dev/ttyUSB0'
    thermo_serial_port = '/dev/ttyUSB1'
    with SG386(sig_gen_serial_port) as sig_gen, HH806(thermo_serial_port) as thermo:
        sig_gen.set_modulation_type(4)
        sig_gen.set_modulation_function(0)
        sig_gen.set_frequency(1e6)
        sig_gen.set_PRBS_pulse_period(0.5)
        sig_gen.set_PRBS_pulse_length(50)
        sig_gen.set_modulation_state(1)
        output_volt = input('Starting Voltage Output (mVolts): ')
        sig_gen.set_RF_amplitude(output_volt)
        sig_gen.display_status()
        print('-'*50)
        t1, t2 = thermo.read_temp()
        print("{:<25} {:<10}".format('Thermo Temperature', t1))
        # target_temp = input('Target Temperature (deg C): ')
        # stim_duration = input('Stimulation Duration (sec): ')
        # input('Press ENTER to start ultrasound stimulation.')
        # sig_gen.set_RF_state(1)


