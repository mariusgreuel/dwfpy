"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import matplotlib.pyplot as plt
import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    scope = device.analog_input
    wavegen = device.analog_output

    input("Connect waveform generator to oscilloscope:\n- W1 to 1+\n- GND to 1-\nPress Enter to continue...")

    print("Generating sine wave...")
    wavegen[0].setup("sine", frequency=1e3, amplitude=2, start=True)

    print("Starting oscilloscope...")
    scope[0].setup(range=5)
    scope.setup_edge_trigger(mode="normal", channel=0, slope="rising", level=0, hysteresis=0.01)
    recorder = scope.record(sample_rate=1e6, length=2e-3, configure=True, start=True)

    if recorder.lost_samples > 0:
        print("Samples lost, reduce sample rate.")
    if recorder.corrupted_samples > 0:
        print("Samples corrupted, reduce sample rate.")

    print(
        f"Processed {recorder.total_samples} samples total, "
        f"received {len(recorder.channels[0].data_samples)} samples."
    )

    channels = recorder.channels

for channel in channels:
    plt.plot(channel.data_samples, drawstyle="steps-post")

plt.show()
