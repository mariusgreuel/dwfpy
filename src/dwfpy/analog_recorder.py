"""
Recorder for Analog Input data.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
from typing import Tuple, List, Optional
from . import bindings as api
from . import analog_input as fwd  # pylint: disable=unused-import
from .constants import Status
from .helpers import Helpers


class AnalogRecorder:
    """Recorder for Analog Input data"""

    class ChannelData:
        """Represents the acquired data of a channel."""
        def __init__(self):
            self._data_samples = None

        @property
        def data_samples(self) -> tuple:
            """Gets the acquired data samples."""
            return self._data_samples

    def __init__(self, module: 'fwd.AnalogInput'):
        self._module = module

        self._requested_samples = 0
        self._total_samples = 0
        self._lost_samples = 0
        self._corrupted_samples = 0
        self._channels = tuple(self.ChannelData() for _ in module.channels)

        self._buffer_size = 0
        self._buffer_index = 0
        self._data_buffers: List[Optional[ctypes.Array]] = []

    @property
    def requested_samples(self) -> int:
        """Gets the number of requested samples."""
        return self._requested_samples

    @property
    def total_samples(self) -> int:
        """Gets the number of acquired and lost samples."""
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
    def channels(self) -> Tuple[ChannelData, ...]:
        """Gets a collection of data channels."""
        return self._channels

    def start(self, sample_count: int) -> None:
        """Starts the recording."""
        self._requested_samples = sample_count
        self._buffer_size = sample_count

        self._setup_recording()

        while self._update_recording():
            pass

        self._finalize_recording()

    def process(self) -> bool:
        """Retrieves and stores samples of the recording.
        This function should be called in a tight loop until the recording is complete.
        Returns False, if the processing is complete and the caller should cease calling this function.
        """
        more_data = self._update_recording()
        if not more_data:
            self._finalize_recording()

        return more_data

    def _setup_recording(self) -> None:
        self._data_buffers = []
        for channel in self._module.channels:
            self._data_buffers.append((ctypes.c_double * self._buffer_size)() if channel.enabled else None)

        self._buffer_index = 0

    def _update_recording(self) -> bool:
        status = self._module.read_status(read_data=True)
        available_samples, lost_samples, corrupted_samples = self._module.record_status

        self._buffer_index += lost_samples
        self._buffer_index %= self._buffer_size

        self._total_samples += lost_samples
        self._total_samples += available_samples
        self._lost_samples += lost_samples
        self._corrupted_samples += corrupted_samples

        sample_index = 0
        if available_samples > 0:
            chunk_size = available_samples
            if self._buffer_index + chunk_size > self._buffer_size:
                chunk_size = self._buffer_size - self._buffer_index

            for i, data_buffer in enumerate(self._data_buffers):
                if data_buffer is not None:
                    api.dwf_analog_in_status_data2(
                        self._module.device.handle,
                        i,
                        self._byref_double(data_buffer, self._buffer_index),
                        sample_index,
                        chunk_size)

            self._buffer_index += chunk_size
            self._buffer_index %= self._buffer_size
            sample_index += chunk_size
            available_samples -= chunk_size

        return status != Status.DONE

    def _finalize_recording(self) -> None:
        for i, data_buffer in enumerate(self._data_buffers):
            if data_buffer is not None:
                self._channels[i]._data_samples = Helpers.normalize_ring_buffer(data_buffer, self._buffer_index)

    @staticmethod
    def _byref_double(c_buffer, index):
        pointer = ctypes.byref(c_buffer, index * ctypes.sizeof(ctypes.c_double))
        return ctypes.cast(pointer, ctypes.POINTER(ctypes.c_double))
