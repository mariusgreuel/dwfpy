"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    device.auto_configure = False
    pattern = device.digital_output

    # 1kHz pulse on IO pin 0
    pattern[0].setup_clock(frequency=1e3)

    # 1kHz 25% duty pulse on IO pin 1
    pattern[1].setup_clock(frequency=1e3, duty_cycle=25)

    # 2kHz random on IO pin 2
    pattern[2].setup_random(frequency=2e3)

    # 10kHz sample rate custom on IO pin 3
    data = bytes((0xFF, 0x80, 0xC0, 0xE0, 0xF0, 0x00))
    pattern[3].setup_custom(frequency=10e3, data=data)

    print('Generating output...')
    pattern.configure(start=True)

    input('Press Enter key to exit.')
