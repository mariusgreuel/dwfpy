"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    print('Configuring I2C...')
    i2c = device.protocols.i2c

    # SCL=DIO-0, SDA=DIO-1, 100kHz
    i2c.setup(pin_scl=0, pin_sda=1, rate=1e5)

    bus_is_free = i2c.clear()
    if not bus_is_free:
        raise RuntimeError('I2C bus error. Check the pull-ups.')

    time.sleep(1)

    tx_buffer = bytes((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))

    print('Separate write and read...')
    i2c.write(address=0x1D << 1, buffer=tx_buffer)
    rx, nak_index = i2c.read(address=0x1D << 1, bytes_to_read=16)
    if nak_index != 0:
        print(f'NAK={nak_index}')
    print(f'RX: {list(rx)}')

    print('Write and read with restart...')
    rx, nak_index = i2c.write_read(address=0x1D << 1, buffer=tx_buffer[:1], bytes_to_read=16)
    if nak_index != 0:
        print(f'NAK={nak_index}')
    print(f'RX: {list(rx)}')
