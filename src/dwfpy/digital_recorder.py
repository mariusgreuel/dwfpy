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
from typing import Callable, Optional
import numpy as np
from . import bindings as api
from . import digital_input as fwd  # pylint: disable=unused-import
from .constants import DigitalInputSampleMode, Status


class DigitalRecorder:
    """Recorder for Digital Input data"""

    def __init__(self, module: "fwd.DigitalInput"):
        self._module = module

        self._is_setup = False
        self._sample_size = 0
        self._buffer_size = 0
        self._buffer_index = 0
        self._data_buffer: Optional[ctypes.Array] = None
        self._noise_buffer: Optional[ctypes.Array] = None

        self._status = Status.READY
        self._acquire_noise = False
        self._requested_samples = 0
        self._total_samples = 0
        self._lost_samples = 0
        self._corrupted_samples = 0
        self._data_samples = None
        self._noise_samples = None

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
    def data_samples(self):
        """Gets the acquired data samples."""
        return self._data_samples

    @property
    def noise_samples(self):
        """Gets the acquired noise samples."""
        return self._noise_samples

    def record(self, callback: Optional[Callable[["DigitalRecorder"], bool]] = None) -> None:
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
        self._acquire_noise = self._module.sample_mode == DigitalInputSampleMode.NOISE

        self._requested_samples = 0
        self._data_samples = None
        self._noise_samples = None

        self._buffer_size = self._module.trigger.prefill + self._module.trigger.position
        if self._buffer_size > 0:
            self._requested_samples = self._buffer_size

            self._buffer_index = 0

            if self._module.sample_format <= 8:
                self._sample_size = ctypes.sizeof(ctypes.c_uint8)
                self._data_buffer = (ctypes.c_uint8 * self._buffer_size)()
                self._noise_buffer = (ctypes.c_uint8 * self._buffer_size)() if self._acquire_noise else None
            elif self._module.sample_format <= 16:
                self._sample_size = ctypes.sizeof(ctypes.c_uint16)
                self._data_buffer = (ctypes.c_uint16 * self._buffer_size)()
                self._noise_buffer = (ctypes.c_uint16 * self._buffer_size)() if self._acquire_noise else None
            elif self._module.sample_format <= 32:
                self._sample_size = ctypes.sizeof(ctypes.c_uint32)
                self._data_buffer = (ctypes.c_uint32 * self._buffer_size)()
                self._noise_buffer = (ctypes.c_uint32 * self._buffer_size)() if self._acquire_noise else None
            else:
                raise ValueError("sample_format must be 8, 16, or 32")

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

            if self._data_buffer is not None:
                api.dwf_digital_in_status_data2(
                    self._module.device.handle,
                    ctypes.byref(self._data_buffer, self._buffer_index * self._sample_size),
                    sample_index,
                    chunk_size * self._sample_size,
                )

            if self._noise_buffer is not None:
                api.dwf_digital_in_status_noise2(
                    self._module.device.handle,
                    ctypes.byref(self._noise_buffer, self._buffer_index * self._sample_size),
                    sample_index,
                    chunk_size * self._sample_size,
                )

            self._buffer_index += chunk_size
            self._buffer_index %= self._buffer_size
            sample_index += chunk_size
            available_samples -= chunk_size

        return self._status != Status.DONE

    def _finalize_recording(self) -> None:
        if self._data_buffer is not None:
            self._data_samples = self._normalize_ring_buffer(self._data_buffer, self._buffer_index)
            self._data_buffer = None

        if self._noise_buffer is not None:
            self._noise_samples = self._normalize_ring_buffer(self._noise_buffer, self._buffer_index)
            self._noise_buffer = None

        self._is_setup = False

    @staticmethod
    def _normalize_ring_buffer(buffer: ctypes.Array, index: int):
        array = np.array(buffer)
        return array if index == 0 else np.concatenate([array[index:], array[:index]])

    def stream(self, callback: Callable[["DigitalRecorder"], bool]) -> None:
        """Starts the streaming.

        Parameters
        ----------
        callback : function
            A user-defined function that is called every time a data chunk is processed.
            Return True to continue streaming, False to stop the streaming.
        """
        if not self._is_setup:
            self._setup_streaming()

            if self._is_setup:
                self._module.configure(start=True)

        if self._is_setup:
            while True:
                again_status = self._update_streaming()
                again_user = callback(self)
                if not again_status or not again_user:
                    break

            self._finalize_streaming()

    def _setup_streaming(self) -> None:
        self._acquire_noise = self._module.sample_mode == DigitalInputSampleMode.NOISE

        self._requested_samples = 0
        self._buffer_size = 0
        self._data_samples = None
        self._noise_samples = None

        self._is_setup = True

    def _update_streaming(self) -> bool:
        self._status = self._module.read_status(read_data=True)
        available_samples, lost_samples, corrupted_samples = self._module.record_status

        self._total_samples += lost_samples
        self._total_samples += available_samples
        self._lost_samples += lost_samples
        self._corrupted_samples += corrupted_samples

        self._data_samples = self._module.get_data(sample_count=available_samples)

        if self._acquire_noise:
            self._noise_samples = self._module.get_noise(sample_count=available_samples)

        return self._status != Status.DONE

    def _finalize_streaming(self) -> None:
        self._status = Status.DONE
        self._is_setup = False
