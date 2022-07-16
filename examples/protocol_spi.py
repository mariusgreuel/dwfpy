"""
DWF Python Example

This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
"""

import time
import dwfpy as dwf

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    print('Configuring SPI...')
    spi = device.protocols.spi
    spi.setup(pin_select=0, pin_clock=1, pin_mosi=2, pin_miso=3, frequency=1e3)
    spi.set_idle(0, dwf.DigitalOutputIdle.ZET)  # 0 DQ0_MOSI_SISO = DwfDigitalOutIdleZet
    spi.set_idle(0, dwf.DigitalOutputIdle.ZET)  # 1 DQ1_MISO = DwfDigitalOutIdleZet

    # CS DIO-0 high
    spi.select(1)

    # start driving the channels, clock and data
    spi.write_one(0, bits_per_word=0)

    time.sleep(1)

    tx = bytes((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))

    # CS DIO-0 low
    spi.select(0)

    # write to MOSI and read from MISO
    rx = spi.write_read(buffer=tx, words_to_receive=10)

    print(f'TX: {list(tx)}')
    print(f'RX: {list(rx)}')

    # CS DIO-0 high
    spi.select(1)

    # write 1 byte to MOSI
    spi.write_one(0xAB)

    # read 24 bits from MISO
    data = spi.read_one(bits_per_word=24)

    # write array of 8 bit (byte) length elements
    spi.write(tx)

    # read array of 8 bit (byte) length elements
    rx = spi.read(words_to_receive=10)
    print(f'RX: {list(rx)}')
