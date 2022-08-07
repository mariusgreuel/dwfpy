"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    pattern = device.digital_output
    channel1 = pattern[0]

    print(
        'Generating on 2 pins phase 180* with different initial low and high polarity, for 5 seconds...'
    )
    pattern[0].setup_clock(frequency=1e6)
    pattern[1].setup_clock(frequency=1e6, phase=180)
    pattern.configure(start=True)
    input('Press Enter key to continue.')

    print('Generating on 3 pins 3 phases with different initial counter values, for 5 seconds...')
    pattern[0].setup_clock(frequency=1e6, phase=0)
    pattern[1].setup_clock(frequency=1e6, phase=240)
    pattern[2].setup_clock(frequency=1e6, phase=120)
    pattern.configure(start=True)
    input('Press Enter key to continue.')

    print('Generating on 4 pins 4 phases with different initial counter values, for 5 seconds...')
    pattern[0].setup_clock(frequency=1e6, phase=0)
    pattern[1].setup_clock(frequency=1e6, phase=-90)
    pattern[2].setup_clock(frequency=1e6, phase=-180)
    pattern[3].setup_clock(frequency=1e6, phase=-270)
    pattern.configure(start=True)
    input('Press Enter key to exit.')
