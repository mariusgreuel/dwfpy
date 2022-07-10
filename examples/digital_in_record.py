"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import matplotlib.pyplot as plt
import dwfpy as dwf

SAMPLE_RATE = 100e3
SAMPLE_COUNT = 100e3

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    logic = device.digital_input
    pattern = device.digital_output

    # setup a binary counter with 100kHz update rate
    counter = round(pattern.clock_frequency / SAMPLE_RATE)

    for i in range(16):
        pattern.channels[i].setup(divider=1 << i, low_counter=counter, high_counter=counter)

    pattern.configure(start=True)

    # for Digital Discovery bit order: DIO24:39; with 32 bit sampling [DIO24:39 + DIN0:15]
    logic.dio_first = True

    # trigger when all digital pins are low
    logic.setup_trigger(source='detector-digital-in')
    logic.trigger.set_trigger_mask(low_level=0xFFFF)

    print('Recording...')
    recorder = logic.record(
        sample_rate=SAMPLE_RATE,
        sample_format=16,
        sample_count=SAMPLE_COUNT // 2,
        prefill=SAMPLE_COUNT // 2,
        configure=True,
        start=True)
    print('done')

    if recorder.lost_samples > 0:
        print('Samples lost, reduce sample rate.')
    if recorder.corrupted_samples > 0:
        print('Samples corrupted, reduce sample rate.')

    print(f'Processed {recorder.total_samples} samples total, received {len(recorder.data_samples)} samples.')

    samples = recorder.data_samples

plt.axvline(x=SAMPLE_COUNT / 2, color='red')
plt.plot(samples, drawstyle='steps-post')
plt.show()
