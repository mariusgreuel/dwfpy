"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    print("Generating a 1kHz sine wave on WaveGen channel 1...")
    device.analog_output["ch1"].setup("sine", frequency=1e3, amplitude=0.1, start=True)
    input("Press Enter key to exit.")
