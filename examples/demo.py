"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

with dwf.Device() as device:
    print("Generating a 1kHz sine wave on WaveGen channel 1...")
    device.analog_output["ch1"].setup("sine", frequency=1e3, amplitude=1, start=True)
    input("Press Enter key to exit.")
