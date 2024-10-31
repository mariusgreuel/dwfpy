"""
Analog Input module for Digilent WaveForms devices.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
import time
from typing import Callable, Optional, Tuple, Union
import numpy as np
from . import bindings as api
from . import device as fwd  # pylint: disable=unused-import
from .constants import (
    AnalogInputCoupling,
    AcquisitionMode,
    FilterMode,
    Status,
    TriggerLengthCondition,
    TriggerSlope,
    TriggerSource,
    TriggerType,
)
from .exceptions import WaveformsError
from .helpers import Helpers
from .analog_recorder import AnalogRecorder


class AnalogInputTrigger:
    """Represents the trigger unit of an Analog Input module."""

    def __init__(self, module):
        self._device = module.device

    @property
    def source(self) -> TriggerSource:
        """Gets or sets the current trigger source setting for the instrument."""
        return TriggerSource(api.dwf_analog_in_trigger_source_get(self._device.handle))

    @source.setter
    def source(self, value: TriggerSource) -> None:
        api.dwf_analog_in_trigger_source_set(self._device.handle, value)

    @property
    def position_min(self) -> float:
        """Gets the minimum supported trigger position in seconds."""
        return api.dwf_analog_in_trigger_position_info(self._device.handle)[0]

    @property
    def position_max(self) -> float:
        """Gets the maximum supported trigger position in seconds."""
        return api.dwf_analog_in_trigger_position_info(self._device.handle)[1]

    @property
    def position_steps(self) -> int:
        """Gets the number of trigger position steps."""
        return int(api.dwf_analog_in_trigger_position_info(self._device.handle)[2])

    @property
    def position(self) -> float:
        """Gets or sets the horizontal trigger position in seconds."""
        return api.dwf_analog_in_trigger_position_get(self._device.handle)

    @position.setter
    def position(self, value: float) -> None:
        api.dwf_analog_in_trigger_position_set(self._device.handle, value)

    @property
    def actual_position(self) -> float:
        """Gets the actual trigger position in seconds."""
        return api.dwf_analog_in_trigger_position_status(self._device.handle)

    @property
    def auto_timeout_min(self) -> float:
        """Gets the minimum auto trigger timeout in seconds."""
        return api.dwf_analog_in_trigger_auto_timeout_info(self._device.handle)[0]

    @property
    def auto_timeout_max(self) -> float:
        """Gets the maximum auto trigger timeout in seconds."""
        return api.dwf_analog_in_trigger_auto_timeout_info(self._device.handle)[1]

    @property
    def auto_timeout_steps(self) -> int:
        """Gets the number of adjustable steps for the auto trigger timeout."""
        return int(api.dwf_analog_in_trigger_auto_timeout_info(self._device.handle)[2])

    @property
    def auto_timeout(self) -> float:
        """Gets or sets the auto trigger timeout in seconds."""
        return api.dwf_analog_in_trigger_auto_timeout_get(self._device.handle)

    @auto_timeout.setter
    def auto_timeout(self, value: float) -> None:
        api.dwf_analog_in_trigger_auto_timeout_set(self._device.handle, value)

    @property
    def hold_off_min(self) -> float:
        """Gets the minimum trigger hold-off time in seconds."""
        return api.dwf_analog_in_trigger_hold_off_info(self._device.handle)[0]

    @property
    def hold_off_max(self) -> float:
        """Gets the maximum trigger hold-off time in seconds."""
        return api.dwf_analog_in_trigger_hold_off_info(self._device.handle)[1]

    @property
    def hold_off_steps(self) -> int:
        """Gets the number of adjustable steps for the trigger hold-off time."""
        return int(api.dwf_analog_in_trigger_hold_off_info(self._device.handle)[2])

    @property
    def hold_off(self) -> float:
        """Gets or sets the trigger hold-off time in seconds."""
        return api.dwf_analog_in_trigger_hold_off_get(self._device.handle)

    @hold_off.setter
    def hold_off(self, value: float) -> None:
        api.dwf_analog_in_trigger_hold_off_set(self._device.handle, value)

    @property
    def type_info(self) -> Tuple[TriggerType, ...]:
        """Gets the supported output types."""
        return Helpers.map_enum_values(TriggerType, api.dwf_analog_in_trigger_type_info(self._device.handle))

    @property
    def type(self) -> TriggerType:
        """Gets or sets the output type."""
        return TriggerType(api.dwf_analog_in_trigger_type_get(self._device.handle))

    @type.setter
    def type(self, value: TriggerType) -> None:
        api.dwf_analog_in_trigger_type_set(self._device.handle, value)

    @property
    def channel_min(self) -> int:
        """Gets the minimum channel index that can be triggered on."""
        return api.dwf_analog_in_trigger_channel_info(self._device.handle)[0]

    @property
    def channel_max(self) -> int:
        """Gets the maximum channel index that can be triggered on."""
        return api.dwf_analog_in_trigger_channel_info(self._device.handle)[1]

    @property
    def channel(self) -> int:
        """Gets or sets the trigger channel."""
        return api.dwf_analog_in_trigger_channel_get(self._device.handle)

    @channel.setter
    def channel(self, value: int) -> None:
        api.dwf_analog_in_trigger_channel_set(self._device.handle, value)

    @property
    def filter_info(self) -> Tuple[FilterMode, ...]:
        """Gets the supported trigger filters."""
        return Helpers.map_enum_values(FilterMode, api.dwf_analog_in_trigger_filter_info(self._device.handle))

    @property
    def filter(self) -> FilterMode:
        """Gets or sets the trigger filter."""
        return FilterMode(api.dwf_analog_in_trigger_filter_get(self._device.handle))

    @filter.setter
    def filter(self, value: FilterMode) -> None:
        api.dwf_analog_in_trigger_filter_set(self._device.handle, value)

    @property
    def level_min(self) -> float:
        """Gets the minimum trigger voltage level."""
        return api.dwf_analog_in_trigger_level_info(self._device.handle)[0]

    @property
    def level_max(self) -> float:
        """Gets the maximum trigger voltage level."""
        return api.dwf_analog_in_trigger_level_info(self._device.handle)[1]

    @property
    def level_steps(self) -> int:
        """Gets the number of trigger voltage level steps."""
        return int(api.dwf_analog_in_trigger_level_info(self._device.handle)[2])

    @property
    def level(self) -> float:
        """Gets or sets the trigger voltage level in volts."""
        return api.dwf_analog_in_trigger_level_get(self._device.handle)

    @level.setter
    def level(self, value: float) -> None:
        api.dwf_analog_in_trigger_level_set(self._device.handle, value)

    @property
    def hysteresis_min(self) -> float:
        """Gets the minimum trigger hysteresis level."""
        return api.dwf_analog_in_trigger_hysteresis_info(self._device.handle)[0]

    @property
    def hysteresis_max(self) -> float:
        """Gets the maximum trigger hysteresis level."""
        return api.dwf_analog_in_trigger_hysteresis_info(self._device.handle)[1]

    @property
    def hysteresis_steps(self) -> int:
        """Gets the number of trigger hysteresis level steps."""
        return int(api.dwf_analog_in_trigger_hysteresis_info(self._device.handle)[2])

    @property
    def hysteresis(self) -> float:
        """Gets or sets the trigger hysteresis level in volts."""
        return api.dwf_analog_in_trigger_hysteresis_get(self._device.handle)

    @hysteresis.setter
    def hysteresis(self, value: float) -> None:
        api.dwf_analog_in_trigger_hysteresis_set(self._device.handle, value)

    @property
    def condition_info(self) -> Tuple[TriggerSlope, ...]:
        """Gets the supported trigger conditions."""
        return Helpers.map_enum_values(TriggerSlope, api.dwf_analog_in_trigger_condition_info(self._device.handle))

    @property
    def condition(self) -> TriggerSlope:
        """Gets or sets the trigger condition."""
        return TriggerSlope(api.dwf_analog_in_trigger_condition_get(self._device.handle))

    @condition.setter
    def condition(self, value: TriggerSlope) -> None:
        api.dwf_analog_in_trigger_condition_set(self._device.handle, value)

    @property
    def length_min(self) -> float:
        """Gets the minimum trigger length in seconds."""
        return api.dwf_analog_in_trigger_length_info(self._device.handle)[0]

    @property
    def length_max(self) -> float:
        """Gets the maximum trigger length in seconds."""
        return api.dwf_analog_in_trigger_length_info(self._device.handle)[1]

    @property
    def length_steps(self) -> int:
        """Gets the number of trigger length steps."""
        return int(api.dwf_analog_in_trigger_length_info(self._device.handle)[2])

    @property
    def length(self) -> float:
        """Gets or sets the trigger length in seconds."""
        return api.dwf_analog_in_trigger_length_get(self._device.handle)

    @length.setter
    def length(self, value: float) -> None:
        api.dwf_analog_in_trigger_length_set(self._device.handle, value)

    @property
    def length_condition_info(self) -> Tuple[TriggerLengthCondition, ...]:
        """Gets the supported trigger length conditions."""
        return Helpers.map_enum_values(
            TriggerLengthCondition,
            api.dwf_analog_in_trigger_length_condition_info(self._device.handle),
        )

    @property
    def length_condition(self) -> TriggerLengthCondition:
        """Gets or sets the trigger length condition."""
        return TriggerLengthCondition(api.dwf_analog_in_trigger_length_condition_get(self._device.handle))

    @length_condition.setter
    def length_condition(self, value: TriggerLengthCondition) -> None:
        api.dwf_analog_in_trigger_length_condition_set(self._device.handle, value)

    @property
    def sampling_source(self) -> TriggerSource:
        """Gets or sets the acquisition data sampling source."""
        return TriggerSource(api.dwf_analog_in_sampling_source_get(self._device.handle))

    @sampling_source.setter
    def sampling_source(self, value: TriggerSource) -> None:
        api.dwf_analog_in_sampling_source_set(self._device.handle, value)

    @property
    def sampling_slope(self) -> TriggerSlope:
        """Gets or sets the sampling slope."""
        return TriggerSlope(api.dwf_analog_in_sampling_slope_get(self._device.handle))

    @sampling_slope.setter
    def sampling_slope(self, value: TriggerSlope) -> None:
        api.dwf_analog_in_sampling_slope_set(self._device.handle, value)

    @property
    def sampling_delay(self) -> float:
        """Gets or sets the sampling delay."""
        return api.dwf_analog_in_sampling_delay_get(self._device.handle)

    @sampling_delay.setter
    def sampling_delay(self, value: float) -> None:
        api.dwf_analog_in_sampling_delay_set(self._device.handle, value)


class AnalogInputChannel:
    """Represents an Analog Input channel."""

    def __init__(self, module, channel):
        self._device = module.device
        self._module = module
        self._channel = channel
        self._label = "ch" + str(channel + 1)

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def module(self) -> "AnalogInput":
        """Gets the Analog Input module."""
        return self._module

    @property
    def index(self) -> int:
        """Gets the channel index."""
        return self._channel

    @property
    def label(self) -> str:
        """Gets or sets the channel label."""
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @property
    def enabled(self) -> bool:
        """Enables or disables the channel."""
        return bool(api.dwf_analog_in_channel_enable_get(self._device.handle, self._channel))

    @enabled.setter
    def enabled(self, value: bool) -> None:
        api.dwf_analog_in_channel_enable_set(self._device.handle, self._channel, value)

    @property
    def adc_bits(self) -> int:
        """Gets the number bits used by the ADC."""
        return api.dwf_analog_in_bits_info(self._device.handle)

    @property
    def filter_info(self) -> Tuple[FilterMode, ...]:
        """Gets the supported acquisition filters."""
        return Helpers.map_enum_values(FilterMode, api.dwf_analog_in_channel_filter_info(self._device.handle))

    @property
    def filter(self) -> FilterMode:
        """Gets or sets the acquisition filter."""
        return FilterMode(api.dwf_analog_in_channel_filter_get(self._device.handle, self._channel))

    @filter.setter
    def filter(self, value: FilterMode) -> None:
        api.dwf_analog_in_channel_filter_set(self._device.handle, self._channel, value)

    @property
    def range_info(self) -> Tuple[float, ...]:
        """Gets the supported channel ranges."""
        volt_steps = (ctypes.c_double * 32)()
        steps = api.dwf_analog_in_channel_range_steps(self._device.handle, volt_steps)
        return tuple(volt_steps)[:steps]

    @property
    def range_min(self) -> float:
        """Gets the minimum channel range."""
        return api.dwf_analog_in_channel_range_info(self._device.handle)[0]

    @property
    def range_max(self) -> float:
        """Gets the maximum channel range."""
        return api.dwf_analog_in_channel_range_info(self._device.handle)[1]

    @property
    def range_steps(self) -> int:
        """Gets the number of channel range steps."""
        return int(api.dwf_analog_in_channel_range_info(self._device.handle)[2])

    @property
    def range(self) -> float:
        """Gets or sets the channel range."""
        return api.dwf_analog_in_channel_range_get(self._device.handle, self._channel)

    @range.setter
    def range(self, value: float) -> None:
        api.dwf_analog_in_channel_range_set(self._device.handle, self._channel, value)

    @property
    def offset_min(self) -> float:
        """Gets the minimum supported offset voltage."""
        return api.dwf_analog_in_channel_offset_info(self._device.handle)[0]

    @property
    def offset_max(self) -> float:
        """Gets the maximum supported offset voltage."""
        return api.dwf_analog_in_channel_offset_info(self._device.handle)[1]

    @property
    def offset_steps(self) -> int:
        """Gets the number of adjustable steps."""
        return int(api.dwf_analog_in_channel_offset_info(self._device.handle)[2])

    @property
    def offset(self) -> float:
        """Gets or sets the channel offset in volts."""
        return api.dwf_analog_in_channel_offset_get(self._device.handle, self._channel)

    @offset.setter
    def offset(self, value: float) -> None:
        api.dwf_analog_in_channel_offset_set(self._device.handle, self._channel, value)

    @property
    def attenuation(self) -> float:
        """Gets or sets the channel attenuation."""
        return api.dwf_analog_in_channel_attenuation_get(self._device.handle, self._channel)

    @attenuation.setter
    def attenuation(self, value: float) -> None:
        api.dwf_analog_in_channel_attenuation_set(self._device.handle, self._channel, value)

    @property
    def bandwidth(self) -> float:
        """Gets or sets the channel bandwidth in Hz."""
        return api.dwf_analog_in_channel_bandwidth_get(self._device.handle, self._channel)

    @bandwidth.setter
    def bandwidth(self, value: float) -> None:
        api.dwf_analog_in_channel_bandwidth_set(self._device.handle, self._channel, value)

    @property
    def impedance(self) -> float:
        """Gets or sets the channel impedance in Ohms."""
        return api.dwf_analog_in_channel_impedance_get(self._device.handle, self._channel)

    @impedance.setter
    def impedance(self, value: float) -> None:
        api.dwf_analog_in_channel_impedance_set(self._device.handle, self._channel, value)

    @property
    def coupling_info(self) -> Tuple[AnalogInputCoupling, ...]:
        """Gets the supported channel coupling modes."""
        return Helpers.map_enum_values(
            AnalogInputCoupling, api.dwf_analog_in_channel_coupling_info(self._device.handle)
        )

    @property
    def coupling(self) -> AnalogInputCoupling:
        """Gets or sets the channel coupling."""
        return AnalogInputCoupling(api.dwf_analog_in_channel_coupling_get(self._device.handle, self._channel))

    @coupling.setter
    def coupling(self, value: AnalogInputCoupling) -> None:
        api.dwf_analog_in_channel_coupling_set(self._device.handle, self._channel, value)

    def get_sample(self) -> float:
        """Gets the last ADC conversion sample.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        return api.dwf_analog_in_status_sample(self._device.handle, self._channel)

    def get_data(self, first_sample: int = 0, sample_count: int = -1, raw: bool = False):
        """Gets the acquired data samples.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        if sample_count < 0:
            sample_count = self._device.analog_input.valid_samples

        if raw:
            samples16 = np.empty(sample_count, dtype=np.short)
            api.dwf_analog_in_status_data16(
                self._device.handle,
                self._channel,
                samples16.ctypes.data_as(ctypes.POINTER(ctypes.c_short)),
                first_sample,
                sample_count,
            )
            return samples16
        else:
            samples = np.empty(sample_count, dtype=np.double)
            api.dwf_analog_in_status_data2(
                self._device.handle,
                self._channel,
                samples.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                first_sample,
                sample_count,
            )
            return samples

    def get_noise(self, first_sample: int = 0, sample_count: int = -1):
        """Gets the acquired noise samples.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        if sample_count < 0:
            sample_count = self._device.analog_input.valid_samples

        min_samples = (ctypes.c_double * sample_count)()
        max_samples = (ctypes.c_double * sample_count)()
        api.dwf_analog_in_status_noise(
            self._device.handle, self._channel, min_samples, max_samples, first_sample, sample_count
        )
        return np.array((min_samples, max_samples)).T

    def setup(
        self,
        range: Optional[float] = None,
        offset: Optional[float] = None,
        coupling: Optional[Union[str, AnalogInputCoupling]] = None,
        bandwidth: Optional[float] = None,
        attenuation: Optional[float] = None,
        impedance: Optional[float] = None,
        filter: Optional[Union[str, FilterMode]] = None,
        enabled: bool = True,
    ) -> None:
        """Sets up the channel for data acquisition.

        Parameters
        ----------
        range : float, optional
            The channel range in Volts.
        offset : float, optional
            The channel offset in Volts.
        coupling : str or AnalogInputCoupling, optional
            The channel coupling.  Can be 'dc' or 'ac'.
        bandwidth : float, optional
            The channel bandwidth in Hz.
        attenuation : float, optional
            The channel attenuation.
        impedance : float, optional
            The channel impedance in Ohms.
        filter : str or FilterMode, optional
            The channel acquisition filter. Can be 'decimate', 'average', or 'min-max'.
        enabled : bool, optional
            If True, then the channel is enabled (default True).
        """
        if range is not None:
            self.range = range
        if offset is not None:
            self.offset = offset
        if coupling is not None:
            self.coupling = Helpers.map_coupling(coupling)
        if bandwidth is not None:
            self.bandwidth = bandwidth
        if attenuation is not None:
            self.attenuation = attenuation
        if impedance is not None:
            self.impedance = impedance
        if filter is not None:
            self.filter = Helpers.map_filter(filter)
        if enabled is not None:
            self.enabled = enabled


