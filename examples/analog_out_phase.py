"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

FREQUENCY = [60.0, 60.0, 60.0, 90.0]
AMPLITUDE = [1.0, 1.0, 1.5, 1.5]
PHASE = [0.0, 30.0, 60.0, 90.0]

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    device.auto_configure = False

    wavegen = device.analog_output

    # enable two channels
    wavegen[0].setup(function='sine')
    wavegen[1].setup(function='sine')

    # for second channel set master the first channel
    wavegen[1].master = 0

    # slave channel is controlled by the master channel

    for i in range(len(FREQUENCY)):
        print(f'Step {i+1}): {FREQUENCY[i]}Hz, {AMPLITUDE[i]}V, {PHASE[i]}* ')
        wavegen[0].setup(frequency=FREQUENCY[i], amplitude=AMPLITUDE[i])
        wavegen[1].setup(frequency=FREQUENCY[i], amplitude=AMPLITUDE[i], phase=PHASE[i])

        if i == 0:
            wavegen[1].configure()
            wavegen[0].configure(start=True)
        else:
            wavegen[1].apply()
            wavegen[0].apply()

        time.sleep(5)

    print('done')
