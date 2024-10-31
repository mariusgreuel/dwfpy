"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    device.auto_configure = False
    pattern = device.digital_output

    print(f"Internal frequency is {pattern.clock_frequency / 1e6}MHz")

    print("Generating binary counter with 100kHz update rate...")
    counter = round(pattern.clock_frequency / 100e3)

    for i in range(16):
        pattern.channels[i].setup(divider=1 << i, low_counter=counter, high_counter=counter)

    pattern.configure(start=True)

    input("Press Enter key to exit.")
