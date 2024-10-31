"""
Internal helper functions.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

from .constants import (
    AcquisitionMode,
    AnalogInputCoupling,
    DigitalOutputMode,
    DigitalOutputType,
    DigitalOutputIdle,
    FilterMode,
    Function,
    TriggerLengthCondition,
    TriggerSlope,
    TriggerSource,
)


class Helpers:
    """Internal helper class."""

    # pylint:disable=missing-function-docstring

    @staticmethod
    def c_char_to_string(buffer) -> str:
        return buffer.value.decode("ascii")

    @staticmethod
    def make_default(value, default_value=None):
        return default_value if value is None else value

    @staticmethod
    def map_enum_values(enum_type, values) -> tuple:
        return tuple(v for v in enum_type if (values & (1 << v.value)) != 0)

    @staticmethod
    def map_named_value(value, named_values, default_value=None):
        if value is None:
            return default_value

        if isinstance(value, str):
            return named_values[value.lower()]

        return value

    @staticmethod
    def pack_bits(data):
        if isinstance(data, (bytes, bytearray)):
            return data, len(data) * 8

        bit_count = len(data)
        byte_buffer = bytearray((bit_count + 7) // 8)

        for i, bit in enumerate(data):
            if bit != 0:
                byte_buffer[i // 8] |= 1 << (i % 8)

        return byte_buffer, bit_count

    @staticmethod
    def map_state(value, default_value=None):
        named_values = {
            "low": False,
            "high": True,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_acquisition_mode(value, default_value=None):
        named_values = {
            "single": AcquisitionMode.SINGLE,
            "scan-shift": AcquisitionMode.SCAN_SHIFT,
            "scan-screen": AcquisitionMode.SCAN_SCREEN,
            "record": AcquisitionMode.RECORD,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_function(value, default_value=None):
        named_values = {
            "dc": Function.DC,
            "sine": Function.SINE,
            "square": Function.SQUARE,
            "triangle": Function.TRIANGLE,
            "ramp-up": Function.RAMP_UP,
            "ramp-down": Function.RAMP_DOWN,
            "noise": Function.NOISE,
            "pulse": Function.PULSE,
            "trapezium": Function.TRAPEZIUM,
            "sine_power": Function.SINE_POWER,
            "custom-pattern": Function.CUSTOM_PATTERN,
            "play-pattern": Function.PLAY_PATTERN,
            "custom": Function.CUSTOM,
            "play": Function.PLAY,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_coupling(value, default_value=None):
        named_values = {
            "dc": AnalogInputCoupling.DC,
            "ac": AnalogInputCoupling.AC,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_digital_output_mode(value, default_value=None):
        named_values = {
            "pp": DigitalOutputMode.PUSH_PULL,
            "push-pull": DigitalOutputMode.PUSH_PULL,
            "od": DigitalOutputMode.OPEN_DRAIN,
            "open-drain": DigitalOutputMode.OPEN_DRAIN,
            "os": DigitalOutputMode.OPEN_SOURCE,
            "open-source": DigitalOutputMode.OPEN_SOURCE,
            "three-state": DigitalOutputMode.THREE_STATE,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_digital_output_type(value, default_value=None):
        named_values = {
            "pulse": DigitalOutputType.PULSE,
            "custom": DigitalOutputType.CUSTOM,
            "random": DigitalOutputType.RANDOM,
            "rom": DigitalOutputType.ROM,
            "state": DigitalOutputType.STATE,
            "play": DigitalOutputType.PLAY,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_digital_output_idle(value, default_value=None):
        named_values = {
            "init": DigitalOutputIdle.INIT,
            "initial": DigitalOutputIdle.INIT,
            "low": DigitalOutputIdle.LOW,
            "high": DigitalOutputIdle.HIGH,
            "z": DigitalOutputIdle.ZET,
            "zet": DigitalOutputIdle.ZET,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_filter(value, default_value=None):
        named_values = {
            "decimate": FilterMode.DECIMATE,
            "average": FilterMode.AVERAGE,
            "min-max": FilterMode.MIN_MAX,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_trigger_length_condition(value, default_value=None):
        named_values = {
            "less": TriggerLengthCondition.LESS,
            "timeout": TriggerLengthCondition.TIMEOUT,
            "more": TriggerLengthCondition.MORE,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_trigger_slope(value, default_value=None):
        named_values = {
            "rise": TriggerSlope.RISE,
            "rising": TriggerSlope.RISE,
            "pos": TriggerSlope.RISE,
            "positive": TriggerSlope.RISE,
            "entering": TriggerSlope.RISE,
            "fall": TriggerSlope.FALL,
            "falling": TriggerSlope.FALL,
            "neg": TriggerSlope.FALL,
            "negative": TriggerSlope.FALL,
            "exiting": TriggerSlope.FALL,
            "either": TriggerSlope.EITHER,
        }
        return Helpers.map_named_value(value, named_values, default_value)

    @staticmethod
    def map_trigger_source(value, default_value=None):
        named_values = {
            "none": TriggerSource.NONE,
            "pc": TriggerSource.PC,
            "detector-analog-in": TriggerSource.DETECTOR_ANALOG_IN,
            "detector-digital-in": TriggerSource.DETECTOR_DIGITAL_IN,
            "analog-in": TriggerSource.ANALOG_IN,
            "digital-in": TriggerSource.DIGITAL_IN,
            "digital-out": TriggerSource.DIGITAL_OUT,
            "analog-out1": TriggerSource.ANALOG_OUT1,
            "analog-out2": TriggerSource.ANALOG_OUT2,
            "analog-out3": TriggerSource.ANALOG_OUT3,
            "analog-out4": TriggerSource.ANALOG_OUT4,
            "external1": TriggerSource.EXTERNAL1,
            "external2": TriggerSource.EXTERNAL2,
            "external3": TriggerSource.EXTERNAL3,
            "external4": TriggerSource.EXTERNAL4,
            "high": TriggerSource.HIGH,
            "low": TriggerSource.LOW,
            "clock": TriggerSource.CLOCK,
        }
        return Helpers.map_named_value(value, named_values, default_value)
