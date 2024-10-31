"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.AnalogDiscovery() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    device.supplies.positive.setup()
    device.supplies.negative.setup()
    device.supplies.master_enable = True

    print("Press Ctrl+C to stop")
    while True:
        time.sleep(1)

        device.analog_io.read_status()

        supply_power = device.supplies.regulator_voltage * device.supplies.regulator_current
        print(f"Total supply power: {supply_power}W")

        Load_percentage = 100 * (device.supplies.regulator_current / 0.2)
        print(f"Load: {Load_percentage}%")

        if not device.supplies.master_enable_status:
            print("Power supplies stopped, restarting...")
            device.supplies.master_enable = False
            device.supplies.master_enable = True
