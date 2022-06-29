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
    AcquisitionMode, AnalogInputCoupling,
    DigitalOutputMode, DigitalOutputType, DigitalOutputIdle,
    FilterMode, Function,
    TriggerLengthCondition, TriggerSlope)


class Helpers:
    """Internal helper class."""

    # pylint:disable=missing-function-docstring

    @staticmethod
    def c_char_to_string(buffer) -> str:
        return buffer.value.decode('ascii')

    @staticmethod
    def map_enum_values(enum_type, values) -> tuple:
        return tuple(v for v in enum_type if (values & (1 << v.value)) != 0)

    @staticmethod
    def map_named_value(value, named_values):
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
    def normalize_ring_buffer(buffer, buffer_index):
        if buffer_index == 0:
            return tuple(buffer)

        return tuple(buffer[buffer_index:] + buffer[:buffer_index])

    @staticmethod
    def map_state(value):
        named_values = {
            'low': False,
            'high': True,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_trigger_slope(value):
        named_values = {
            'rise': TriggerSlope.RISE,
            'rising': TriggerSlope.RISE,
            'pos': TriggerSlope.RISE,
            'positive': TriggerSlope.RISE,
            'entering': TriggerSlope.RISE,
            'fall': TriggerSlope.FALL,
            'falling': TriggerSlope.FALL,
            'neg': TriggerSlope.FALL,
            'negative': TriggerSlope.FALL,
            'exiting': TriggerSlope.FALL,
            'either': TriggerSlope.EITHER,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_trigger_length_condition(value):
        named_values = {
            'less': TriggerLengthCondition.LESS,
            'timeout': TriggerLengthCondition.TIMEOUT,
            'more': TriggerLengthCondition.MORE,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_acquisition_mode(value):
        named_values = {
            'single': AcquisitionMode.SINGLE,
            'scan-shift': AcquisitionMode.SCAN_SHIFT,
            'scan-screen': AcquisitionMode.SCAN_SCREEN,
            'record': AcquisitionMode.RECORD,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_function(value):
        named_values = {
            'dc': Function.DC,
            'sine': Function.SINE,
            'square': Function.SQUARE,
            'triangle': Function.TRIANGLE,
            'ramp-up': Function.RAMP_UP,
            'ramp-down': Function.RAMP_DOWN,
            'noise': Function.NOISE,
            'pulse': Function.PULSE,
            'trapezium': Function.TRAPEZIUM,
            'sine_power': Function.SINE_POWER,
            'custom-pattern': Function.CUSTOM_PATTERN,
            'play-pattern': Function.PLAY_PATTERN,
            'custom': Function.CUSTOM,
            'play': Function.PLAY,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_coupling(value):
        named_values = {
            'dc': AnalogInputCoupling.DC,
            'ac': AnalogInputCoupling.AC,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_digital_output_mode(value):
        named_values = {
            'pp': DigitalOutputMode.PUSH_PULL,
            'push-pull': DigitalOutputMode.PUSH_PULL,
            'od': DigitalOutputMode.OPEN_DRAIN,
            'open-drain': DigitalOutputMode.OPEN_DRAIN,
            'os': DigitalOutputMode.OPEN_SOURCE,
            'open-source': DigitalOutputMode.OPEN_SOURCE,
            'three-state': DigitalOutputMode.THREE_STATE,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_digital_output_type(value):
        named_values = {
            'pulse': DigitalOutputType.PULSE,
            'custom': DigitalOutputType.CUSTOM,
            'random': DigitalOutputType.RANDOM,
            'rom': DigitalOutputType.ROM,
            'state': DigitalOutputType.STATE,
            'play': DigitalOutputType.PLAY,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_digital_output_idle(value):
        named_values = {
            'init': DigitalOutputIdle.INIT,
            'initial': DigitalOutputIdle.INIT,
            'low': DigitalOutputIdle.LOW,
            'high': DigitalOutputIdle.HIGH,
            'z': DigitalOutputIdle.ZET,
            'zet': DigitalOutputIdle.ZET,
        }
        return Helpers.map_named_value(value, named_values)

    @staticmethod
    def map_filter(value):
        named_values = {
            'decimate': FilterMode.DECIMATE,
            'average': FilterMode.AVERAGE,
            'min-max': FilterMode.MIN_MAX,
        }
        return Helpers.map_named_value(value, named_values)
