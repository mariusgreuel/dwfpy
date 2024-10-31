"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import matplotlib.pyplot as plt
import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    logic = device.digital_input
    pattern = device.digital_output

    # for Digital Discovery bit order: DIO24:39; with 32 bit sampling [DIO24:39 + DIN0:15]
    logic.dio_first = True

    # setup a binary counter with 100MHz update rate
    for i in range(16):
        pattern.channels[i].setup(divider=1 << i, low_counter=1, high_counter=1)

    pattern.configure(start=True)

    print("Waiting for acquisition...")
    samples = logic.single(sample_rate=100e6, sample_format=16, buffer_size=1000, configure=True, start=True)
    print("done")

plt.plot(samples, drawstyle="steps-post")
plt.show()
