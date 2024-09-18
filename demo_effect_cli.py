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
This script provides a command-line interface to send effects
to the PixMob bracelets over IR directly from a Raspberry Pi.

Be sure to set your GPIO Pin in config file:
'pipyir/config.py'.
"""

import pipyir.ir  # Import the ir module
import pipyir.config as cfg  # Import configuration settings
from pipyir.effect_definitions import base_color_effects, tail_codes, special_effects
import time
import argparse
import logging
from typing import Optional


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)

LOG = logging.getLogger(__name__)

def print_help():
    """
    Prints the help message listing available commands and effects.
    """
    print(
        "Command syntax:",
        " BASE_EFFECT [TAIL_CODE]",
        " SPECIAL_EFFECT [TAIL_CODE]",
        "Base effects:",
        " ".join(base_color_effects.keys()),
        "",
        "Special effects:",
        " ".join(special_effects.keys()),
        "",
        "Tail codes:",
        " ".join(tail_codes.keys()),
        "",
        "Example:",
        " %s" % next(iter(base_color_effects.keys())),
        " %s %s"
        % (next(iter(base_color_effects.keys())), next(iter(tail_codes.keys()))),
        sep="\n",
    )

def send_effect(
    effect_code: str, tail_code: Optional[str] = None
):
    """
    Sends a single effect via IR.

    :param effect_code: The main effect code (string)
    :param tail_code: The tail code (string or None)
    """
    global ir_sender
    effect_bits = []

    effect_code = effect_code.upper().strip()

    if effect_code in base_color_effects:
        effect_bits = base_color_effects[effect_code]
    elif effect_code in special_effects:
        effect_bits = special_effects[effect_code]
    else:
        LOG.warning(
            "Invalid effect %s. See base_color_effects and "
            "special_effects in effect_definitions.py for options.",
            effect_code,
        )
        return

    # NOTE: Tail codes may not be compatible with special effects
    if tail_code is not None:
        tail_code = tail_code.upper().strip()

        if tail_code in tail_codes:
            effect_bits += tail_codes[tail_code]
        else:
            LOG.warning(
                "Invalid tail code %s. See tail_codes "
                "in effect_definitions.py for options.",
                tail_code,
            )

    # Send the effect_bits using ir_sender
    ir_sender.send_bits_command(effect_bits)

    # Small delay after each command
    time.sleep(cfg.WAIT_BEFORE_SEND + 0.0008 * len(effect_bits))

    if cfg.DEBUG:
        LOG.debug(
            "Sent effect: %s, %s.",
            effect_code,
            'no tail effect' if not tail_code else 'tail: ' + tail_code,
        )

def repl_commands():
    """
    Starts a REPL loop to accept user commands interactively.
    """
    print('Type "help" for a list of known commands, "exit" or "q" to quit.')
    while True:
        try:
            cmd = input("Command> ")
        except KeyboardInterrupt:
            break

        # Split by space to add tail command after base command.
        cmd = cmd.upper().split(" ")

        if cmd[0] == "EXIT" or cmd[0] == "Q":
            break

        if cmd[0] == "HELP":
            print_help()
            continue

        effect_code = cmd[0]
        tail_code = cmd[1] if len(cmd) > 1 else None
        send_effect(effect_code, tail_code=tail_code)

def main():
    """
    Main function to parse arguments and initiate command sending.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Simple command-line loop to send effects "
            "to the PixMob bracelet by typing in the effect names."
        )
    )
    parser.add_argument(
        "-c",
        "--continue-cli",
        action="store_true",
        default=False,
        help=(
            "Set to True if you are passing the effect in the "
            "command line, and want to still drop into the REPL."
        ),
    )

    parser.add_argument("effect", type=str, nargs="?")
    parser.add_argument("tail_code", type=str, nargs="?")

    args = parser.parse_args()

    try:
        if cfg.WAIT_BEFORE_SEND:
            time.sleep(2.5)

        # If user has provided effect in arguments, send it directly
        if args.effect is not None:
            send_effect(args.effect, tail_code=args.tail_code)
            # If the program should not go to the REPL after done, exit.
            if not args.continue_cli:
                return

        repl_commands()
    except Exception:
        LOG.exception("Uncaught exception occurred in the input loop. Full traceback:")
    finally:
        # Clean up
        ir_sender.cleanup()

if __name__ == "__main__":
    main()
