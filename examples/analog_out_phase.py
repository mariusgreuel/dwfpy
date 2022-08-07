"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

PARAMETERS = (
    (60.0, 1.0, 0.0),
    (60.0, 1.0, 30.0),
    (60.0, 1.5, 60.0),
    (90.0, 1.5, 90.0),
)

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

    for i, parameters in enumerate(PARAMETERS):
        frequency = parameters[0]
        amplitude = parameters[1]
        phase = parameters[2]
        print(f'Step {i+1}): {frequency}Hz, {amplitude}V, {phase}* ')
        wavegen[0].setup(frequency=frequency, amplitude=amplitude)
        wavegen[1].setup(frequency=frequency, amplitude=amplitude, phase=phase)

        if i == 0:
            wavegen[1].configure()
            wavegen[0].configure(start=True)
        else:
            wavegen[1].apply()
            wavegen[0].apply()

        time.sleep(5)

    print('done')
