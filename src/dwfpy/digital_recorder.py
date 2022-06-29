"""
Recorder for Digital Input data.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
from typing import Optional
from . import bindings as api
from . import digital_input as fwd  # pylint: disable=unused-import
from .constants import DigitalInputSampleMode, Status
from .helpers import Helpers


class DigitalRecorder:
    """Recorder for Digital Input data"""
    def __init__(self, module: 'fwd.DigitalInput', callback=None):
        self._module = module
        self._callback = callback

        self._status = Status.READY
        self._requested_samples = 0
        self._total_samples = 0
        self._lost_samples = 0
        self._corrupted_samples = 0
        self._data_samples: tuple = ()
        self._noise_samples: tuple = ()

        self._sample_size = 0
        self._buffer_size = 0
        self._buffer_index = 0
        self._data_buffer: Optional[ctypes.Array] = None
        self._noise_buffer: Optional[ctypes.Array] = None

    @property
    def status(self) -> Status:
        """Gets the last acquisition status."""
        return self._status

    @property
    def requested_samples(self) -> int:
        """Gets the number of requested samples for recording."""
        return self._requested_samples

    @property
    def total_samples(self) -> int:
        """Gets the total number of acquired and lost samples."""
        return self._total_samples

    @property
    def lost_samples(self) -> int:
        """Gets the number of lost samples."""
        return self._lost_samples

    @property
    def corrupted_samples(self) -> int:
        """Gets the number of corrupted samples."""
        return self._corrupted_samples

    @property
    def data_samples(self) -> tuple:
        """Gets the acquired data samples."""
        return self._data_samples

    @property
    def noise_samples(self) -> tuple:
        """Gets the acquired noise samples."""
        return self._noise_samples

    def record(self, sample_count: int) -> None:
        """Starts the recording."""
        self._requested_samples = sample_count
        self._buffer_size = sample_count

        if sample_count > 0:
            self._setup_recording()

            while True:
                if not self._update_recording():
                    break

            self._finalize_recording()

    def _setup_recording(self) -> None:
        acquire_noise = self._module.sample_mode == DigitalInputSampleMode.NOISE

        if self._module.sample_format <= 8:
            self._sample_size = ctypes.sizeof(ctypes.c_uint8)
            self._data_buffer = (ctypes.c_uint8 * self._buffer_size)()
            self._noise_buffer = (ctypes.c_uint8 * self._buffer_size)() if acquire_noise else None
        elif self._module.sample_format <= 16:
            self._sample_size = ctypes.sizeof(ctypes.c_uint16)
            self._data_buffer = (ctypes.c_uint16 * self._buffer_size)()
            self._noise_buffer = (ctypes.c_uint16 * self._buffer_size)() if acquire_noise else None
        elif self._module.sample_format <= 32:
            self._sample_size = ctypes.sizeof(ctypes.c_uint32)
            self._data_buffer = (ctypes.c_uint32 * self._buffer_size)()
            self._noise_buffer = (ctypes.c_uint32 * self._buffer_size)() if acquire_noise else None
        else:
            raise ValueError('sample_format must be 8, 16, or 32.')

        self._buffer_index = 0

    def _update_recording(self) -> bool:
        self._status = self._module.read_status(read_data=True)
        available_samples, lost_samples, corrupted_samples = self._module.record_status

        self._buffer_index += lost_samples
        self._buffer_index %= self._buffer_size

        self._total_samples += lost_samples
        self._total_samples += available_samples
        self._lost_samples += lost_samples
        self._corrupted_samples += corrupted_samples

        sample_index = 0
        while available_samples > 0:
            chunk_size = available_samples
            if self._buffer_index + chunk_size > self._buffer_size:
                chunk_size = self._buffer_size - self._buffer_index

            if self._data_buffer is not None:
                api.dwf_digital_in_status_data2(
                    self._module.device.handle,
                    ctypes.byref(self._data_buffer, self._buffer_index * self._sample_size),
                    sample_index,
                    chunk_size * self._sample_size)

            if self._noise_buffer is not None:
                api.dwf_digital_in_status_noise2(
                    self._module.device.handle,
                    ctypes.byref(self._noise_buffer, self._buffer_index * self._sample_size),
                    sample_index,
                    chunk_size * self._sample_size)

            self._buffer_index += chunk_size
            self._buffer_index %= self._buffer_size
            sample_index += chunk_size
            available_samples -= chunk_size

        return self._status != Status.DONE

    def _finalize_recording(self) -> None:
        if self._data_buffer is not None:
            self._data_samples = Helpers.normalize_ring_buffer(self._data_buffer, self._buffer_index)
            self._data_buffer = None

        if self._noise_buffer is not None:
            self._noise_samples = Helpers.normalize_ring_buffer(self._noise_buffer, self._buffer_index)
            self._noise_buffer = None
