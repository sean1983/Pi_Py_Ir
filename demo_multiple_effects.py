# Pi Py Ir - Raspberry Pi PixMob Python IR Transmitter
# 
# A Python-based IR transmitter solution  for the Raspberry Pi.
# It allows you to control PixMob bracelets directly using Python scripts,
# eliminating the need for additional hardware like an Arduino.
#
# Requirements
# - Raspberry Pi 3 (or later model)
# - IR LED connected to a GPIO pin on the Raspberry Pi
#   A current-limiting resistor & NPN Transistor to drive the IR LED
# - PixMob Bracelets compatible with IR control
#
# Libraries
# - pigpio, argparse, logging
#
# Acknowledgments
#   Special thanks to:
#   - Wouter De Droog	https://github.com/wouterdedroog)
#   - Daniel Weidman	https://github.com/danielweidman)
#   - Zach Resmer		https://github.com/zacharesmer)
"""
This script lets you send a series of light effect commands
with customizable timings over IR directly from a Raspberry Pi.

Be sure to set your GPIO Pin in config file:
'pipyir/config.py'.
"""
import pipyir.config as cfg  # Import configuration settings
import pipyir.ir  # Import the ir module
from pipyir.effect_definitions import base_color_effects, tail_codes, special_effects
import time

# List of all effects you want to display, in order. Each entry has the effect name, optional tail code, and
# duration to wait before sending next effect. Note that some effects are long, and the bracelets might not respond
# to an effect until the current one is finished, so don't set your durations to less than the time it takes for the
# bracelets to show the effects.
EFFECTS_TO_SHOW = [
    {
        "main_effect": "RED",
        "tail_code": None,
        "duration": 0.8
    },
    {
        "main_effect": "GREEN",
        "tail_code": None,
        "duration": 0.8
    },
    {
        "main_effect": "BLUE",
        "tail_code": None,
        "duration": 0.8
    },
    {
        "main_effect": "TURQUOISE",
        "tail_code": "FADE_1",
        "duration": 3.5
    },
    {
        "main_effect": "YELLOW",
        "tail_code": "FADE_2",
        "duration": 3
    },
    {
        "main_effect": "MAGENTA",
        "tail_code": "FADE_5",
        "duration": 4
    },
    {
        "main_effect": "SLOW_ORANGE",
        "tail_code": None,
        "duration": 5
    },
]

#################################
# Initialize the IRSender
ir_sender = pipyir.ir.IRSender()

def send_effect(main_effect, tail_code):
    """
    Sends a single effect via IR.

    :param main_effect: The main effect name (string)
    :param tail_code: The tail code name (string or None)
    """
    if main_effect in base_color_effects:
        effect_bits = base_color_effects[main_effect]
        if tail_code:
            if tail_code in tail_codes:
                effect_bits += tail_codes[tail_code]
            else:
                raise Exception("Invalid tail code name. See tail_codes in effect_definitions.py for options.")
    elif main_effect in special_effects:
        effect_bits = special_effects[main_effect]
        if tail_code:
            raise Exception("Tail code effects only supported on simple color effects found in base_color_effects of "
                            "effect_definitions.py. Set tail_code to None or choose a main_effect from base_color_effects "
                            "(instead of special_effects).")
    else:
        raise Exception("Invalid main_effect. See base_color_effects and special_effects in effect_definitions.py for "
                        "options.")

    # Send the effect_bits using ir_sender
    ir_sender.send_bits_command(effect_bits)

    # Wait for enough time for the Raspberry Pi to transmit this code
    time.sleep(cfg.WAIT_BEFORE_SEND + 0.0008 * len(effect_bits))

    if cfg.DEBUG:
        print(f"Sent effect: {main_effect}, {'no tail effect' if not tail_code else 'tail: ' + tail_code}.")

for effect_instance in EFFECTS_TO_SHOW:
    send_effect(effect_instance.get("main_effect"), effect_instance.get("tail_code", None))
    time.sleep(effect_instance["duration"])

# Clean up
ir_sender.cleanup()
