"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.ElectronicsExplorer() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    device.supplies.fixed.setup(voltage=3.3)
    device.supplies.positive.setup(voltage=6.0, current_limit=0.5)
    device.supplies.negative.setup(voltage=-6.0, current_limit=-0.5)
    device.supplies.reference1.setup(voltage=7.0)
    device.supplies.reference2.setup(voltage=-7.0)
    device.supplies.master_enable = True

    print("Press Ctrl+C to stop")
    while True:
        time.sleep(1)

        device.analog_io.read_status()

        print(f"VCC:\t{device.supplies.fixed.voltage:.3f}V\t{device.supplies.fixed.current:.3f}A")
        print(f"VP+:\t{device.supplies.positive.voltage:.3f}V\t{device.supplies.positive.current:.3f}A")
        print(f"VP-:\t{device.supplies.negative.voltage:.3f}V\t{device.supplies.negative.current:.3f}A")

        vmtr = device.voltmeters
        print(
            f"Vmtr1-4:"
            f"\t{vmtr.voltmeter1:.3f}V"
            f"\t{vmtr.voltmeter2:.3f}V"
            f"\t{vmtr.voltmeter3:.3f}V"
            f"\t{vmtr.voltmeter4:.3f}V"
        )
