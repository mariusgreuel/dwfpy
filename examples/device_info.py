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
    print(f"\tName: {device.name}")
    print(f"\tSerial number: {device.serial_number}")

    with device:
        try:
            scope = device.analog_input
            print()
            print(f"AnalogIn channels: {len(scope.channels)}")
            print(f"\tBuffer size: {scope.buffer_size_max}")
            print(f"\tADC bits: {scope[0].adc_bits}")
            print(f"\tRange from {scope[0].range_min} to {scope[0].range_max} in {scope[0].range_steps} steps")
            print(f"\tOffset from {scope[0].offset_min} to {scope[0].offset_max} in {scope[0].offset_steps} steps")
        except dwf.FeatureNotSupportedError:
            pass

        try:
            wavegen = device.analog_output
            print()
            print(f"AnalogOut channels: {len(wavegen.channels)}")
            for channel_index, channel in enumerate(wavegen.channels):
                print(f"\tChannel {channel_index + 1} :")
                for node_index, node in enumerate(channel.nodes):
                    print(f"\t\tNode {node_index + 1} :")
                    print(f'\t\t\tName: {["Carrier", "FM", "AM"][node.type]}')
                    print(f"\t\t\tBuffer size: {node.data_samples_max}")
                    print(f"\t\t\tAmplitude from {node.amplitude_min} to {node.amplitude_max}")
                    print(f"\t\t\tOffset from {node.offset_min} to {node.offset_max}")
                    print(f"\t\t\tFrequency from {node.frequency_min} to {node.frequency_max}")
        except dwf.FeatureNotSupportedError:
            pass

        try:
            io = device.analog_io
            print()
            print(f"AnalogIO channels: {len(io.channels)}")
            print(f"\tCan set master_enable: {io.master_enable_can_set}")
            print(f"\tCan read master_enable: {io.master_enable_can_read}")
            for channel_index, channel in enumerate(io.channels):
                print(f"\tChannel {channel_index + 1} :")
                print(f"\t\tName: {channel.name}")
                print(f"\t\tLabel: {channel.label}")
                for node_index, node in enumerate(channel.nodes):
                    print(f"\t\tNode {node_index + 1} :")
                    print(f"\t\t\tName: {node.name}")
                    print(f"\t\t\tUnit: {node.unit}")

                    if node.value_steps == 1:
                        if node.value_min == node.value_max:
                            print(f"\t\t\tConstant output: {node.value_min}")
                        else:
                            print(f"\t\t\tNon settable range from {node.value_min} to {node.value_max}")
                    elif node.value_steps > 1:
                        print(f"\t\t\tSetting from {node.value_min} to {node.value_max} in {node.value_steps} steps")

                    if node.status_steps == 1:
                        if node.status_min == node.status_max:
                            print(f"\t\t\tConstant input: {node.status_min}")
                        else:
                            print(f"\t\t\tInput range from {node.status_min} to {node.status_max}")
                    elif node.status_steps > 1:
                        print(f"\t\t\tReading from {node.status_min} to {node.status_max} in {node.status_steps} steps")
        except dwf.FeatureNotSupportedError:
            pass

        try:
            logic = device.digital_input
            print()
            print(f"DigitalIn channels: {len(logic.channels)}")
            print(f"\tBuffer size: {logic.buffer_size_max}")
        except dwf.FeatureNotSupportedError:
            pass

        try:
            pattern = device.digital_output
            print()
            print(f"DigitalOut channels: {len(pattern.channels)}")
            print(f"\tCustom size: {pattern[0].max_bits}")
        except dwf.FeatureNotSupportedError:
            pass

        try:
            io = device.digital_io
            print()
            print(f"DigitalIO channels: {len(io.channels)}")
            print(f"\tOE Mask: {hex(io.output_enable_mask)}")
            print(f"\tOutput : {hex(io.output_state_mask)}")
            print(f"\tInput  : {hex(io.input_state_mask)}")
        except dwf.FeatureNotSupportedError:
            pass
