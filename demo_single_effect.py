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
This script lets you send a single command to
bracelets over IR directly from a Raspberry Pi.

Be sure to set your GPIO Pin in config file:
'pipyir/config.py'.
"""
import pipyir.config as cfg  # Import configuration settings
import pipyir.ir  # Import the ir module
from pipyir.effect_definitions import base_color_effects, tail_codes, special_effects
import time

# Which effect/color to display on the lights. See base_color_effects or special_effects in effect_definitions.py for options.
MAIN_EFFECT = "BLUE"

# Optional, set to None if not using. Can use this to modify simple color effects by making them fade in and/or out
# and/or making them display probabilistically. See tail_codes in effect_definitions.py for options.
# WARNING: NOT ALL TAIL CODES ARE COMPATIBLE WITH ALL BRACELETS AND COLORS. It may take some trial and error.
TAIL_CODE = "FADE_2"

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
                            "effect_definitions.py. Set TAIL_CODE to None or choose a MAIN_EFFECT from base_color_effects "
                            "(instead of special_effects).")
    else:
        raise Exception("Invalid MAIN_EFFECT. See base_color_effects and special_effects in effect_definitions.py for "
                        "options.")

    # Send the effect_bits using ir_sender
    ir_sender.send_bits_command(effect_bits)

    # Wait for enough time for the Raspberry Pi to transmit this code
    time.sleep(cfg.WAIT_BEFORE_SEND + 0.0008 * len(effect_bits))

    if cfg.DEBUG:
        print(f"Sent effect: {main_effect}, {'no tail effect' if not tail_code else 'tail: ' + tail_code}.")

# Send the effect
send_effect(MAIN_EFFECT, TAIL_CODE)

# Clean up
ir_sender.cleanup()
print("Command sent via IR.")
