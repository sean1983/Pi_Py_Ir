"""
Configuration settings for the pipyir module.
"""

# GPIO pin connected to the IR LED
IR_GPIO = 17  # Adjust this to the GPIO pin you're using

# Time to wait after sending, before next action (in seconds)
WAIT_BEFORE_SEND = 0.01

# Base unit time for pulses (in microseconds)
PULSE_LENGTH = 700  # Base unit in microseconds

# Carrier frequency for IR signal (in Hz)
CARRIER_FREQUENCY = 38000  # 38kHz carrier frequency

# Whether to print debug statements
DEBUG = True
