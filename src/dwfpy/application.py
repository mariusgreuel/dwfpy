"""
Support for Digilent WaveForms applications.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
import logging
from . import bindings as api
from .constants import Error, GlobalParameter
from .exceptions import WaveformsError
from .helpers import Helpers


class _Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance


class Application(_Singleton):
    """WaveForms application."""

    _logger = logging.getLogger("dwfpy")

    def __init__(self):
        api.set_error_handler(Application._error_handler)

    @staticmethod
    def _error_handler(result, _, args):
        if not result:
            error = Application.get_last_error()
            if error != Error.NO_ERROR:
                error_message = Application.get_last_error_message()
                raise WaveformsError(error_message, error)

        return args

    @staticmethod
    def get_logger() -> logging.Logger:
        """Gets the WaveForms logger."""
        return Application._logger

    @staticmethod
    def get_version() -> str:
        """Gets the DWF API version string."""
        buffer = ctypes.create_string_buffer(32)
        api.dwf_get_version(buffer)
        return Helpers.c_char_to_string(buffer)

    @staticmethod
    def get_last_error() -> Error:
        """Gets the last DWF API error code."""
        return Error(api.dwf_get_last_error())

    @staticmethod
    def get_last_error_message() -> str:
        """Gets the last DWF API error message."""
        buffer = ctypes.create_string_buffer(512)
        api.dwf_get_last_error_msg(buffer)
        return Helpers.c_char_to_string(buffer).rstrip("\n")

    @staticmethod
    def get_parameter(parameter: GlobalParameter) -> int:
        """Gets a global parameter."""
        return api.dwf_param_get(parameter)

    @staticmethod
    def set_parameter(parameter: GlobalParameter, value: int) -> None:
        """Sets a global parameter."""
        api.dwf_param_set(parameter, value)

    @property
    def usb_power_on_aux(self) -> bool:
        """Gets or sets a value to keep the USB power enabled even when AUX supply is connected.
        Applies to Analog Discovery 2"""
        return bool(self.get_parameter(GlobalParameter.USB_POWER))

    @usb_power_on_aux.setter
    def usb_power_on_aux(self, value: bool) -> None:
        self.set_parameter(GlobalParameter.USB_POWER, value)

    @property
    def led_brightness(self) -> int:
        """Gets or sets the Digital Discovery LED brightness."""
        return self.get_parameter(GlobalParameter.LED_BRIGHTNESS)

    @led_brightness.setter
    def led_brightness(self, value: int) -> None:
        self.set_parameter(GlobalParameter.LED_BRIGHTNESS, value)

    @property
    def on_close_behavior(self) -> int:
        """Gets or sets a value indicating the device close behavior.
        0 = Continue, 1 = Stop, 2 = Shutdown."""
        return self.get_parameter(GlobalParameter.ON_CLOSE)

    @on_close_behavior.setter
    def on_close_behavior(self, value: int) -> None:
        self.set_parameter(GlobalParameter.ON_CLOSE, value)

    @property
    def enable_audio_output(self) -> bool:
        """Enables or disables audio output."""
        return bool(self.get_parameter(GlobalParameter.AUDIO_OUT))

    @enable_audio_output.setter
    def enable_audio_output(self, value: bool) -> None:
        self.set_parameter(GlobalParameter.AUDIO_OUT, value)

    @property
    def usb_limit(self) -> int:
        """Gets or sets the USB current limitation in mA."""
        return self.get_parameter(GlobalParameter.USB_LIMIT)

    @usb_limit.setter
    def usb_limit(self, value: int) -> None:
        self.set_parameter(GlobalParameter.USB_LIMIT, value)

    @property
    def enable_analog_out(self) -> bool:
        """Enables or disables the analog audio output."""
        return bool(self.get_parameter(GlobalParameter.ANALOG_OUT))

    @enable_analog_out.setter
    def enable_analog_out(self, value: bool) -> None:
        self.set_parameter(GlobalParameter.ANALOG_OUT, value)

    @property
    def frequency(self) -> int:
        """Gets or sets the frequency in Hz."""
        return self.get_parameter(GlobalParameter.FREQUENCY)

    @frequency.setter
    def frequency(self, value: int) -> None:
        self.set_parameter(GlobalParameter.FREQUENCY, value)

    @property
    def external_frequency(self) -> int:
        """Specifies the external frequency in Hz."""
        return self.get_parameter(GlobalParameter.EXT_FREQ)

    @external_frequency.setter
    def external_frequency(self, value: int) -> None:
        self.set_parameter(GlobalParameter.EXT_FREQ, value)

    @property
    def clock_mode(self) -> int:
        """Specifies the clock mode: 0 internal, 1 output, 2 input, 3 IO."""
        return self.get_parameter(GlobalParameter.CLOCK_MODE)

    @clock_mode.setter
    def clock_mode(self, value: int) -> None:
        self.set_parameter(GlobalParameter.CLOCK_MODE, value)
