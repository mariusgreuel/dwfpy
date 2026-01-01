"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    analog_io = device.analog_io

    print("Press Ctrl+C to stop")
    while True:
        print("Device status:")
        analog_io.read_status()
        for channel in analog_io.channels:
            for node in channel.nodes:
                print(f"- Node[{channel.index}][{node.index}]: {node!r}: {node}")

        time.sleep(1)
