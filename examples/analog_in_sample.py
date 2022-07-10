"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    print('Preparing to read sample...')
    scope = device.analog_input
    scope[0].setup(range=50)
    scope[1].setup(range=50)
    scope.configure()

    print('Press Ctrl+C to stop')

    while True:
        time.sleep(1)

        scope.read_status()

        for channel in scope.channels:
            print(f'CH{channel.index + 1}: {channel.get_sample()}V')
