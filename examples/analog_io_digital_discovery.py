"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f"DWF Version: {dwf.Application.get_version()}")

with dwf.DigitalDiscovery() as device:
    print(f"Found device: {device.name} ({device.serial_number})")

    # set digital voltage between 1.2 and 3.3V
    device.supplies.digital.setup(voltage=1.8)

    # enable VIO output
    device.supplies.master_enable = True

    # configure week pull for DIN lines, 0.0 low, 0.5 middle, 1 high
    device.din_pull_up_down = 0.5

    # pull enable for DIO 39 to 24, bit 15 to 0
    device.dio_pull_enable = 0x0081  # DIO7 and DIO0

    # pull up/down for DIO
    device.dio_pull_up_down = 0x0080  # DIO7 pull up and DIO0 pull down

    # drive strength for DIO lines: 0 (auto based on digital voltage), 2, 4, 6, 8, 12, 16 (mA)
    device.dio_drive_strength = 8

    # slew rate for DIO lines: 0 quietio, 1 slow, 2 fast
    device.dio_slew = 0

    print("Press Ctrl+C to stop")
    while True:
        time.sleep(1)

        device.analog_io.read_status()

        print(f"USB:\t{device.usb_voltage:.3f}V\t{device.usb_current:.3f}A")
        print(f"VIO:\t{device.vio_voltage:.3f}V\t{device.vio_current:.3f}A")

        if not device.supplies.master_enable_status:
            print("Power supplies stopped, restarting...")
            device.supplies.master_enable = False
            device.supplies.master_enable = True
