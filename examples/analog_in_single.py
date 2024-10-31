"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    scope = device.analog_input
    wavegen = device.analog_output

    input("Connect waveform generator to oscilloscope:\n- W1 to 1+\n- GND to 1-\nPress Enter to continue...")

    print("Generating square wave...")
    wavegen[0].setup("square", frequency=11, amplitude=1, offset=1, start=True)

    print("Starting repeated acquisitions...")
    scope[0].setup(range=5)
    scope.setup_edge_trigger(mode="normal", channel=0, slope="rising", level=0.5, hysteresis=0.01)
    scope.single(sample_rate=20e6, buffer_size=8192, configure=True, start=True)

    for i in range(10):
        scope.wait_for_status(dwf.Status.DONE, read_data=True)
        samples = scope[0].get_data()
        dc = sum(samples) / len(samples)
        print(f"Acquisition #{i} average: {dc}V")
