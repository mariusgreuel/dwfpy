"""
`dwfpy` is a package for accessing Digilent WaveForms devices.
"""

#
# This software is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

from dwfpy.constants import (
    DeviceId,
    DeviceType,
    GlobalParameter,
    Error,
    Status,
    TriggerSource,
    TriggerType,
    TriggerSlope,
    TriggerLengthCondition,
    Function,
    ChannelNodeType,
    DmmMode,
    AnalogInputCoupling,
    AnalogOutputNode,
    AnalogOutputMode,
    AnalogOutputIdle,
    DigitalInputClockSource,
    DigitalInputSampleMode,
    DigitalOutputMode,
    DigitalOutputType,
    DigitalOutputIdle,
    AnalogImpedance,
    Window,
    AcquisitionMode,
    FilterMode,
)
from dwfpy.exceptions import WaveformsError, DeviceNotFound, DeviceNotOpenError, FeatureNotSupportedError
from dwfpy.device import (
    Device,
    ElectronicsExplorer,
    AnalogDiscovery,
    AnalogDiscovery2,
    AnalogDiscovery3,
    DigitalDiscovery,
)
from dwfpy.application import Application
from dwfpy.analog_recorder import AnalogRecorder
from dwfpy.digital_recorder import DigitalRecorder

__version__ = "1.0"
