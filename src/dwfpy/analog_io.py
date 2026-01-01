"""
Analog IO module for Digilent WaveForms devices.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
from typing import Tuple
from . import bindings as api
from . import device as fwd  # pylint: disable=unused-import
from .constants import ChannelNodeType
from .helpers import Helpers


class AnalogIoChannelNode:
    """Represents an Analog IO channel node."""

    def __init__(self, channel, index):
        self._device = channel.device
        self._channel = channel
        self._index = index

    def __str__(self):
        match self.type:
            case ChannelNodeType.VOLTAGE | ChannelNodeType.CURRENT | ChannelNodeType.POWER:
                return f"{self.status:.3f}{self.unit}"
            case ChannelNodeType.TEMPERATURE:
                return f"{self.status:.1f}{self.unit}"
            case _:
                return f"{self.status}{self.unit}"

    def __repr__(self):
        return (
            f"'{self._channel.name}.{self.name}' ({self.type.name}), "
            + f"Value [{self.value_min}..{self.value_max}/{self.value_steps}], "
            + f"Status [{self.status_min}..{self.status_max}/{self.status_steps}]"
        )

    @property
    def index(self) -> int:
        """Gets the node index."""
        return self._index

    @property
    def name(self) -> str:
        """Gets the node name."""
        name = ctypes.create_string_buffer(32)
        units = ctypes.create_string_buffer(16)
        api.dwf_analog_io_channel_node_name(self._device.handle, self._channel.index, self._index, name, units)
        return Helpers.c_char_to_string(name)

    @property
    def unit(self) -> str:
        """Gets the unit of the node value."""
        name = ctypes.create_string_buffer(32)
        units = ctypes.create_string_buffer(16)
        api.dwf_analog_io_channel_node_name(self._device.handle, self._channel.index, self._index, name, units)
        return Helpers.c_char_to_string(units)

    @property
    def type(self) -> ChannelNodeType:
        """Gets the node type."""
        return ChannelNodeType(
            api.dwf_analog_io_channel_node_info(self._device.handle, self._channel.index, self._index)
        )

    @property
    def value_min(self) -> float:
        """Gets the minimum settable value."""
        return api.dwf_analog_io_channel_node_set_info(self._device.handle, self._channel.index, self._index)[0]

    @property
    def value_max(self) -> float:
        """Gets the maximum settable value."""
        return api.dwf_analog_io_channel_node_set_info(self._device.handle, self._channel.index, self._index)[1]

    @property
    def value_steps(self) -> int:
        """Gets the number of steps between minimum and maximum settable values."""
        return api.dwf_analog_io_channel_node_set_info(self._device.handle, self._channel.index, self._index)[2]

    @property
    def value(self) -> float:
        """Gets or sets the node value."""
        return api.dwf_analog_io_channel_node_get(self._device.handle, self._channel.index, self._index)

    @value.setter
    def value(self, value: float) -> None:
        api.dwf_analog_io_channel_node_set(self._device.handle, self._channel.index, self._index, value)

    @property
    def status_min(self) -> float:
        """Gets the minimum reading value."""
        return api.dwf_analog_io_channel_node_status_info(self._device.handle, self._channel.index, self._index)[0]

    @property
    def status_max(self) -> float:
        """Gets the maximum reading value."""
        return api.dwf_analog_io_channel_node_status_info(self._device.handle, self._channel.index, self._index)[1]

    @property
    def status_steps(self) -> int:
        """Gets the number of steps between minimum and maximum reading values."""
        return api.dwf_analog_io_channel_node_status_info(self._device.handle, self._channel.index, self._index)[2]

    @property
    def status(self) -> float:
        """Gets the actual node value."""
        return api.dwf_analog_io_channel_node_status(self._device.handle, self._channel.index, self._index)


class AnalogIoChannel:
    """Represents an Analog IO channel."""

    def __init__(self, module, index):
        self._device = module.device
        self._module = module
        self._index = index
        self._nodes = tuple(
            AnalogIoChannelNode(self, i)
            for i in range(api.dwf_analog_io_channel_info(self._device.handle, self._index))
        )

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def module(self) -> "AnalogIo":
        """Gets the Analog IO module."""
        return self._module

    @property
    def index(self) -> int:
        """Gets the channel index."""
        return self._index

    @property
    def nodes(self) -> Tuple[AnalogIoChannelNode, ...]:
        """Gets the channel nodes."""
        return self._nodes

    def __getitem__(self, key) -> AnalogIoChannelNode:
        if isinstance(key, int):
            return self._nodes[key]

        if isinstance(key, str):
            for node in self._nodes:
                if node.name == key:
                    return node

        raise IndexError(key)

    @property
    def name(self) -> str:
        """Gets the channel name."""
        name = ctypes.create_string_buffer(32)
        label = ctypes.create_string_buffer(16)
        api.dwf_analog_io_channel_name(self._device.handle, self._index, name, label)
        return Helpers.c_char_to_string(name)

    @property
    def label(self) -> str:
        """Gets the channel label."""
        name = ctypes.create_string_buffer(32)
        label = ctypes.create_string_buffer(16)
        api.dwf_analog_io_channel_name(self._device.handle, self._index, name, label)
        return Helpers.c_char_to_string(label)


class AnalogIo:
    """Analog IO module."""

    def __init__(self, device):
        self._device = device
        self._channels = tuple(
            AnalogIoChannel(self, i) for i in range(api.dwf_analog_io_channel_count(self._device.handle))
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
    def channels(self) -> Tuple[AnalogIoChannel, ...]:
        """Gets a collection of Analog IO channels."""
        return self._channels

    def __getitem__(self, key) -> AnalogIoChannel:
        if isinstance(key, int):
            return self._channels[key]

        if isinstance(key, str):
            for channel in self._channels:
                if channel.label == key:
                    return channel

        raise IndexError(key)

    @property
    def master_enable_can_read(self) -> bool:
        """Return True when the status of the master enable can be read."""
        _, can_read = api.dwf_analog_io_enable_info(self._device.handle)
        return bool(can_read)

    @property
    def master_enable_can_set(self) -> bool:
        """Return True when the status of the master enable can be set."""
        can_set, _ = api.dwf_analog_io_enable_info(self._device.handle)
        return bool(can_set)

    @property
    def master_enable(self) -> bool:
        """Gets or sets the master enable switch."""
        return bool(api.dwf_analog_io_enable_get(self._device.handle))

    @master_enable.setter
    def master_enable(self, value: bool) -> None:
        api.dwf_analog_io_enable_set(self._device.handle, value)

    @property
    def master_enable_status(self) -> bool:
        """Gets the master enable status."""
        return bool(api.dwf_analog_io_enable_status(self._device.handle))

    def reset(self) -> None:
        """Resets and configures all instrument parameters to default values."""
        api.dwf_analog_io_reset(self._device.handle)

    def configure(self) -> None:
        """Configures the instrument."""
        api.dwf_analog_io_configure(self._device.handle)

    def read_status(self) -> None:
        """Reads the status of the device."""
        api.dwf_analog_io_status(self._device.handle)
