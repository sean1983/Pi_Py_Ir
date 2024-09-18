
"""
This module provides the IRSender class for sending IR signals using the Raspberry Pi GPIO pins.
Configuration settings are loaded from 'pipyir/config.py'.
The IRSender class uses the 'pigpio' library to generate accurate waveforms for IR communication.
It also provides the bits_to_run_lengths_pulses function for converting bits to run lengths.
"""

import time
import pigpio
import pipyir.config as cfg  # Import configuration settings

def group_by(iterable):

    """
    Groups consecutive elements in an iterable that are the same.

    :param iterable: Iterable of bits (0s and 1s)
    :return: List of tuples containing the bit and the group of bits
    """
    result = []
    current_group = []
    current_value = None

    for item in iterable:
        if current_value is None or item != current_value:
            if current_group:
                result.append((current_value, current_group))
            current_group = [item]
            current_value = item
        else:
            current_group.append(item)

    if current_group:
        result.append((current_value, current_group))

    return result

def bits_to_run_lengths_pulses(bit_list):
    """
    Converts a list of bits into run lengths by counting consecutive bits.

    :param bit_list: List of bits (0s and 1s)
    :return: List of run lengths
    """
    run_lengths = []
    for _, group in group_by(bit_list):
        run_lengths.append(len(group))
    return run_lengths

class IRSender:
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("Failed to connect to pigpio daemon")
        self.IR_GPIO = cfg.IR_GPIO
        self.pi.set_mode(self.IR_GPIO, pigpio.OUTPUT)
        if cfg.DEBUG:
            print(f"IRSender initialized on GPIO pin {self.IR_GPIO}")

    def send_raw_ir_command(self, run_lengths):
        """
        Generates and sends the IR waveform based on run lengths of bits.

        :param run_lengths: List of run lengths corresponding to marks and spaces
        """
        unit = cfg.PULSE_LENGTH  # Use PULSE_LENGTH from config
        carrier_freq = cfg.CARRIER_FREQUENCY  # Use CARRIER_FREQUENCY from config
        carrier_period = 1e6 / carrier_freq  # in microseconds
        carrier_half_period = carrier_period / 2  # in microseconds

        wave = []
        for idx, duration_units in enumerate(run_lengths):
            duration_us = duration_units * unit
            if idx % 2 == 0:
                # Mark: carrier on
                num_cycles = int(duration_us / carrier_period)
                for _ in range(num_cycles):
                    wave.append(pigpio.pulse(1 << self.IR_GPIO, 0, int(carrier_half_period)))
                    wave.append(pigpio.pulse(0, 1 << self.IR_GPIO, int(carrier_half_period)))
                remaining_time = duration_us - (num_cycles * carrier_period)
                if remaining_time > 0:
                    wave.append(pigpio.pulse(1 << self.IR_GPIO, 0, int(remaining_time)))
            else:
                # Space: carrier off
                wave.append(pigpio.pulse(0, 0, int(duration_us)))

        # Send the waveform
        self.pi.wave_add_generic(wave)
        wid = self.pi.wave_create()
        if wid >= 0:
            self.pi.wave_send_once(wid)
            while self.pi.wave_tx_busy():
                time.sleep(0.001)
            self.pi.wave_delete(wid)
            if cfg.DEBUG:
                print(f"IR command sent with waveform ID {wid}")
        else:
            print("Error creating wave")

    def send_bits_command(self, bit_list):
        """
        Converts a bit list into run_lengths and sends the corresponding IR command.

        :param bit_list: List of bits (0s and 1s)
        """
        run_lengths = bits_to_run_lengths_pulses(bit_list)
        if cfg.DEBUG:
            print(f"Sending bits: {bit_list}")
            print(f"Run lengths: {run_lengths}")
        self.send_raw_ir_command(run_lengths)

    def send_multiple_commands(self, command_list):
        """
        Sends multiple IR commands.

        :param command_list: List of bit lists
        """
        for command in command_list:
            self.send_bits_command(command)

    def cleanup(self):
        """
        Cleans up the pigpio resources.
        """
        self.pi.stop()
        if cfg.DEBUG:
            print("IRSender cleaned up and pigpio connection closed.")
