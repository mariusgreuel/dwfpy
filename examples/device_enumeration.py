"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

devices = dwf.Device.enumerate()
print(f"Number of devices: {len(devices)}")

for device_index, device in enumerate(devices):
    print("------------------------------")
    print(f"Device {device_index + 1} :")
    print(f"\tName: {device.name} {device.serial_number}")
    print(f"\tID: {device.id} rev: {device.revision}")

    print("\tConfigurations:")
    for configuration_index, configuration in enumerate(device.configurations):
        print(
            f"\t{configuration_index}."
            f" \tAnalogIn: {configuration.analog_in_channel_count} x {configuration.analog_in_buffer_size}"
            f" \tAnalogOut: {configuration.analog_out_channel_count} x {configuration.analog_out_buffer_size}"
            f" \tDigitalIn: {configuration.digital_in_channel_count} x {configuration.digital_in_buffer_size}"
            f" \tDigitalOut: {configuration.digital_out_channel_count} x {configuration.digital_out_buffer_size}"
            f" \t {configuration.text_info}"
        )
