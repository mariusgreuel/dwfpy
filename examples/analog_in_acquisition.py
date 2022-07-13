"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import matplotlib.pyplot as plt
import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    scope = device.analog_input

    print(f'Device buffer size: {scope.buffer_size_max}')

    print('Starting oscilloscope...')
    scope[0].setup(range=5, filter='decimate')
    scope.single(sample_rate=20e3, buffer_size=8192, configure=True, start=True)

    samples = scope[0].get_data()
    dc = sum(samples) / len(samples)
    print(f'DC: {dc}V')

plt.plot(samples, drawstyle='steps-post')
plt.show()
