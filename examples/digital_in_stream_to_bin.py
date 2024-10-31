"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

FILENAME = "temp_recording.bin"
SAMPLE_RATE = 1e6
SAMPLE_COUNT = 1e6

with dwf.Device() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    logic = device.digital_input
    pattern = device.digital_output

    # setup a binary counter
    counter = round(pattern.clock_frequency / SAMPLE_RATE)

    for i in range(16):
        pattern.channels[i].setup(divider=1 << i, low_counter=counter, high_counter=counter)

    pattern.setup(start=True)

    # for Digital Discovery bit order: DIO24:39; with 32 bit sampling [DIO24:39 + DIN0:15]
    logic.dio_first = True

    print(f"Creating '{FILENAME}'...")
    with open(FILENAME, "wb") as bin_file:

        def callback(recorder: dwf.DigitalRecorder) -> bool:
            """Recorder callback"""
            if recorder.lost_samples > 0:
                raise RuntimeError("Samples lost, reduce sample rate.")
            if recorder.corrupted_samples > 0:
                raise RuntimeError("Samples corrupted, reduce sample rate.")

            bin_file.write(recorder.data_samples)

            if recorder.total_samples < SAMPLE_COUNT:
                return True

            print(
                f"Status: {recorder.status}, "
                f"lost={recorder.lost_samples}, "
                f"corrupted={recorder.corrupted_samples}, "
                f"total={recorder.total_samples}"
            )

            return False

        print(f"Streaming data for {SAMPLE_COUNT / SAMPLE_RATE}s...")
        logic.stream(callback=callback, sample_rate=SAMPLE_RATE, sample_format=16, configure=True, start=True)
