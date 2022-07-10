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

    # configure DIO-0 as 1kHz clock
    pattern[0].setup_clock(frequency=1e3, configure=True, start=True)

    # DIO-1 low
    device.digital_io[1].setup(state=False, configure=True)

    input('Press Enter key to exit.')
