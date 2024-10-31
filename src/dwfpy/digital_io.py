"""
Digital IO module for Digilent WaveForms devices.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

from typing import Optional, Tuple
from . import bindings as api
from . import device as fwd  # pylint: disable=unused-import


class DigitalIoChannel:
    """Represents an Digital IO channel."""

    def __init__(self, module, channel):
        self._device = module.device
        self._module = module
        self._channel = channel
        self._label = "ch" + str(channel + 1)

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def module(self) -> "DigitalIo":
        """Gets the Digital IO module."""
        return self._module

    @property
    def index(self) -> int:
        """Gets the channel index."""
        return self._channel

    @property
    def label(self) -> str:
        """Gets or sets the channel label."""
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @property
    def enabled(self) -> bool:
        """Enables or disables the pin as an output."""
        state = api.dwf_digital_io_output_enable_get64(self._device.handle)
        return bool(state & self._mask)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        state = api.dwf_digital_io_output_enable_get64(self._device.handle)
        state = (state | self._mask) if value else (state & ~self._mask)
        api.dwf_digital_io_output_enable_set64(self._device.handle, state)

    @property
    def can_read(self) -> bool:
        """Returns True of the pin can be read."""
        state = api.dwf_digital_io_input_info64(self._device.handle)
        return bool(state & self._mask)

    @property
    def can_write(self) -> bool:
        """Returns True of the pin can be written."""
        state = api.dwf_digital_io_output_info64(self._device.handle)
        return bool(state & self._mask)

    @property
    def output_state(self) -> bool:
        """Gets or sets the ouput state of the pin."""
        state = api.dwf_digital_io_output_get64(self._device.handle)
        return bool(state & self._mask)

    @output_state.setter
    def output_state(self, value: bool) -> None:
        state = api.dwf_digital_io_output_get64(self._device.handle)
        state = (state | self._mask) if value else (state & ~self._mask)
        api.dwf_digital_io_output_set64(self._device.handle, state)

    @property
    def input_state(self) -> bool:
        """Gets the input state of the pin.
        Before calling this function, call the 'read_status()' function
        to read the Digital I/O states from the device.
        """
        state = api.dwf_digital_io_input_status64(self._device.handle)
        return bool(state & self._mask)

    def setup(
        self,
        enabled: Optional[bool] = None,
        state: Optional[bool] = None,
        configure: Optional[bool] = None,
    ) -> None:
        """Sets up the channel.

        Parameters
        ----------
        enabled : bool, optional
            If True, then the channel is configured as an output.
        state : bool, optional
            The output state.
        configure : bool, optional
            If True, then the instrument is configured.
        """
        if enabled is not None:
            self.enabled = enabled
        if state is not None:
            self.output_state = state
        if configure:
            self._module.configure()

    @property
    def _mask(self) -> int:
        return 1 << self._channel


class DigitalIo:
    """Digital IO module."""

    def __init__(self, device):
        self._device = device
        self._channels = tuple(
            DigitalIoChannel(self, i) for i in range(api.dwf_digital_in_bits_info(self._device.handle))
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        del exception_type, exception_value, traceback
        self.reset()

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def channels(self) -> Tuple[DigitalIoChannel, ...]:
        """Gets a collection of Digital IO channels."""
        return self._channels

    def __getitem__(self, key) -> DigitalIoChannel:
        if isinstance(key, int):
            return self._channels[key]

        if isinstance(key, str):
            for channel in self._channels:
                if channel.label == key:
                    return channel

        raise IndexError(key)

    def reset(self) -> None:
        """Resets and configures all instrument parameters to default values."""
        api.dwf_digital_io_reset(self._device.handle)

    def configure(self) -> None:
        """Configures the instrument."""
        api.dwf_digital_io_configure(self._device.handle)

    def read_status(self) -> None:
        """Reads the status and input values of the device."""
        api.dwf_digital_io_status(self._device.handle)

    @property
    def output_enable_mask(self) -> int:
        """Gets the pins that can be enabled as an output as a bit-mask."""
        return api.dwf_digital_io_output_enable_info64(self._device.handle)

    @property
    def output_enable(self) -> int:
        """Enables or disables the specified pins as an output via a bit-mask."""
        return api.dwf_digital_io_output_enable_get64(self._device.handle)

    @output_enable.setter
    def output_enable(self, value: int) -> None:
        api.dwf_digital_io_output_enable_set64(self._device.handle, value)

    @property
    def output_state_mask(self) -> int:
        """Gets the pins that can be written to as a bit-mask."""
        return api.dwf_digital_io_output_info64(self._device.handle)

    @property
    def output_state(self) -> int:
        """Gets or sets the ouput state of all pins via a bit-mask."""
        return api.dwf_digital_io_output_get64(self._device.handle)

    @output_state.setter
    def output_state(self, value: int) -> None:
        api.dwf_digital_io_output_set64(self._device.handle, value)

    @property
    def input_state_mask(self) -> int:
        """Gets the pins that can be read from as a bit-mask."""
        return api.dwf_digital_io_input_info64(self._device.handle)

    @property
    def input_state(self) -> int:
        """Gets the input state of all pins as a bit-mask.
        Before calling this function, call the 'read_status()' function
        to read the Digital I/O states from the device.
        """
        return api.dwf_digital_io_input_status64(self._device.handle)
