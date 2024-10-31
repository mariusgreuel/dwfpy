"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.AnalogDiscovery2() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    device.supplies.positive.setup(voltage=5)
    device.supplies.negative.setup(voltage=-5)
    device.supplies.master_enable = True

    print("Press Ctrl+C to stop")
    while True:
        time.sleep(1)

        device.analog_io.read_status()

        print(f"USB:\t{device.usb_voltage:.3f}V\t{device.usb_current:.3f}A")
        print(f"AUX:\t{device.aux_voltage:.3f}V\t{device.aux_current:.3f}A")

        if not device.supplies.master_enable_status:
            print("Power supplies stopped, restarting...")
            device.supplies.master_enable = False
            device.supplies.master_enable = True
