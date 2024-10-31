"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    pattern = device.digital_output
    channel = pattern[0]

    print("Generating PWM signal...")
    channel.setup_clock(frequency=1000, duty_cycle=1.23, configure=True, start=True)

    total_count = channel.low_counter + channel.high_counter
    print(f"Actual frequency: {pattern.clock_frequency / total_count / channel.divider}Hz")
    print(f"Actual duty-cycle: {100 * channel.high_counter / total_count:3f}%")
    print(f"Actual divider: {channel.divider}")

    input("Press Enter key to exit.")
