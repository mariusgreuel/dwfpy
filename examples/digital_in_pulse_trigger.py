"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import matplotlib.pyplot as plt
import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    logic = device.digital_input

    SAMPLE_COUNT = 2048

    # positive pulse of at least 5ms seconds on DIO-0
    logic.setup_more_trigger(channel=0, polarity='positive', more_than=5e-3)

    print('Waiting for acquisition...')
    samples = logic.single(
        sample_rate=20e3,
        sample_format=16,
        buffer_size=SAMPLE_COUNT,
        position=SAMPLE_COUNT / 8,
        configure=True,
        start=True,
    )
    print(f'Got {len(samples)} samples')

plt.axvline(x=SAMPLE_COUNT - SAMPLE_COUNT // 8, color='red')
plt.plot(samples, drawstyle='steps-post')
plt.show()