class AnalogInput:
    """Analog Input module (Oscilloscope)."""

    def __init__(self, device):
        self._device = device
        self._trigger = AnalogInputTrigger(self)
        self._channels = tuple(
            AnalogInputChannel(self, i) for i in range(api.dwf_analog_in_channel_count(self._device.handle))
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        del exception_type, exception_value, traceback
        self.reset()

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def trigger(self) -> AnalogInputTrigger:
        """Gets the trigger unit."""
        return self._trigger

    @property
    def channels(self) -> Tuple[AnalogInputChannel, ...]:
        """Gets a collection of Analog Input channels."""
        return self._channels

    def __getitem__(self, key) -> AnalogInputChannel:
        if isinstance(key, int):
            return self._channels[key]

        if isinstance(key, str):
            for channel in self._channels:
                if channel.label == key:
                    return channel

        raise IndexError(key)

    @property
    def remaining_samples(self) -> int:
        """Gets the number of samples left in the acquisition.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        return api.dwf_analog_in_status_samples_left(self._device.handle)

    @property
    def valid_samples(self) -> int:
        """Gets the number of valid/acquired data samples.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        return api.dwf_analog_in_status_samples_valid(self._device.handle)

    @property
    def write_index(self) -> int:
        """Gets the buffer write pointer,
        which is needed in scan_screen acquisition mode to display the scan bar.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        return api.dwf_analog_in_status_index_write(self._device.handle)

    @property
    def auto_triggered(self) -> bool:
        """Returns True if the acquisition is auto triggered.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        return bool(api.dwf_analog_in_status_auto_triggered(self._device.handle))

    @property
    def time(self) -> Tuple[int, int, int]:
        """Gets instrument trigger time information.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        return api.dwf_analog_in_status_time(self._device.handle)

    @property
    def record_status(self) -> Tuple[int, int, int]:
        """Gets information about the recording process:
        Returns (available_samples, lost_samples, corrupted_samples)

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        return api.dwf_analog_in_status_record(self._device.handle)

    @property
    def record_length(self) -> float:
        """Gets or sets the record length in seconds."""
        return api.dwf_analog_in_record_length_get(self._device.handle)

    @record_length.setter
    def record_length(self, value: float) -> None:
        api.dwf_analog_in_record_length_set(self._device.handle, value)

    @property
    def counter_max(self) -> float:
        """Gets the maximum count value."""
        return api.dwf_analog_in_counter_info(self._device.handle)[0]

    @property
    def timeout_max(self) -> float:
        """Gets the maximum timeout value."""
        return api.dwf_analog_in_counter_info(self._device.handle)[1]

    @property
    def counter(self) -> float:
        """Gets or sets the current timeout in seconds."""
        return api.dwf_analog_in_counter_get(self._device.handle)

    @counter.setter
    def counter(self, value: float) -> None:
        api.dwf_analog_in_counter_set(self._device.handle, value)

    @property
    def counter_status(self) -> Tuple[float, float, int]:
        """Gets the count, frequency and tick values."""
        return api.dwf_analog_in_counter_status(self._device.handle)

    @property
    def frequency_min(self) -> float:
        """Gets the minimum supported sample frequency."""
        return api.dwf_analog_in_frequency_info(self._device.handle)[0]

    @property
    def frequency_max(self) -> float:
        """Gets the maximum supported sample frequency."""
        return api.dwf_analog_in_frequency_info(self._device.handle)[1]

    @property
    def frequency(self) -> float:
        """Gets or sets the configured sample frequency in Hz."""
        return api.dwf_analog_in_frequency_get(self._device.handle)

    @frequency.setter
    def frequency(self, value: float) -> None:
        api.dwf_analog_in_frequency_set(self._device.handle, value)

    @property
    def buffer_size_min(self) -> int:
        """Gets the minimum supported buffer size."""
        return api.dwf_analog_in_buffer_size_info(self._device.handle)[0]

    @property
    def buffer_size_max(self) -> int:
        """Gets the maximum supported buffer size."""
        return api.dwf_analog_in_buffer_size_info(self._device.handle)[1]

    @property
    def buffer_size(self) -> int:
        """Gets or sets the buffer size."""
        return api.dwf_analog_in_buffer_size_get(self._device.handle)

    @buffer_size.setter
    def buffer_size(self, value: int) -> None:
        api.dwf_analog_in_buffer_size_set(self._device.handle, value)

    @property
    def noise_buffer_size_max(self) -> int:
        """Gets the maximum supported noise buffer size."""
        return api.dwf_analog_in_noise_size_info(self._device.handle)

    @property
    def noise_buffer_size(self) -> int:
        """Gets or sets the noise buffer size."""
        return api.dwf_analog_in_noise_size_get(self._device.handle)

    @noise_buffer_size.setter
    def noise_buffer_size(self, value: int) -> None:
        api.dwf_analog_in_noise_size_set(self._device.handle, value)

    @property
    def acquisition_mode_info(self) -> Tuple[AcquisitionMode, ...]:
        """Gets the supported acquisition modes."""
        return Helpers.map_enum_values(AcquisitionMode, api.dwf_analog_in_acquisition_mode_info(self._device.handle))

    @property
    def acquisition_mode(self) -> AcquisitionMode:
        """Gets or sets the acquisition mode."""
        return AcquisitionMode(api.dwf_analog_in_acquisition_mode_get(self._device.handle))

    @acquisition_mode.setter
    def acquisition_mode(self, value: AcquisitionMode) -> None:
        api.dwf_analog_in_acquisition_mode_set(self._device.handle, value)

    def reset(self) -> None:
        """Resets and configures all instrument parameters to default values."""
        api.dwf_analog_in_reset(self._device.handle)

    def configure(self, reconfigure: bool = False, start: bool = False) -> None:
        """Configures the instrument and optionally starts the acquisition."""
        api.dwf_analog_in_configure(self._device.handle, reconfigure, start)

    def force_trigger(self) -> None:
        """Force trigger of instrument."""
        api.dwf_analog_in_trigger_force(self._device.handle)

    def read_status(self, read_data: bool = False) -> Status:
        """Gets the acquisition state and optionally reads the data."""
        return Status(api.dwf_analog_in_status(self._device.handle, read_data))

    def wait_for_status(self, status, read_data: bool = False) -> None:
        """Waits for the specified acquisition state."""
        while self.read_status(read_data=read_data) != status:
            time.sleep(0.001)

    def setup_channel(
        self,
        channel: int,
        range: Optional[float] = None,
        offset: Optional[float] = None,
        coupling: Optional[Union[str, AnalogInputCoupling]] = None,
        bandwidth: Optional[float] = None,
        attenuation: Optional[float] = None,
        impedance: Optional[float] = None,
        filter: Optional[Union[str, FilterMode]] = None,
        enabled: bool = True,
    ) -> None:
        """Sets up a channel for data acquisition.

        Parameters
        ----------
        channel : int
            The channel to setup.
        range : float, optional
            The channel range in Volts.
        offset : float, optional
            The channel offset in Volts.
        coupling : str or AnalogInputCoupling, optional
            The channel coupling.  Can be 'dc' or 'ac'.
        bandwidth : float, optional
            The channel bandwidth in Hz.
        attenuation : float, optional
            The channel attenuation.
        impedance : float, optional
            The channel impedance in Ohms.
        filter : str or FilterMode, optional
            The channel acquisition filter. Can be 'decimate', 'average', or 'min-max'.
        enabled : bool, optional
            If True, then the channel is enabled (default True).
        """
        self.channels[channel].setup(
            range=range,
            offset=offset,
            coupling=coupling,
            bandwidth=bandwidth,
            attenuation=attenuation,
            impedance=impedance,
            filter=filter,
            enabled=enabled,
        )

    def setup_edge_trigger(
        self,
        channel: int,
        slope: Optional[Union[str, TriggerSlope]] = None,
        level: Optional[float] = None,
        hysteresis: Optional[float] = None,
        position: Optional[float] = None,
        hold_off: Optional[float] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Trigger upon a certain voltage level in the positive or negative slope of the waveform.

        Parameters
        ----------
        channel : int
            The source channel used for triggering.
        slope : str or TriggerSlope, optional
            The trigger slope. Can be 'rising', 'falling', or 'either'.
        level : float, optional
            The trigger level in Volts.
        hysteresis : float, optional
            The trigger hysteresis in Volts.
        position : float, optional
            The horizontal trigger position in seconds.
        hold_off : float, optional
            The trigger hold-off time in seconds.
        mode : str, optional
            The trigger mode. Can be 'normal' or 'auto'.
        """
        self.trigger.source = TriggerSource.DETECTOR_ANALOG_IN
        self.trigger.type = TriggerType.EDGE
        self._set_trigger_parameter(
            channel=channel,
            condition=slope,
            level=level,
            hysteresis=hysteresis,
            position=position,
            hold_off=hold_off,
            mode=mode,
        )

    def setup_pulse_trigger(
        self,
        channel: int,
        condition: Optional[Union[str, TriggerSlope]] = None,
        length_condition: Optional[Union[str, TriggerLengthCondition]] = None,
        length: Optional[float] = None,
        level: Optional[float] = None,
        hysteresis: Optional[float] = None,
        position: Optional[float] = None,
        hold_off: Optional[float] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Trigger upon a positive or negative pulse width when measured at a certain voltage level.

        Parameters
        ----------
        channel : int
            The source channel used for triggering.
        condition : str, optional
            The trigger condition. Can be 'positive' or 'negative'.
        length_condition : str, optional
            The trigger length condition. Can be 'less', 'timeout', or 'more'.
        length : float, optional
            The pulse length in seconds.
        level : float, optional
            The trigger level in Volts.
        hysteresis : float, optional
            The trigger hysteresis in Volts.
        position : float, optional
            The horizontal trigger position in seconds.
        hold_off : float, optional
            The trigger hold-off time in seconds.
        mode : str, optional
            The trigger mode. Can be 'normal' or 'auto'.
        """
        self.trigger.source = TriggerSource.DETECTOR_ANALOG_IN
        self.trigger.type = TriggerType.PULSE
        self._set_trigger_parameter(
            channel=channel,
            condition=condition,
            length_condition=length_condition,
            length=length,
            level=level,
            hysteresis=hysteresis,
            position=position,
            hold_off=hold_off,
            mode=mode,
        )

    def setup_transition_trigger(
        self,
        channel: int,
        condition: Optional[Union[str, TriggerSlope]] = None,
        length_condition: Optional[Union[str, TriggerLengthCondition]] = None,
        length: Optional[float] = None,
        level: Optional[float] = None,
        hysteresis: Optional[float] = None,
        position: Optional[float] = None,
        hold_off: Optional[float] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Sets up a transition trigger.

        Parameters
        ----------
        channel : int
            The source channel used for triggering.
        condition : str, optional
            The trigger condition. Can be 'rising', 'falling', or 'either'.
        length_condition : str, optional
            The trigger length condition. Can be 'less', 'timeout', or 'more'.
        length : float, optional
            The transition length in seconds.
        level : float, optional
            The trigger level in Volts.
        hysteresis : float, optional
            The trigger hysteresis in Volts.
        position : float, optional
            The horizontal trigger position in seconds.
        hold_off : float, optional
            The trigger hold-off time in seconds.
        mode : str, optional
            The trigger mode. Can be 'normal' or 'auto'.
        """
        self.trigger.source = TriggerSource.DETECTOR_ANALOG_IN
        self.trigger.type = TriggerType.TRANSITION
        self._set_trigger_parameter(
            channel=channel,
            condition=condition,
            length_condition=length_condition,
            length=length,
            level=level,
            hysteresis=hysteresis,
            position=position,
            hold_off=hold_off,
            mode=mode,
        )

    def setup_window_trigger(
        self,
        channel: int,
        condition: Optional[Union[str, TriggerSlope]] = None,
        length: Optional[float] = None,
        level: Optional[float] = None,
        hysteresis: Optional[float] = None,
        position: Optional[float] = None,
        hold_off: Optional[float] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Trigger upon a signal entering or exiting a window at certain voltage thresholds.

        Parameters
        ----------
        channel : int
            The source channel used for triggering.
        condition : str, optional
            The trigger condition. Can be 'entering' or 'exiting'.
        length : float, optional
            The window length in seconds.
        level : float, optional
            The trigger level in Volts.
        hysteresis : float, optional
            The trigger hysteresis in Volts.
        position : float, optional
            The horizontal trigger position in seconds.
        hold_off : float, optional
            The trigger hold-off time in seconds.
        mode : str, optional
            The trigger mode. Can be 'normal' or 'auto'.
        """
        self.trigger.source = TriggerSource.DETECTOR_ANALOG_IN
        self.trigger.type = TriggerType.WINDOW
        self._set_trigger_parameter(
            channel=channel,
            condition=condition,
            length=length,
            level=level,
            hysteresis=hysteresis,
            position=position,
            hold_off=hold_off,
            mode=mode,
        )

    def _set_trigger_parameter(
        self,
        channel: Optional[int] = None,
        condition: Optional[Union[str, TriggerSlope]] = None,
        length_condition: Optional[Union[str, TriggerLengthCondition]] = None,
        length: Optional[float] = None,
        level: Optional[float] = None,
        hysteresis: Optional[float] = None,
        position: Optional[float] = None,
        hold_off: Optional[float] = None,
        mode: Optional[str] = None,
    ) -> None:
        if channel is not None:
            self.trigger.channel = self[channel].index
        if condition is not None:
            self.trigger.condition = Helpers.map_trigger_slope(condition)
        if length_condition is not None:
            self.trigger.length_condition = Helpers.map_trigger_length_condition(length_condition)
        if length is not None:
            self.trigger.length = length
        if level is not None:
            self.trigger.level = level
        if hysteresis is not None:
            self.trigger.hysteresis = hysteresis
        if position is not None:
            self.trigger.position = position
        if hold_off is not None:
            self.trigger.hold_off = hold_off
        if mode is not None:
            if mode == "normal":
                self.trigger.auto_timeout = 0
            elif mode == "auto":
                self.trigger.auto_timeout = 1
            else:
                raise WaveformsError("Invalid mode.")

    def setup_acquisition(
        self,
        mode: Optional[Union[str, AcquisitionMode]] = None,
        sample_rate: Optional[float] = None,
        buffer_size: Optional[Union[int, float]] = None,
        record_length: Optional[float] = None,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Sets up a new data acquisition.

        Parameters
        ----------
        mode : str or AcquisitionMode, optional
            The sampling mode.
            Can be 'single', 'scan-shift', 'scan-screen', or 'record'.
        sample_rate : float, optional
            The sampling rate in Hz.
        buffer_size : int or float, optional
            The buffer size.
        record_length : float, optional
            The record length in seconds.
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the acquisition is started (default False).
        """
        if mode is not None:
            self.acquisition_mode = Helpers.map_acquisition_mode(mode)
        if sample_rate is not None:
            self.frequency = sample_rate
        if buffer_size is not None:
            self.buffer_size = int(buffer_size)
        if record_length is not None:
            self.record_length = record_length
        if configure or start:
            self.configure(reconfigure=configure, start=start)

    def single(
        self,
        sample_rate: Optional[float] = None,
        buffer_size: Optional[Union[int, float]] = None,
        continuous: bool = True,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Starts a single data acquisition.

        Parameters
        ----------
        sample_rate : float, optional
            The sampling rate in Hz.
        buffer_size : int or float, optional
            The buffer size.
        continuous : bool, optional
            If True, then the instrument is rearmed after the data is retrieved. (default True).
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the acquisition is started (default False).
        """
        self.setup_acquisition(
            AcquisitionMode.SINGLE if continuous else AcquisitionMode.SINGLE1,
            sample_rate=sample_rate,
            buffer_size=buffer_size,
            configure=configure,
            start=start,
        )

        if start:
            self.wait_for_status(Status.DONE, read_data=True)

    def scan_shift(
        self,
        sample_rate: Optional[float] = None,
        buffer_size: Optional[Union[int, float]] = None,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Starts a scan-shift data acquisition.

        Parameters
        ----------
        sample_rate : float, optional
            The sampling rate in Hz.
        buffer_size : int or float, optional
            The buffer size.
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the acquisition is started (default False).
        """
        self.setup_acquisition(
            AcquisitionMode.SCAN_SHIFT,
            sample_rate=sample_rate,
            buffer_size=buffer_size,
            configure=configure,
            start=start,
        )

    def scan_screen(
        self,
        sample_rate: Optional[float] = None,
        buffer_size: Optional[Union[int, float]] = None,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Starts a scan-screen data acquisition.

        Parameters
        ----------
        sample_rate : float, optional
            The sampling rate in Hz.
        buffer_size : int or float, optional
            The buffer size.
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the acquisition is started (default False).
        """
        self.setup_acquisition(
            AcquisitionMode.SCAN_SCREEN,
            sample_rate=sample_rate,
            buffer_size=buffer_size,
            configure=configure,
            start=start,
        )

    def record(
        self,
        sample_rate: Optional[float] = None,
        length: Optional[float] = None,
        buffer_size: Optional[Union[int, float]] = None,
        callback: Optional[Callable[["AnalogRecorder"], bool]] = None,
        configure: bool = False,
        start: bool = False,
    ) -> AnalogRecorder:
        """Starts a data recording.

        Parameters
        ----------
        sample_rate : float, optional
            The sampling rate in Hz.
        length : float, optional
            The recording length in seconds.
        buffer_size : int or float, optional
            The buffer size.
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the recording is started (default False).

        Returns
        -------
        AnalogRecorder
            The recorder instance.
        """
        self.setup_acquisition(
            AcquisitionMode.RECORD,
            sample_rate=sample_rate,
            record_length=length,
            buffer_size=buffer_size,
            configure=configure,
        )

        recorder = AnalogRecorder(self)

        if start:
            recorder.record(callback)

        return recorder
