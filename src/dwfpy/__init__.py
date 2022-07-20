"""
`dwfpy` is a package for accessing Digilent WaveForms devices.

Example
-------

import dwfpy as dwf

with dwf.Device() as device:
    print(f'Found device: {device.name} ({device.serial_number})')

    # Generate sine wave
    device.analog_output[0].setup(function='sine', frequency=1000, amplitude=1.41, offset=1.41, configure=True)

Available subpackages
---------------------
bindings
    Provides access to the raw C bindings of the DWF API.
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
from dwfpy.exceptions import WaveformsError, DeviceNotFound, DeviceNotOpenError
from dwfpy.device import (
    Device,
    ElectronicsExplorer,
    AnalogDiscovery,
    AnalogDiscovery2,
    DigitalDiscovery,
)
from dwfpy.application import Application
from dwfpy.analog_recorder import AnalogRecorder
from dwfpy.digital_recorder import DigitalRecorder

__version__ = '1.0'
