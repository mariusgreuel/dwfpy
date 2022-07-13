"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.AnalogDiscovery2() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    print('Device temperature and USB/AUX supply voltage and current')

    print('Press Ctrl+C to stop')
    while True:
        time.sleep(1)

        device.analog_io.read_status()

        print(f'Temperature: {device.temperature}*C')
        print(f'USB:\t{device.usb_voltage:.3f}V\t{device.usb_current:.3f}A')
        print(f'AUX:\t{device.aux_voltage:.3f}V\t{device.aux_current:.3f}A')
