"""
Device information for Digilent WaveForms devices.
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
from .configuration import Configuration
from .helpers import Helpers


class DeviceInfo:
    """Device information gathered during device enumeration."""

    def __init__(self, device_index=None):
        self._has_properties = False
        self._is_open = False
        self._id = None
        self._revision = None
        self._name = None
        self._user_name = None
        self._serial_number = None
        self._configurations = None

        if device_index is not None:
            self.get_properties(device_index)

    @property
    def has_properties(self) -> bool:
        """Returns True, if the device properties have been read."""
        return self._has_properties

    @property
    def is_open(self) -> bool:
        """Returns true if the device has been opened."""
        return self._is_open

    @property
    # pylint: disable-next=invalid-name
    def id(self) -> int:
        """Gets the device ID."""
        return self._id

    @property
    def revision(self) -> int:
        """Gets the device revision."""
        return self._revision

    @property
    def name(self) -> str:
        """Gets the device name."""
        return self._name

    @property
    def user_name(self) -> str:
        """Gets the user-defined device name."""
        return self._user_name

    @property
    def serial_number(self) -> str:
        """Gets the 12-digit, unique device serial number."""
        return self._serial_number

    @property
    def configurations(self) -> Tuple[Configuration, ...]:
        """Returns a list of device configurations."""
        return self._configurations

    def get_properties(self, device_index: int) -> None:
        """Read all device properties."""
        self._is_open = api.dwf_enum_device_is_opened(device_index)
        self._id, self._revision = api.dwf_enum_device_type(device_index)
        self._name = self.get_device_name(device_index)
        self._user_name = self.get_user_name(device_index)
        self._serial_number = self.get_serial_number(device_index)
        self._configurations = tuple(Configuration(i) for i in range(api.dwf_enum_config(device_index)))
        self._has_properties = True

    @staticmethod
    def get_device_name(device_index: int) -> str:
        """Gets the device name."""
        device_name = ctypes.create_string_buffer(32)
        api.dwf_enum_device_name(device_index, device_name)
        return Helpers.c_char_to_string(device_name)

    @staticmethod
    def get_user_name(device_index: int) -> str:
        """Gets the user-defined device name."""
        user_name = ctypes.create_string_buffer(32)
        api.dwf_enum_user_name(device_index, user_name)
        return Helpers.c_char_to_string(user_name)

    @staticmethod
    def get_serial_number(device_index: int) -> str:
        """Gets the device serial number."""
        serial_number = ctypes.create_string_buffer(32)
        api.dwf_enum_sn(device_index, serial_number)
        return DeviceInfo.normalize_serial_number(Helpers.c_char_to_string(serial_number))

    @staticmethod
    def normalize_serial_number(serial_number: str) -> str:
        """Normalizes the serial number, i.e. strip the leading 'SN:' and convert to uppercase."""
        return serial_number.upper().lstrip("SN:")
