"""
Protocols module for Digilent WaveForms devices.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
from typing import Optional, Tuple
from . import bindings as api
from .helpers import Helpers


class Protocols:
    """Digital Protocols module."""

    class Uart:
        """UART protocol."""

        def __init__(self, device):
            self._device = device
            self._pin_tx = None
            self._pin_rx = None
            self._rate = None
            self._data_bits = None
            self._stop_bits = None
            self._parity = None

        @property
        def pin_rx(self) -> Optional[int]:
            """Gets or sets the DIO channel to use for reception."""
            return self._pin_rx

        @pin_rx.setter
        def pin_rx(self, value: int) -> None:
            self._pin_rx = value
            api.dwf_digital_uart_rx_set(self._device.handle, value)

        @property
        def pin_tx(self) -> Optional[int]:
            """Gets or sets the DIO channel to use for transmission."""
            return self._pin_tx

        @pin_tx.setter
        def pin_tx(self, value: int) -> None:
            self._pin_tx = value
            api.dwf_digital_uart_tx_set(self._device.handle, value)

        @property
        def rate(self) -> float:
            """Gets or sets the baud rate."""
            return self._rate

        @rate.setter
        def rate(self, value: float) -> None:
            self._rate = value
            api.dwf_digital_uart_rate_set(self._device.handle, value)

        @property
        def data_bits(self) -> Optional[int]:
            """Gets or sets the number of data bits."""
            return self._data_bits

        @data_bits.setter
        def data_bits(self, value: int) -> None:
            self._data_bits = value
            api.dwf_digital_uart_bits_set(self._device.handle, value)

        @property
        def stop_bits(self) -> float:
            """Gets or sets the number of stop bits."""
            return self._stop_bits

        @stop_bits.setter
        def stop_bits(self, value: float) -> None:
            self._stop_bits = value
            api.dwf_digital_uart_stop_set(self._device.handle, value)

        @property
        def parity(self) -> str:
            """Gets or sets the parity."""
            return self._parity

        @parity.setter
        def parity(self, value: str) -> None:
            self._parity = value
            api.dwf_digital_uart_parity_set(self._device.handle, self._map_parity(value))

        def reset(self) -> None:
            """Resets the UART configuration to default value."""
            api.dwf_digital_uart_reset(self._device.handle)
            self._pin_tx = None
            self._pin_rx = None
            self._rate = None
            self._data_bits = None
            self._stop_bits = None
            self._parity = None

        def setup(
                self,
                pin_rx=None,
                pin_tx=None,
                rate=9600,
                data_bits=8,
                stop_bits=1,
                parity='n') -> None:
            """Sets up the UART configuration."""
            if pin_rx is not None:
                self.pin_rx = pin_rx
            if pin_tx is not None:
                self.pin_tx = pin_tx
            if rate is not None:
                self.rate = rate
            if data_bits is not None:
                self.data_bits = data_bits
            if stop_bits is not None:
                self.stop_bits = stop_bits
            if parity is not None:
                self.parity = parity
            if pin_rx is not None:
                api.dwf_digital_uart_rx(self._device.handle, None, 0)
            if pin_tx is not None:
                api.dwf_digital_uart_tx(self._device.handle, None, 0)

        def read(self, buffer_size=8192) -> Tuple[bytes, int]:
            """Returns the received characters since the last call.
            Returns (rx_buffer, parity)."""
            c_buffer = (ctypes.c_char * buffer_size)()
            count, parity = api.dwf_digital_uart_rx(self._device.handle, c_buffer, len(c_buffer))
            return bytes(c_buffer)[:count], parity

        def write(self, buffer: bytes) -> None:
            """Transmits the specified characters."""
            c_buffer = (ctypes.c_char * len(buffer)).from_buffer_copy(buffer)
            api.dwf_digital_uart_tx(self._device.handle, c_buffer, len(c_buffer))

        @staticmethod
        def _map_parity(value) -> int:
            named_values = {
                'n': 0,
                'no': 0,
                'o': 1,
                'odd': 1,
                'e': 2,
                'even': 2,
            }
            return Helpers.map_named_value(value, named_values)

    class Spi:
        """SPI protocol."""

        def __init__(self, device):
            self._device = device
            self._dq_mode = 1  # MOSI/MISO
            self._pin_clock = None
            self._pin_select = None
            self._pin_dq0 = None
            self._pin_dq1 = None
            self._pin_dq2 = None
            self._pin_dq3 = None
            self._frequency = None
            self._mode = None
            self._msb_first = None

        @property
        def pin_clock(self) -> int:
            """Gets or sets the DIO channel to use for SPI clock."""
            return self._pin_clock

        @pin_clock.setter
        def pin_clock(self, value: int) -> None:
            self._pin_clock = value
            api.dwf_digital_spi_clock_set(self._device.handle, value)

        @property
        def pin_select(self) -> int:
            """Gets or sets the DIO channel to use for SPI clock."""
            return self._pin_select

        @pin_select.setter
        def pin_select(self, value: int) -> None:
            self._pin_select = value

        @property
        def pin_dq0(self) -> int:
            """Gets or sets the DIO channel to use for SPI data."""
            return self._pin_dq0

        @pin_dq0.setter
        def pin_dq0(self, value: int) -> None:
            self._pin_dq0 = value
            api.dwf_digital_spi_data_set(self._device.handle, 0, value)

        @property
        def pin_dq1(self) -> int:
            """Gets or sets the DIO channel to use for SPI data."""
            return self._pin_dq1

        @pin_dq1.setter
        def pin_dq1(self, value: int) -> None:
            self._pin_dq1 = value
            api.dwf_digital_spi_data_set(self._device.handle, 1, value)

        @property
        def pin_dq2(self) -> int:
            """Gets or sets the DIO channel to use for SPI data."""
            return self._pin_dq2

        @pin_dq2.setter
        def pin_dq2(self, value: int) -> None:
            self._pin_dq2 = value
            api.dwf_digital_spi_data_set(self._device.handle, 2, value)

        @property
        def pin_dq3(self) -> int:
            """Gets or sets the DIO channel to use for SPI data."""
            return self._pin_dq3

        @pin_dq3.setter
        def pin_dq3(self, value: int) -> None:
            self._pin_dq3 = value
            api.dwf_digital_spi_data_set(self._device.handle, 3, value)

        @property
        def frequency(self) -> float:
            """Gets or sets the DIO channel to use for SPI data."""
            return self._frequency

        @frequency.setter
        def frequency(self, value: float) -> None:
            self._frequency = value
            api.dwf_digital_spi_frequency_set(self._device.handle, value)

        @property
        def mode(self) -> int:
            """Gets or sets the SPI mode."""
            return self._mode

        @mode.setter
        def mode(self, value: int) -> None:
            self._mode = value
            api.dwf_digital_spi_mode_set(self._device.handle, value)

        @property
        def msb_first(self) -> bool:
            """Gets or sets the bit order for SPI data."""
            return self._msb_first

        @msb_first.setter
        def msb_first(self, value: bool) -> None:
            self._msb_first = value
            api.dwf_digital_spi_order_set(self._device.handle, value)

        def reset(self) -> None:
            """Resets the SPI configuration to default value."""
            api.dwf_digital_spi_reset(self._device.handle)
            self._pin_clock = None
            self._pin_select = None
            self._pin_dq0 = None
            self._pin_dq1 = None
            self._pin_dq2 = None
            self._pin_dq3 = None
            self._frequency = 1000.0
            self._mode = None
            self._msb_first = None

        def setup(
                self,
                pin_clock,
                mosi_pin,
                miso_pin=None,
                pin_select=None,
                frequency=None,
                mode=0,
                msb_first=True) -> None:
            """Sets up the SPI pin configuration in standard mode."""
            self._dq_mode = 1  # MOSI/MISO
            self.pin_clock = pin_clock
            if mosi_pin is not None:
                self.pin_dq0 = mosi_pin
            if miso_pin is not None:
                self.pin_dq1 = miso_pin
            if pin_select is not None:
                self.pin_select = pin_select
            self._setup_config(frequency, mode, msb_first)

        def setup_three_wire(
                self,
                pin_clock,
                pin_siso,
                pin_select=None,
                frequency=None,
                mode=0,
                msb_first=True) -> None:
            """Sets up the SPI pin configuration in Three-wire mode."""
            self._dq_mode = 0  # SISO
            self.pin_clock = pin_clock
            self.pin_dq0 = pin_siso
            if pin_select is not None:
                self.pin_select = pin_select
            self._setup_config(frequency, mode, msb_first)

        def setup_dual(
                self,
                pin_clock,
                pin_dq0,
                pin_dq1,
                pin_select=None,
                frequency=None,
                mode=0,
                msb_first=True) -> None:
            """Sets up the SPI pin configuration in Dual mode."""
            self._dq_mode = 2  # DUAL
            self.pin_clock = pin_clock
            if pin_dq0 is not None:
                self.pin_dq0 = pin_dq0
            if pin_dq1 is not None:
                self.pin_dq1 = pin_dq1
            if pin_select is not None:
                self.pin_select = pin_select
            self._setup_config(frequency, mode, msb_first)

        def setup_quad(
                self,
                pin_clock,
                pin_dq0,
                pin_dq1,
                pin_dq2,
                pin_dq3,
                pin_select=None,
                frequency=None,
                mode=0,
                msb_first=True) -> None:
            """Sets up the SPI pin configuration in Quad mode."""
            self._dq_mode = 3  # QUAD
            self.pin_clock = pin_clock
            if pin_dq0 is not None:
                self.pin_dq0 = pin_dq0
            if pin_dq1 is not None:
                self.pin_dq1 = pin_dq1
            if pin_dq2 is not None:
                self.pin_dq2 = pin_dq2
            if pin_dq3 is not None:
                self.pin_dq3 = pin_dq3
            if pin_select is not None:
                self.pin_select = pin_select
            self._setup_config(frequency, mode, msb_first)

        def _setup_config(self, frequency, mode, msb_first) -> None:
            if frequency is not None:
                self.frequency = frequency
            if mode is not None:
                self.mode = mode
            if msb_first is not None:
                self.msb_first = msb_first

        def select(self, level, pin_select=None) -> None:
            """Control the SPI chip select."""
            if pin_select is None:
                pin_select = self.pin_select
            api.dwf_digital_spi_select(self._device.handle, pin_select, self._map_select_level(level))

        def read_one(self, dq_mode=None, bits_per_word=8) -> None:
            """Performs a SPI reception of up to 32 bits."""
            if dq_mode is None:
                dq_mode = self._dq_mode
            return api.dwf_digital_spi_read_one(self._device.handle, dq_mode, bits_per_word)

        def write_one(self, data: int, dq_mode=None, bits_per_word=8) -> None:
            """Performs a SPI transmit of up to 32 bits."""
            if dq_mode is None:
                dq_mode = self._dq_mode

            return api.dwf_digital_spi_write_one(self._device.handle, dq_mode, bits_per_word, data)

        def read(self, words_to_receive: int, dq_mode=None, bits_per_word=8):
            """Performs a SPI read."""
            if dq_mode is None:
                dq_mode = self._dq_mode

            c_rx_buffer: ctypes.Array
            if bits_per_word <= 8:
                c_rx_buffer = (ctypes.c_ubyte * words_to_receive)()
                api.dwf_digital_spi_read(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_rx_buffer, len(c_rx_buffer))
                return bytes(c_rx_buffer)
            if bits_per_word <= 16:
                c_rx_buffer = (ctypes.c_ushort * words_to_receive)()
                api.dwf_digital_spi_read16(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_rx_buffer, len(c_rx_buffer))
                return tuple(c_rx_buffer)
            if bits_per_word <= 32:
                c_rx_buffer = (ctypes.c_uint * words_to_receive)()
                api.dwf_digital_spi_read32(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_rx_buffer, len(c_rx_buffer))
                return tuple(c_rx_buffer)

            raise ValueError('bits_per_word cannot be higher than 32.')

        def write(self, buffer: bytes, dq_mode=None, bits_per_word=8) -> None:
            """Performs a SPI write."""
            if dq_mode is None:
                dq_mode = self._dq_mode

            if bits_per_word <= 8:
                c_tx_buffer = (ctypes.c_ubyte * len(buffer)).from_buffer_copy(buffer)
                api.dwf_digital_spi_write(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_tx_buffer, len(c_tx_buffer))
            if bits_per_word <= 16:
                c_tx_buffer = (ctypes.c_ubyte * len(buffer)).from_buffer_copy(buffer)
                api.dwf_digital_spi_write16(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_tx_buffer, len(c_tx_buffer))
            if bits_per_word <= 32:
                c_tx_buffer = (ctypes.c_ubyte * len(buffer)).from_buffer_copy(buffer)
                api.dwf_digital_spi_write32(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_tx_buffer, len(c_tx_buffer))

            raise ValueError('bits_per_word cannot be higher than 32.')

        def write_read(
                self,
                buffer,
                words_to_receive:
                int, dq_mode=None,
                bits_per_word=8):
            """Performs a SPI write/read."""
            if dq_mode is None:
                dq_mode = self._dq_mode

            c_tx_buffer: ctypes.Array
            c_rx_buffer: ctypes.Array
            if bits_per_word <= 8:
                c_tx_buffer = (ctypes.c_ubyte * len(buffer)).from_buffer_copy(buffer)
                c_rx_buffer = (ctypes.c_ubyte * words_to_receive)()
                api.dwf_digital_spi_write_read(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_tx_buffer, len(c_tx_buffer),
                    c_rx_buffer, len(c_rx_buffer))
                return bytes(c_rx_buffer)
            if bits_per_word <= 16:
                c_tx_buffer = (ctypes.c_ushort * len(buffer)).from_buffer_copy(buffer)
                c_rx_buffer = (ctypes.c_ushort * words_to_receive)()
                api.dwf_digital_spi_write_read16(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_tx_buffer, len(c_tx_buffer),
                    c_rx_buffer, len(c_rx_buffer))
                return tuple(c_rx_buffer)
            if bits_per_word <= 32:
                c_tx_buffer = (ctypes.c_uint * len(buffer)).from_buffer_copy(buffer)
                c_rx_buffer = (ctypes.c_uint * words_to_receive)()
                api.dwf_digital_spi_write_read32(
                    self._device.handle,
                    dq_mode, bits_per_word,
                    c_tx_buffer, len(c_tx_buffer),
                    c_rx_buffer, len(c_rx_buffer))
                return tuple(c_rx_buffer)
            raise ValueError('bits_per_word cannot be higher than 32.')

        @staticmethod
        def _map_select_level(value) -> int:
            named_values = {
                'l': 0,
                'low': 0,
                'h': 1,
                'high': 1,
                'z': -1,
                'release': -1,
            }
            return Helpers.map_named_value(value, named_values)

    class I2C:
        """I2C protocol."""

        def __init__(self, device):
            self._device = device
            self._pin_scl = None
            self._pin_sda = None
            self._rate = None
            self._read_nak = True

        @property
        def pin_scl(self) -> int:
            """Gets or sets the DIO channel to use for I2C clock."""
            return self._pin_scl

        @pin_scl.setter
        def pin_scl(self, value: int) -> None:
            self._pin_scl = value
            api.dwf_digital_i2c_scl_set(self._device.handle, value)

        @property
        def pin_sda(self) -> int:
            """Gets or sets the DIO channel to use for I2C data."""
            return self._pin_sda

        @pin_sda.setter
        def pin_sda(self, value: int) -> None:
            self._pin_sda = value
            api.dwf_digital_i2c_sda_set(self._device.handle, value)

        @property
        def rate(self) -> float:
            """Gets or sets the data rate."""
            return self._rate

        @rate.setter
        def rate(self, value: float) -> None:
            self._rate = value
            api.dwf_digital_i2c_rate_set(self._device.handle, value)

        @property
        def read_nak(self) -> bool:
            """Gets or sets a value indicating if the last read byte
            should be acknowledged or not."""
            return self._read_nak

        @read_nak.setter
        def read_nak(self, value: bool) -> None:
            self._read_nak = value
            api.dwf_digital_i2c_read_nak_set(self._device.handle, value)

        def reset(self) -> None:
            """Resets the I2C configuration to default value."""
            api.dwf_digital_i2c_reset(self._device.handle)
            self._pin_scl = None
            self._pin_sda = None
            self._rate = 100000.0
            self._read_nak = True

        def clear(self) -> bool:
            """ Verifies and tries to solve eventual bus lockup.
            Returns true, if the bus is free."""
            return bool(api.dwf_digital_i2c_clear(self._device.handle))

        def setup(self, pin_scl, pin_sda, rate=None, read_nak=None) -> None:
            """Sets up the I2C configuration."""
            if pin_scl is not None:
                self.pin_scl = pin_scl
            if pin_sda is not None:
                self.pin_sda = pin_sda
            if rate is not None:
                self.rate = rate
            if read_nak is not None:
                self.read_nak = read_nak

        def write_one(self, address: int, data: int) -> None:
            """Performs an I2C write of a single byte."""
            return api.dwf_digital_i2c_write_one(self._device.handle, address, data)

        def read(self, address: int, bytes_to_read: int) -> Tuple[bytes, int]:
            """Performs an I2C read.
            Returns (rx_buffer, nak_index)."""
            c_rx_buffer = (ctypes.c_ubyte * bytes_to_read)()
            nak_index = api.dwf_digital_i2c_read(
                self._device.handle,
                address,
                c_rx_buffer, len(c_rx_buffer))
            return bytes(c_rx_buffer), nak_index

        def write(self, address: int, buffer: bytes) -> None:
            """Performs an I2C write."""
            c_tx_buffer = (ctypes.c_ubyte * len(buffer)).from_buffer_copy(buffer)
            return api.dwf_digital_i2c_write(
                self._device.handle,
                address,
                c_tx_buffer, len(c_tx_buffer))

        def write_read(self, address: int, buffer: bytes, bytes_to_read: int) -> Tuple[bytes, int]:
            """Performs an I2C write/read.
            Returns (rx_buffer, nak_index)."""
            c_tx_buffer = (ctypes.c_ubyte * len(buffer)).from_buffer_copy(buffer)
            c_rx_buffer = (ctypes.c_ubyte * bytes_to_read)()
            nak_index = api.dwf_digital_i2c_write_read(
                self._device.handle,
                address,
                c_tx_buffer, len(c_tx_buffer),
                c_rx_buffer, len(c_rx_buffer))
            return bytes(c_rx_buffer), nak_index

    class CAN:
        """CAN protocol."""

        def __init__(self, device):
            self._device = device
            self._pin_tx = None
            self._pin_rx = None
            self._rate = None
            self._inverted = None

        @property
        def pin_rx(self) -> int:
            """Gets or sets the DIO channel to use for reception."""
            return self._pin_rx

        @pin_rx.setter
        def pin_rx(self, value: int) -> None:
            self._pin_rx = value
            api.dwf_digital_can_rx_set(self._device.handle, value)

        @property
        def pin_tx(self) -> int:
            """Gets or sets the DIO channel to use for transmission."""
            return self._pin_tx

        @pin_tx.setter
        def pin_tx(self, value: int) -> None:
            self._pin_tx = value
            api.dwf_digital_can_tx_set(self._device.handle, value)

        @property
        def rate(self) -> float:
            """Gets or sets the data rate."""
            return self._rate

        @rate.setter
        def rate(self, value: float) -> None:
            self._rate = value
            api.dwf_digital_can_rate_set(self._device.handle, value)

        @property
        def inverted(self) -> bool:
            """Gets or sets the polarity."""
            return self._inverted

        @inverted.setter
        def inverted(self, value: bool) -> None:
            self._inverted = value
            api.dwf_digital_can_polarity_set(self._device.handle, value)

        def reset(self) -> None:
            """Resets the CAN configuration to default value."""
            api.dwf_digital_can_reset(self._device.handle)
            self._pin_tx = None
            self._pin_rx = None
            self._rate = None
            self._inverted = None

        def setup(self, pin_rx=None, pin_tx=None, rate=None, inverted=False) -> None:
            """Sets up the CAN configuration."""
            if pin_rx is not None:
                self.pin_rx = pin_rx
            if pin_tx is not None:
                self.pin_tx = pin_tx
            if rate is not None:
                self.rate = rate
            if inverted is not None:
                self.inverted = inverted
            api.dwf_digital_can_rx(self._device.handle, 0, None)
            api.dwf_digital_can_tx(self._device.handle, -1, 0, 0, 0, None)

        def read(self) -> Tuple[bytes, int, int, int, int]:
            """Returns the received CAN frames since the last call."""
            c_buffer = (ctypes.c_char * 8)()
            frame_id, extended, remote, dlc, status = api.dwf_digital_can_rx(
                self._device.handle,
                c_buffer, len(c_buffer))
            return bytes(c_buffer)[:dlc], frame_id, extended, remote, status

        def write(self, frame_id: int, extended: int, remote: int, buffer: bytes) -> None:
            """Performs a CAN transmission."""
            c_buffer = (ctypes.c_char * len(buffer)).from_buffer_copy(buffer)
            api.dwf_digital_can_tx(
                self._device.handle,
                frame_id, extended, remote,
                len(c_buffer), c_buffer)

    def __init__(self, device):
        self._uart = self.Uart(device)
        self._spi = self.Spi(device)
        self._i2c = self.I2C(device)
        self._can = self.CAN(device)

    @property
    def uart(self) -> Uart:
        """Gets the UART protocol unit."""
        return self._uart

    @property
    def spi(self) -> Spi:
        """Gets the SPI protocol unit."""
        return self._spi

    @property
    def i2c(self) -> I2C:
        """Gets the I2C protocol unit."""
        return self._i2c

    @property
    def can(self) -> CAN:
        """Gets the CAN protocol unit."""
        return self._can
