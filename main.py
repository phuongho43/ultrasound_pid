import os
import time
import atexit

import serial

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from serial.tools import list_ports
from simple_pid import PID
from HH806 import HH806
from SG386 import SG386


custom_palette = ['#648FFF', '#FE6100', '#DC267F', '#785EF0', '#FFB000']

custom_styles = {
    'figure.figsize': (16, 8),
    'text.color': '#212121',
    'axes.titleweight': 'bold',
    'axes.titlesize': 32,
    'axes.titlepad': 18,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.labelsize': 28,
    'axes.labelpad': 10,
    'axes.labelcolor': '#212121',
    'axes.labelweight': 600,
    'axes.linewidth': 3,
    'axes.edgecolor': '#212121',
    'xtick.labelsize': 28,
    'ytick.labelsize': 28,
    'legend.fontsize': 28,
    'lines.linewidth': 5
}


def setup_dirs(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def plot_lines(save_dir, xvar, yvar, xlabel, ylabel):
    df = pd.read_csv(os.path.join(save_dir, 'y.csv'))
    with plt.style.context(('seaborn-whitegrid', custom_styles)), sns.color_palette(custom_palette):
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.lineplot(data=df, x=xvar, y=yvar)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig_name = '{}.png'.format(yvar)
        plt.savefig(os.path.join(save_dir, fig_name), dpi=200, transparent=False, bbox_inches='tight')
        plt.close()

def get_ports():
    ports = [port.device for port in list_ports.comports()]
    return ports

def exit_handler():
    data = {'time': time_data, 'temp': temp_data, 'volt': volt_data}
    df = pd.DataFrame(data)
    save_dir = os.path.join(root_dir, time.strftime('%Y%m%d_%H-%M-%S'))
    setup_dirs(save_dir)
    df.to_csv(os.path.join(save_dir, 'y.csv'), index=False)
    plot_lines(save_dir, xvar='time', yvar='temp', xlabel='Time', ylabel='Temperature')
    plot_lines(save_dir, xvar='time', yvar='volt', xlabel='Time', ylabel='Voltage')


if __name__ == '__main__':
    atexit.register(exit_handler)
    # ports = get_ports()
    # print(ports)
    root_dir = '/home/phuong/data/ultrasound_pid_data/'
    sig_gen_serial_port = '/dev/ttyUSB0'
    thermo_serial_port = '/dev/ttyUSB1'
    with SG386(sig_gen_serial_port) as sig_gen, HH806(thermo_serial_port) as thermo:
        sig_gen.set_modulation_type(4)
        sig_gen.set_modulation_function(3)
        sig_gen.set_frequency(1e6)
        sig_gen.set_pulse_period(0.5)
        sig_gen.set_pulse_duty_factor(95)
        sig_gen.set_modulation_state(1)
        # # volt_0 = input('Starting Voltage Output (Vpp): ')
        volt_0 = 0.00001
        sig_gen.set_RF_amplitude(volt_0)
        sig_gen.display_status()
        print('-'*50)
        temp_0, _ = thermo.read_temp()
        print("{:<25} {:<10}".format('Current Temperature', temp_0))
        target_temp = float(input('Target Temperature (deg C): '))
        stim_duration = float(input('Stimulation Duration (sec): '))
        pid_controller = PID(0.500, 0.100, 0.000, setpoint=target_temp, sample_time=1, output_limits=(0.00001, 0.50000))
        input('Press [ENTER] to START ultrasound stimulation.')
        sig_gen.set_RF_state(1)
        t0 = time.time()
        time_data = []
        temp_data = []
        volt_data = []
        while time.time() - t0 < stim_duration:
            time_i = time.time() - t0
            temp_i, _ = thermo.read_temp()
            if temp_i > 50:
                print('Temp > 50...Skipping...')
                continue
            volt_i = pid_controller(temp_i)
            sig_gen.set_RF_amplitude(volt_i)
            time_data.append(time_i)
            temp_data.append(temp_i)
            volt_data.append(volt_i)
            print("{:<25} {:<15} {:<10}".format('Elapsed Time', 'Temperature', 'Voltage'))
            print("{:<25} {:<15} {:<10}".format(round(time.time() - t0, 1), temp_i, volt_i))
        
