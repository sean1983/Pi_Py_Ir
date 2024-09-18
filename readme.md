## ***Pi Py Ir*** - RPi Pixmob Python IR Transmitter

### Overview

**Pi Py Ir** is a Python-based IR (Infrared) transmitter solution for the Raspberry Pi. It allows you to control PixMob bracelets directly from a Raspberry Pi using Python scripts, eliminating the need for additional hardware like an Arduino. By utilizing the Raspberry Pi's GPIO pins and the `pigpio` library for precise timing, Pi Py Ir can send IR signals to PixMob bracelets to display various light effects.

The project includes a set of Python scripts and modules:

- **pipyir**: A Python module that handles IR signal generation and transmission using the Raspberry Pi's GPIO pins.
- **Effect Scripts**: Scripts like `demo_send_multiple_effects_advanced.py`, `demo_multiple_effects.py`, and `demo_single_effect.py` demonstrate how to send single or multiple effects to PixMob bracelets.
- **Command-Line Interface**: A script (`command_line_ir.py`) that provides an interactive command-line interface to send effects in real-time.

Pi Py Ir supports sending predefined light effects, including base colors, special effects, and tail codes for PixMob bracelets. The effects are defined in the `effect_definitions.py` file and can be customized as needed.

### Requirements

#### Hardware

- **Raspberry Pi 3** (or later model)
- **IR LED** connected to a GPIO pin on the Raspberry Pi (with appropriate current-limiting resistor)
- **Transistor** (e.g., NPN transistor like 2N2222 or a MOSFET) to drive the IR LED if necessary
- **PixMob Bracelets** compatible with IR control

#### Software

- **Raspbian OS** (or any Raspberry Pi-compatible Linux distribution)
- **Python 3** installed on the Raspberry Pi
- **pigpio Library** for accurate GPIO control and timing
  - Install with: `sudo apt-get install pigpio python-pigpio python3-pigpio`
  - Start the pigpio daemon: `sudo pigpiod`
- **pipyir Module** (included in this project)
- **Access to GPIO Pins** (may require running scripts with `sudo`)

#### Additional Python Modules

- **argparse**
- **logging**

These modules are part of the Python Standard Library and should be available by default.

#### Setup and Configuration

- Ensure the `pipyir` folder is in the same directory as your scripts or is included in your `PYTHONPATH`.
- Configure settings like GPIO pin numbers, pulse lengths, and carrier frequency in `pipyir/config.py`.
- Update effect definitions in `pipyir/effect_definitions.py` as needed.

---

### Acknowledgments

#### Special thanks to:
- Wouter De Droog [@wouterdedroog](https://github.com/wouterdedroog)
- Daniel Weidman [@danielweidman](https://github.com/danielweidman)
- Zach Resmer [@zacharesmer](https://github.com/zacharesmer)