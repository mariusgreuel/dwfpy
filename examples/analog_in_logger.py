"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import numpy as np
import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    print('Connect Waveform Generator output 1 to Oscilloscope input 1: W1 to 1+, GND to 1-')

    print('Generating AM sine wave...')
    wavegen = device.analog_output
    wavegen[0].setup(function='sine', frequency=50, amplitude=1, offset=0.5)
    wavegen[0].setup_am(function='triangle', frequency=0.1, amplitude=50)
    wavegen[0].configure(start=True)

    scope = device.analog_input
    scope[0].setup(range=50)
    scope[1].setup(range=50)
    scope.scan_shift(sample_rate=4096, buffer_size=4096, configure=True, start=True)

    print('Press Ctrl+C to stop')
    while True:
        time.sleep(1)

        status = scope.read_status(read_data=True)

        for channel in scope.channels:
            samples = np.array(channel.get_data())
            dc = np.average(samples)
            dcrms = np.sqrt(np.average(samples**2))
            acrms = np.sqrt(np.average((samples - dc) ** 2))
            print(f'CH{channel.index + 1}: DC:{dc:.3f}V DCRMS:{dcrms:.3f}V ACRMS:{acrms:.3f}V')
