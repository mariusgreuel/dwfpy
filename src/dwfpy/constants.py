"""
Constants used by Digilent WaveForms API.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import enum


class DeviceId(enum.IntEnum):
    """Device identifier."""
    ELECTRONICS_EXPLORER = 1
    ANALOG_DISCOVERY = 2
    ANALOG_DISCOVERY2 = 3
    DIGITAL_DISCOVERY = 4


class DeviceFilter(enum.IntEnum):
    """Device filter."""
    ELECTRONICS_EXPLORER = 1
    ANALOG_DISCOVERY = 2
    ANALOG_DISCOVERY2 = 3
    DIGITAL_DISCOVERY = 4


class GlobalParameter(enum.IntEnum):
    """Global parameter."""
    USB_POWER = 2  # 1 keep the USB power enabled even when AUX is connected, Analog Discovery 2
    LED_BRIGHTNESS = 3  # LED brightness 0 ... 100%, Digital Discovery
    ON_CLOSE = 4  # 0 continue, 1 stop, 2 shutdown
    AUDIO_OUT = 5  # 0 disable / 1 enable audio output, Analog Discovery 1, 2
    USB_LIMIT = 6  # 0..1000 mA USB power limit, -1 no limit, Analog Discovery 1, 2


class Error(enum.IntEnum):
    """DWF API error codes."""
    NO_ERROR = 0
    UNKNOWN_ERROR = 1
    API_LOCK_TIMEOUT = 2
    ALREADY_OPENED = 3
    NOT_SUPPORTED = 4
    INVALID_PARAMETER0 = 0x10
    INVALID_PARAMETER1 = 0x11
    INVALID_PARAMETER2 = 0x12
    INVALID_PARAMETER3 = 0x13
    INVALID_PARAMETER4 = 0x14


class Status(enum.IntEnum):
    """Status of instrument state machine."""
    READY = 0
    ARMED = 1
    DONE = 2
    RUNNING = 3
    TRIGGERED = 3
    CONFIG = 4
    PREFILL = 5
    WAIT = 7


class TriggerSource(enum.IntEnum):
    """Trigger input source."""
    NONE = 0
    PC = 1
    DETECTOR_ANALOG_IN = 2
    DETECTOR_DIGITAL_IN = 3
    ANALOG_IN = 4
    DIGITAL_IN = 5
    DIGITAL_OUT = 6
    ANALOG_OUT1 = 7
    ANALOG_OUT2 = 8
    ANALOG_OUT3 = 9
    ANALOG_OUT4 = 10
    EXTERNAL1 = 11
    EXTERNAL2 = 12
    EXTERNAL3 = 13
    EXTERNAL4 = 14
    HIGH = 15
    LOW = 16


class TriggerType(enum.IntEnum):
    """Trigger type."""
    EDGE = 0
    PULSE = 1
    TRANSITION = 2


class TriggerSlope(enum.IntEnum):
    """Trigger slope."""
    RISE = 0
    FALL = 1
    EITHER = 2


class TriggerLengthCondition(enum.IntEnum):
    """Trigger length condition."""
    LESS = 0
    TIMEOUT = 1
    MORE = 2


class Function(enum.IntEnum):
    """Function type for analog output instruments."""
    DC = 0
    SINE = 1
    SQUARE = 2
    TRIANGLE = 3
    RAMP_UP = 4
    RAMP_DOWN = 5
    NOISE = 6
    PULSE = 7
    TRAPEZIUM = 8
    SINE_POWER = 9
    CUSTOM = 30
    PLAY = 31


class ChannelNodeType(enum.IntEnum):
    """Channel node type."""
    ENABLE = 1
    VOLTAGE = 2
    CURRENT = 3
    POWER = 4
    TEMPERATURE = 5


class AnalogOutputNode(enum.IntEnum):
    """Analog node type of analog output instruments."""
    CARRIER = 0
    FM = 1
    AM = 2


class AnalogOutputMode(enum.IntEnum):
    """Generator mode of analog output instruments."""
    VOLTAGE = 0
    CURRENT = 1


class AnalogOutputIdle(enum.IntEnum):
    """Idle output options of analog output instruments."""
    DISABLE = 0
    OFFSET = 1
    INITIAL = 2


class DigitalInputClockSource(enum.IntEnum):
    """Clock source for digital input instruments."""
    INTERNAL = 0
    EXTERNAL = 1


class DigitalInputSampleMode(enum.IntEnum):
    """Sample mode for digital input instruments."""
    SIMPLE = 0
    NOISE = 1


class DigitalOutputMode(enum.IntEnum):
    """Output pin mode of a digital output channel."""
    PUSH_PULL = 0
    OPEN_DRAIN = 1
    OPEN_SOURCE = 2
    THREE_STATE = 3


class DigitalOutputType(enum.IntEnum):
    """Output type of a digital output channel."""
    PULSE = 0
    CUSTOM = 1
    RANDOM = 2
    ROM = 3
    FSM = 3


class DigitalOutputIdle(enum.IntEnum):
    """Idle state of a digital output channel."""
    INIT = 0
    LOW = 1
    HIGH = 2
    ZET = 3


class AnalogImpedance(enum.IntEnum):
    """Analog impedance measurement index."""
    IMPEDANCE = 0  # Ohms
    IMPEDANCE_PHASE = 1  # Radians
    RESISTANCE = 2  # Ohms
    REACTANCE = 3  # Ohms
    ADMITTANCE = 4  # Siemen
    ADMITTANCE_PHASE = 5  # Radians
    CONDUCTANCE = 6  # Siemen
    SUSCEPTANCE = 7  # Siemen
    SERIES_CAPACITANCE = 8  # Farad
    PARALLEL_CAPACITANCE = 9  # Farad
    SERIES_INDUCTANCE = 10  # Henry
    PARALLEL_INDUCTANCE = 11  # Henry
    DISSIPATION = 12  # factor
    QUALITY = 13  # factor


class AcquisitionMode(enum.IntEnum):
    """Acquisition mode for analog and digital instruments."""
    SINGLE = 0
    SCAN_SHIFT = 1
    SCAN_SCREEN = 2
    RECORD = 3
    OVERS = 4
    SINGLE1 = 5


class FilterMode(enum.IntEnum):
    """Acquisition filter for analog input channels."""
    DECIMATE = 0
    AVERAGE = 1
    MIN_MAX = 2
