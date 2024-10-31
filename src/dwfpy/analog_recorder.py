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
from typing import Callable, Tuple, List, Optional
import numpy as np
from . import bindings as api
from . import analog_input as fwd  # pylint: disable=unused-import
from .constants import Status


class AnalogRecorder:
    """Recorder for Analog Input data"""

    class ChannelData:
        """Represents the acquired data of a channel."""

        def __init__(self):
            self._data_samples = None

        @property
        def data_samples(self):
            """Gets the acquired data samples."""
            return self._data_samples

    def __init__(self, module: "fwd.AnalogInput"):
        self._module = module

        self._is_setup = False
        self._buffer_size = 0
        self._buffer_index = 0
        self._data_buffers: List[Optional[ctypes.Array]] = []

        self._status = Status.READY
        self._requested_samples = 0
        self._total_samples = 0
        self._lost_samples = 0
        self._corrupted_samples = 0
        self._channels = tuple(self.ChannelData() for _ in module.channels)

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
    def channels(self) -> Tuple[ChannelData, ...]:
        """Gets a collection of data channels."""
        return self._channels

    def record(self, callback: Optional[Callable[["AnalogRecorder"], bool]] = None) -> None:
        """Starts the recording and processes all samples until the recording is complete.

        Parameters
        ----------
        callback : function
            A user-defined function that is called every time a data chunk is processed.
            Return True to continue recording, False to abort the recording.

        Notes
        -----
        This function blocks until the recording is complete.
        """
        if not self._is_setup:
            self._setup_recording()

            if self._is_setup:
                self._module.configure(start=True)

        if self._is_setup:
            while True:
                again_status = self._process_recording()
                again_user = callback(self) if callback is not None else True
                if not again_status or not again_user:
                    break

            self._finalize_recording()

    def process(self) -> bool:
        """Checks the instrument status and processes a chunk of data if available.

        Returns
        -------
        bool
            If True, then if there is more data to process, and the function must be called again.
            If False, the recording is complete, and you must stop calling this function.

        Notes
        -----
        This function must be called repeatedly by the user to process the recording data.
        Failure to call this function in a timely manner
        will cause samples to get lost or corrupted.
        """
        if not self._is_setup:
            self._setup_recording()

            if self._is_setup:
                self._module.configure(start=True)

        if self._is_setup:
            again = self._process_recording()
            if not again:
                self._finalize_recording()

            return again

        return False

    def _setup_recording(self) -> None:
        self._channels = tuple(self.ChannelData() for _ in self._module.channels)

        self._buffer_size = round(self._module.record_length * self._module.frequency)
        if self._buffer_size > 0:
            self._requested_samples = self._buffer_size

            self._buffer_index = 0

            self._data_buffers = []
            for channel in self._module.channels:
                self._data_buffers.append((ctypes.c_double * self._buffer_size)() if channel.enabled else None)

            self._is_setup = True

    def _process_recording(self) -> bool:
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

            for i, data_buffer in enumerate(self._data_buffers):
                if data_buffer is not None:
                    api.dwf_analog_in_status_data2(
                        self._module.device.handle,
                        i,
                        self._byref_double(data_buffer, self._buffer_index),
                        sample_index,
                        chunk_size,
                    )

            self._buffer_index += chunk_size
            self._buffer_index %= self._buffer_size
            sample_index += chunk_size
            available_samples -= chunk_size

        return self._status != Status.DONE

    def _finalize_recording(self) -> None:
        for i, data_buffer in enumerate(self._data_buffers):
            if data_buffer is not None:
                # pylint: disable-next=protected-access
                self._channels[i]._data_samples = self._normalize_ring_buffer(data_buffer, self._buffer_index)

        self._is_setup = False

    @staticmethod
    def _byref_double(c_buffer, index):
        pointer = ctypes.byref(c_buffer, index * ctypes.sizeof(ctypes.c_double))
        return ctypes.cast(pointer, ctypes.POINTER(ctypes.c_double))

    @staticmethod
    def _normalize_ring_buffer(buffer: ctypes.Array, index: int):
        array = np.array(buffer)
        return array if index == 0 else np.concatenate([array[index:], array[:index]])
