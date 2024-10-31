"""
Configuration set for Digilent WaveForms devices.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
from . import bindings as api
from .helpers import Helpers


class Configuration:
    """Configuration set for Digilent WaveForms devices."""

    def __init__(self, index):
        self._analog_in_channel_count = api.dwf_enum_config_info(index, api.DECI_ANALOG_IN_CHANNEL_COUNT)
        self._analog_out_channel_count = api.dwf_enum_config_info(index, api.DECI_ANALOG_OUT_CHANNEL_COUNT)
        self._analog_io_channel_count = api.dwf_enum_config_info(index, api.DECI_ANALOG_IO_CHANNEL_COUNT)
        self._digital_in_channel_count = api.dwf_enum_config_info(index, api.DECI_DIGITAL_IN_CHANNEL_COUNT)
        self._digital_out_channel_count = api.dwf_enum_config_info(index, api.DECI_DIGITAL_OUT_CHANNEL_COUNT)
        self._digital_io_channel_count = api.dwf_enum_config_info(index, api.DECI_DIGITAL_IO_CHANNEL_COUNT)
        self._analog_in_buffer_size = api.dwf_enum_config_info(index, api.DECI_ANALOG_IN_BUFFER_SIZE)
        self._analog_out_buffer_size = api.dwf_enum_config_info(index, api.DECI_ANALOG_OUT_BUFFER_SIZE)
        self._digital_in_buffer_size = api.dwf_enum_config_info(index, api.DECI_DIGITAL_IN_BUFFER_SIZE)
        self._digital_out_buffer_size = api.dwf_enum_config_info(index, api.DECI_DIGITAL_OUT_BUFFER_SIZE)

        text_info = Configuration._enum_config_info_str(index, api.DECI_TEXT_INFO)
        self._text_info = text_info if len(text_info) > 1 else ""

    @property
    def analog_in_channel_count(self) -> int:
        """Gets the total number of Analog Input channels."""
        return self._analog_in_channel_count

    @property
    def analog_out_channel_count(self) -> int:
        """Gets the total number of Analog Output channels."""
        return self._analog_out_channel_count

    @property
    def analog_io_channel_count(self) -> int:
        """Gets the total number of Analog IO channels."""
        return self._analog_io_channel_count

    @property
    def digital_in_channel_count(self) -> int:
        """Gets the total number of Digital Input channels."""
        return self._digital_in_channel_count

    @property
    def digital_out_channel_count(self) -> int:
        """Gets the total number of Digital Output channels."""
        return self._digital_out_channel_count

    @property
    def digital_io_channel_count(self) -> int:
        """Gets the total number of Digital IO channels."""
        return self._digital_io_channel_count

    @property
    def analog_in_buffer_size(self) -> int:
        """Gets the Analog Input buffer size."""
        return self._analog_in_buffer_size

    @property
    def analog_out_buffer_size(self) -> int:
        """Gets the Analog Output buffer size."""
        return self._analog_out_buffer_size

    @property
    def digital_in_buffer_size(self) -> int:
        """Gets the Digital Input buffer size."""
        return self._digital_in_buffer_size

    @property
    def digital_out_buffer_size(self) -> int:
        """Gets the Digital Output buffer size."""
        return self._digital_out_buffer_size

    @property
    def text_info(self) -> str:
        """Gets an extra configuration information string."""
        return self._text_info

    @staticmethod
    def _enum_config_info_str(device, info) -> str:
        buffer = ctypes.create_string_buffer(128)
        api.dwf_enum_config_info_str(device, info, buffer)
        return Helpers.c_char_to_string(buffer)
