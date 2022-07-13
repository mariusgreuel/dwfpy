"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

print(f'DWF Version: {dwf.Application.get_version()}')

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    print('Configuring UART...')
    uart = device.protocols.uart
    uart.setup(pin_rx=0, pin_tx=1, rate=9600, data_bits=8, stop_bits=1, parity='n')

    print('Sending on TX...')
    uart.write(b'Hello\r\n')

    print('Receiving on RX, press Ctrl+C to stop...')

    while True:
        time.sleep(0.01)
        rx, parity = uart.read()
        if len(rx) > 0:
            print(rx.decode('ascii'), end='', flush=True)
        if parity != 0:
            print(f'Parity error {parity}')
