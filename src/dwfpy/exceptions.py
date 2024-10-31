"""
Exceptions for Digilent WaveForms.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#


class WaveformsError(RuntimeError):
    """Base class for Digilent WaveForms exceptions."""

    def __init__(self, message: str, error: int = 0):
        super().__init__(message)
        self.error = error


class DeviceNotFound(WaveformsError):
    """Device not found error."""

    def __init__(self, message):
        super().__init__(message)


class DeviceNotOpenError(WaveformsError):
    """Device is not open error."""

    def __init__(self, message):
        super().__init__(message)


class FeatureNotSupportedError(WaveformsError):
    """Feature is not supported error."""

    def __init__(self, message):
        super().__init__(message)
