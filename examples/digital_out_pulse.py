"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    pattern = device.digital_output

    print("Generating 1ms pulse...")

    # CH1: low when not running, initialize high on start
    pattern[0].setup(idle_state="low", initial_state="high", low_counter=0, high_counter=0)

    # 1ms run, once
    pattern.setup(run_length=1e-3, repeat_count=1, start=True)

    input("Press Enter key to exit.")
