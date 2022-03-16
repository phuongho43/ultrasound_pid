import time
import serial
from serial.tools import list_ports
from simple_pid import PID
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
        sig_gen.set_pulse_period(0.5)
        sig_gen.set_pulse_duty_factor(50)
        sig_gen.set_modulation_state(1)
        volt_0 = input('Starting Voltage Output (mVolts): ')
        sig_gen.set_RF_amplitude(volt_0)
        sig_gen.display_status()
        print('-'*50)
        temp_0, _ = thermo.read_temp()
        print("{:<25} {:<10}".format('Thermo Temperature', temp_0))
        target_temp = input('Target Temperature (deg C): ')
        stim_duration = input('Stimulation Duration (sec): ')
        # pid_controller = PID(1, 0.1, 0.05, setpoint=target_temp, sample_time=1, output_limits=(0, 0.3))
        input('Press ENTER to START ultrasound stimulation.')
        sig_gen.set_RF_state(1)
        t0 = time.time()
        while time.time() - t0 < stim_duration:
            temp_i, _ = thermo.read_temp()
            volt_i = pid_controller(temp_i)
            print(temp_i, volt_i)
            # sig_gen.set_RF_amplitude(volt_i)
        sig_gen.set_RF_state(0)