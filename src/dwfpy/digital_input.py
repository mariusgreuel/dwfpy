"""
Digital Input module for Digilent WaveForms devices.
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
    AcquisitionMode,
    DigitalInputClockSource,
    DigitalInputSampleMode,
    Status,
    TriggerSlope,
    TriggerSource,
)
from .helpers import Helpers
from .digital_recorder import DigitalRecorder


class DigitalInputClock:
    """Represents the clock unit of a Digital Input device."""

    def __init__(self, module):
        self._device = module.device

    @property
    def frequency(self) -> float:
        """Gets the internal clock frequency in Hz."""
        return api.dwf_digital_in_internal_clock_info(self._device.handle)

    @property
    def source_info(self) -> Tuple[DigitalInputClockSource, ...]:
        """Gets the supported clock sources."""
        return Helpers.map_enum_values(
            DigitalInputClockSource, api.dwf_digital_in_clock_source_info(self._device.handle)
        )

    @property
    def source(self) -> DigitalInputClockSource:
        """Gets or sets the clock source."""
        return DigitalInputClockSource(api.dwf_digital_in_clock_source_get(self._device.handle))

    @source.setter
    def source(self, value: DigitalInputClockSource) -> None:
        api.dwf_digital_in_clock_source_set(self._device.handle, value)

    @property
    def divider_max(self) -> int:
        """Gets the maximum supported clock divider value."""
        return api.dwf_digital_in_divider_info(self._device.handle)

    @property
    def divider(self) -> int:
        """Gets or sets the configured clock divider value."""
        return api.dwf_digital_in_divider_get(self._device.handle)

    @divider.setter
    def divider(self, value: int) -> None:
        api.dwf_digital_in_divider_set(self._device.handle, value)


class DigitalInputTrigger:
    """Represents the trigger unit of a Digital Input device."""

    def __init__(self, module):
        self._device = module.device

    @property
    def source(self) -> TriggerSource:
        """Gets or sets the current trigger source setting for the instrument."""
        return TriggerSource(api.dwf_digital_in_trigger_source_get(self._device.handle))

    @source.setter
    def source(self, value: TriggerSource) -> None:
        api.dwf_digital_in_trigger_source_set(self._device.handle, value)

    @property
    def slope(self) -> TriggerSlope:
        """Gets or sets the trigger slope for the instrument."""
        return TriggerSlope(api.dwf_digital_in_trigger_slope_get(self._device.handle))

    @slope.setter
    def slope(self, value: TriggerSlope) -> None:
        api.dwf_digital_in_trigger_slope_set(self._device.handle, value)

    @property
    def position_max(self) -> int:
        """Gets the maximum values of the trigger position in samples."""
        return api.dwf_digital_in_trigger_position_info(self._device.handle)

    @property
    def position(self) -> int:
        """Gets or sets the number of samples to acquire after trigger."""
        return api.dwf_digital_in_trigger_position_get(self._device.handle)

    @position.setter
    def position(self, value: int) -> None:
        api.dwf_digital_in_trigger_position_set(self._device.handle, value)

    @property
    def prefill(self) -> int:
        """Gets or sets the number of samples to acquire
        before arming in 'record' acquisition mode."""
        return api.dwf_digital_in_trigger_prefill_get(self._device.handle)

    @prefill.setter
    def prefill(self, value: int) -> None:
        api.dwf_digital_in_trigger_prefill_set(self._device.handle, value)

    @property
    def auto_timeout_min(self) -> float:
        """Gets the minimum auto trigger timeout in seconds."""
        return api.dwf_digital_in_trigger_auto_timeout_info(self._device.handle)[0]

    @property
    def auto_timeout_max(self) -> float:
        """Gets the maximum auto trigger timeout in seconds."""
        return api.dwf_digital_in_trigger_auto_timeout_info(self._device.handle)[1]

    @property
    def auto_timeout_steps(self) -> int:
        """Gets the number of adjustable steps of the timeout."""
        return int(api.dwf_digital_in_trigger_auto_timeout_info(self._device.handle)[2])

    @property
    def auto_timeout(self) -> float:
        """Gets or sets the auto trigger timeout in seconds."""
        return api.dwf_digital_in_trigger_auto_timeout_get(self._device.handle)

    @auto_timeout.setter
    def auto_timeout(self, value: float) -> None:
        api.dwf_digital_in_trigger_auto_timeout_set(self._device.handle, value)

    def get_trigger_mask_info(self) -> int:
        """Gets the supported triggers as a bit-mask.
        Returs (low_level, high_level, rising_edge, falling_edge)"""
        return api.dwf_digital_in_trigger_info(self._device.handle)

    def get_trigger_mask(self) -> Tuple[int, int, int, int]:
        """Gets state and edge trigger condition as a bit-mask.
        Returs (low_level, high_level, rising_edge, falling_edge)"""
        return api.dwf_digital_in_trigger_get(self._device.handle)

    def set_trigger_mask(
        self,
        low_level: int = 0,
        high_level: int = 0,
        rising_edge: int = 0,
        falling_edge: int = 0,
    ) -> None:
        """Sets state and edge trigger conditions as a bit-mask."""
        api.dwf_digital_in_trigger_set(self._device.handle, low_level, high_level, rising_edge, falling_edge)

    def set_reset_mask(
        self,
        low_level: int = 0,
        high_level: int = 0,
        rising_edge: int = 0,
        falling_edge: int = 0,
    ) -> None:
        """Configures the trigger reset condition as a bit-mask."""
        api.dwf_digital_in_trigger_reset_set(self._device.handle, low_level, high_level, rising_edge, falling_edge)

    def set_counter(self, count: int, restart: bool = False) -> None:
        """Configures the trigger counter."""
        api.dwf_digital_in_trigger_count_set(self._device.handle, count, restart)

    def set_length(self, min_length: float, max_length: float, sync_mode: int) -> None:
        """Configures the trigger timing."""
        api.dwf_digital_in_trigger_length_set(self._device.handle, min_length, max_length, sync_mode)

    def set_match(self, pin, mask: int, value: int, bit_stuffing: int) -> None:
        """Configures the trigger deserializer."""
        api.dwf_digital_in_trigger_match_set(self._device.handle, pin, mask, value, bit_stuffing)


class DigitalInputChannelTrigger:
    """Represents the trigger unit of a Digital Input channel."""

    def __init__(self, channel):
        self._module = channel.module
        self._channel = channel

    @property
    def supports_low_level(self) -> bool:
        """Returns True if the trigger detector supports
        a low-level trigger for this channel."""
        low, _, _, _ = self._module.trigger.get_trigger_mask_info()
        return bool(low & self._mask)

    @property
    def supports_high_level(self) -> bool:
        """Returns True if the trigger detector supports
        a high-level trigger for this channel."""
        _, high, _, _ = self._module.trigger.get_trigger_mask_info()
        return bool(high & self._mask)

    @property
    def supports_rising_edge(self) -> bool:
        """Returns True if the trigger detector supports
        a edge-rise trigger for this channel."""
        _, _, rise, _ = self._module.trigger.get_trigger_mask_info()
        return bool(rise & self._mask)

    @property
    def supports_falling_edge(self) -> bool:
        """Returns True if the trigger detector supports
        a edge-fall trigger for this channel."""
        _, _, _, fall = self._module.trigger.get_trigger_mask_info()
        return bool(fall & self._mask)

    @property
    def low_level(self) -> bool:
        """Gets or sets the low-level trigger for this channel."""
        low, _, _, _ = self._module.trigger.get_trigger_mask()
        return bool(low & self._mask)

    @low_level.setter
    def low_level(self, value: bool) -> None:
        low, high, rise, fall = self._module.trigger.get_trigger_mask()
        low = (low | self._mask) if value else (low & ~self._mask)
        self._module.trigger.set_trigger_mask(low, high, rise, fall)

    @property
    def high_level(self) -> bool:
        """Gets or sets the high-level trigger for this channel."""
        _, high, _, _ = self._module.trigger.get_trigger_mask()
        return bool(high & self._mask)

    @high_level.setter
    def high_level(self, value: bool) -> None:
        low, high, rise, fall = self._module.trigger.get_trigger_mask()
        high = (high | self._mask) if value else (high & ~self._mask)
        self._module.trigger.set_trigger_mask(low, high, rise, fall)

    @property
    def rising_edge(self) -> bool:
        """Gets or sets the edge-rise trigger for this channel."""
        _, _, rise, _ = self._module.trigger.get_trigger_mask()
        return bool(rise & self._mask)

    @rising_edge.setter
    def rising_edge(self, value: bool) -> None:
        low, high, rise, fall = self._module.trigger.get_trigger_mask()
        rise = (rise | self._mask) if value else (rise & ~self._mask)
        self._module.trigger.set_trigger_mask(low, high, rise, fall)

    @property
    def falling_edge(self) -> bool:
        """Gets or sets the edge-fall trigger for this channel."""
        _, _, _, fall = self._module.trigger.get_trigger_mask()
        return bool(fall & self._mask)

    @falling_edge.setter
    def falling_edge(self, value: bool) -> None:
        low, high, rise, fall = self._module.trigger.get_trigger_mask()
        fall = (fall | self._mask) if value else (fall & ~self._mask)
        self._module.trigger.set_trigger_mask(low, high, rise, fall)

    @property
    def _mask(self) -> int:
        return 1 << self._channel.index


class DigitalInputChannel:
    """Represents a Digital Input channel."""

    def __init__(self, module, channel):
        self._device = module.device
        self._module = module
        self._channel = channel
        self._label = "dio" + str(channel)
        self._trigger = DigitalInputChannelTrigger(self)

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def module(self) -> "DigitalInput":
        """Gets the Digital Input module."""
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
    def trigger(self) -> DigitalInputChannelTrigger:
        """Gets the trigger unit."""
        return self._trigger

    def setup_trigger(self, condition: str) -> None:
        """Sets up the trigger condition for this channel.

        Parameters
        ----------
        condition : str
            The trigger condition. Can be 'ignore', 'low', 'high', 'rise', 'fall', or 'edge'.
        """
        low, high, rise, fall = self._module.trigger.get_trigger_mask()
        self._module.trigger.set_trigger_mask(*self._calc_trigger(condition, low, high, rise, fall))

    def setup_reset_trigger(self, condition: str) -> None:
        """Sets up the trigger reset condition for this channel.

        Parameters
        ----------
        condition : str
            The trigger condition. Can be 'ignore', 'low', 'high', 'rise', 'fall', or 'edge'.
        """
        self._module.trigger.set_reset_mask(*self._calc_trigger(condition, 0, 0, 0, 0))

    def _calc_trigger(self, condition, low, high, rise, fall) -> Tuple[int, int, int, int]:
        mask = 1 << self._channel

        if condition == "ignore":
            low &= ~mask
            high &= ~mask
            rise &= ~mask
            fall &= ~mask
        elif condition == "low":
            low |= mask
            high &= ~mask
            rise &= ~mask
            fall &= ~mask
        elif condition == "high":
            low &= ~mask
            high |= mask
            rise &= ~mask
            fall &= ~mask
        elif condition == "rise":
            low &= ~mask
            high &= ~mask
            rise |= mask
            fall &= ~mask
        elif condition == "fall":
            low &= ~mask
            high &= ~mask
            rise &= ~mask
            fall |= mask
        elif condition == "edge":
            low &= ~mask
            high &= ~mask
            rise |= mask
            fall |= mask
        else:
            raise ValueError("Trigger condition must be 'ignore', 'low', 'high', 'rise', 'fall', or 'edge'")

        return low, high, rise, fall


class DigitalInput:
    """Digital Input module (Logic Analyzer)."""

    def __init__(self, device):
        self._device = device
        self._clock = DigitalInputClock(self)
        self._trigger = DigitalInputTrigger(self)
        self._channels = tuple(
            DigitalInputChannel(self, i) for i in range(api.dwf_digital_in_bits_info(self._device.handle))
        )
        self._dio_first = False

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
    def clock(self) -> DigitalInputClock:
        """Gets the clock unit."""
        return self._clock

    @property
    def trigger(self) -> DigitalInputTrigger:
        """Gets the trigger unit."""
        return self._trigger

    @property
    def channels(self):
        """Gets a collection of Digital Input channels."""
        return self._channels

    def __getitem__(self, key) -> DigitalInputChannel:
        if isinstance(key, int):
            return self._channels[key]

        if isinstance(key, str):
            for channel in self._channels:
                if channel.label == key:
                    return channel

        raise IndexError(key)

    @property
    def dio_first(self) -> bool:
        """Gets or sets a value indicating if DIO pins will be placed in front of the DIN pins."""
        return self._dio_first

    @dio_first.setter
    def dio_first(self, value: bool) -> None:
        self._dio_first = value
        api.dwf_digital_in_input_order_set(self._device.handle, value)

    @property
    def remaining_samples(self) -> int:
        """Gets the number of samples left in the acquisition."""
        return api.dwf_digital_in_status_samples_left(self._device.handle)

    @property
    def valid_samples(self) -> int:
        """Gets the number of valid/acquired data samples."""
        return api.dwf_digital_in_status_samples_valid(self._device.handle)

    @property
    def write_index(self) -> int:
        """Gets the buffer write pointer which is needed in scan_screen acquisition mode
        to display the scan bar."""
        return api.dwf_digital_in_status_index_write(self._device.handle)

    @property
    def auto_triggered(self) -> bool:
        """Returns True if the acquisition is auto triggered."""
        return bool(api.dwf_digital_in_status_auto_triggered(self._device.handle))

    @property
    def record_status(self) -> Tuple[int, int, int]:
        """Gets information about the recording process.
        Returns (available_samples, lost_samples, corrupted_samples)"""
        return api.dwf_digital_in_status_record(self._device.handle)

    @property
    def time(self) -> None:
        """Returns instrument trigger time information."""
        return api.dwf_digital_in_status_time(self._device.handle)

    @property
    def sample_rate(self) -> float:
        """Gets or sets the sample rate."""
        return self.clock.frequency / self.clock.divider

    @sample_rate.setter
    def sample_rate(self, value: float) -> None:
        self.clock.divider = round(self.clock.frequency / value)

    @property
    def sample_format(self) -> int:
        """Gets or sets the number of bits to be sampled. Can be 8, 16, or 32."""
        return api.dwf_digital_in_sample_format_get(self._device.handle)

    @sample_format.setter
    def sample_format(self, value: int) -> None:
        api.dwf_digital_in_sample_format_set(self._device.handle, value)

    @property
    def buffer_size_max(self) -> int:
        """Gets the maximum supported buffer size."""
        return api.dwf_digital_in_buffer_size_info(self._device.handle)

    @property
    def buffer_size(self) -> int:
        """Gets or sets the buffer size."""
        return api.dwf_digital_in_buffer_size_get(self._device.handle)

    @buffer_size.setter
    def buffer_size(self, value: int) -> None:
        api.dwf_digital_in_buffer_size_set(self._device.handle, value)

    @property
    def sample_mode_info(self) -> Tuple[DigitalInputSampleMode, ...]:
        """Gets the supported sample modes."""
        return Helpers.map_enum_values(DigitalInputSampleMode, api.dwf_digital_in_sample_mode_info(self._device.handle))

    @property
    def sample_mode(self) -> DigitalInputSampleMode:
        """Gets or sets the sample mode."""
        return DigitalInputSampleMode(api.dwf_digital_in_sample_mode_get(self._device.handle))

    @sample_mode.setter
    def sample_mode(self, value: DigitalInputSampleMode) -> None:
        api.dwf_digital_in_sample_mode_set(self._device.handle, value)

    @property
    def sample_sensible(self) -> int:
        """Gets or sets the signals to be used for data compression in record acquisition mode."""
        return api.dwf_digital_in_sample_sensible_get(self._device.handle)

    @sample_sensible.setter
    def sample_sensible(self, value: int) -> None:
        api.dwf_digital_in_sample_sensible_set(self._device.handle, value)

    @property
    def acquisition_mode_info(self) -> Tuple[AcquisitionMode, ...]:
        """Gets the supported acquisition modes."""
        return Helpers.map_enum_values(AcquisitionMode, api.dwf_digital_in_acquisition_mode_info(self._device.handle))

    @property
    def acquisition_mode(self) -> AcquisitionMode:
        """Gets or sets the acquisition mode."""
        return AcquisitionMode(api.dwf_digital_in_acquisition_mode_get(self._device.handle))

    @acquisition_mode.setter
    def acquisition_mode(self, value: AcquisitionMode) -> None:
        api.dwf_digital_in_acquisition_mode_set(self._device.handle, value)

    def reset(self) -> None:
        """Resets and configures all instrument parameters to default values."""
        api.dwf_digital_in_reset(self._device.handle)

    def configure(self, reconfigure: bool = False, start: bool = False) -> None:
        """Configures the instrument and starts the acquisition.."""
        api.dwf_digital_in_configure(self._device.handle, reconfigure, start)

    def read_status(self, read_data: bool = False) -> Status:
        """Gets the acquisition state and optionally reads the data."""
        return Status(api.dwf_digital_in_status(self._device.handle, read_data))

    def wait_for_status(self, status, read_data: bool = False) -> None:
        """Waits for the specified acquisition state."""
        while self.read_status(read_data=read_data) != status:
            time.sleep(0.001)

    def get_data(self, first_sample: int = 0, sample_count: int = -1):
        """Gets the acquired data samples.

        Notes
        -----
        Before calling this function, call the 'read_status()' function
        to read the data from the device.
        """
        if sample_count < 0:
            sample_count = self.valid_samples

        samples = self._create_sample_buffer(sample_count)
        api.dwf_digital_in_status_data2(
            self._device.handle,
            samples.ctypes.data_as(ctypes.c_void_p),
            first_sample,
            samples.size * samples.itemsize,
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
            sample_count = self.valid_samples

        samples = self._create_sample_buffer(sample_count)
        api.dwf_digital_in_status_noise2(
            self._device.handle,
            samples.ctypes.data_as(ctypes.c_void_p),
            first_sample,
            samples.size * samples.itemsize,
        )
        return samples

    def _create_sample_buffer(self, size: int):
        if self.sample_format <= 8:
            return np.empty(size, dtype=np.uint8)

        if self.sample_format <= 16:
            return np.empty(size, dtype=np.uint16)

        if self.sample_format <= 32:
            return np.empty(size, dtype=np.uint32)

        raise ValueError("sample_format must be 8, 16, or 32")

    def setup_trigger(
        self,
        source: Optional[Union[str, TriggerSource]] = None,
        slope: Optional[Union[str, TriggerSlope]] = None,
        position: Optional[int] = None,
        prefill: Optional[int] = None,
        auto_timeout: Optional[float] = None,
    ) -> None:
        """Sets up the trigger condition.

        Parameters
        ----------
        source : str, optional
            The trigger source.
            Can be 'none', 'pc',
            'detector-analog-in', 'detector-digital-in',
            'analog-in', 'digital-in', 'digital-out',
            'analog-out1', 'analog-out2', 'analog-out3', 'analog-out3',
            'external1', 'external2', 'external3', 'external4',
            'low', 'high', or 'clock'.
        slope : str, optional
            The trigger slope.
            Can be 'rising', 'falling', or 'either'.
        position : int, optional
            The number of samples to be acquired after the trigger.
        prefill : int, optional
            The number of samples to be acquired before the trigger.
        auto_timeout : float, optional
            The auto trigger timeout in seconds.
        """

        if source is not None:
            self._trigger.source = Helpers.map_trigger_source(source)
        if slope is not None:
            self.trigger.slope = Helpers.map_trigger_slope(slope)
        if position is not None:
            self._trigger.position = int(position)
        if prefill is not None:
            self._trigger.prefill = int(prefill)
        if auto_timeout is not None:
            self._trigger.auto_timeout = auto_timeout

    def setup_edge_trigger(self, channel: int, edge: str) -> None:
        """Sets up an edge trigger.

        Parameters
        ----------
        channel : int
            The trigger channel.
        edge : str
            The trigger edge. Can be 'rising' or 'falling'.
        """
        self._setup_condition_trigger(channel, edge)

    def setup_level_trigger(self, channel: int, level: str) -> None:
        """Sets up a level trigger.

        Parameters
        ----------
        channel : int
            The trigger channel.
        level : str
            The trigger level. Can be 'low' or 'high'.
        """
        self._setup_condition_trigger(channel, level)

    def _setup_condition_trigger(self, channel: int, condition: str) -> None:
        self._trigger.source = TriggerSource.DETECTOR_DIGITAL_IN
        if condition == "ignore":
            self.trigger.set_trigger_mask(low_level=0, high_level=0, rising_edge=0, falling_edge=0)
        elif condition == "low":
            self.trigger.set_trigger_mask(low_level=1 << channel)
        elif condition == "high":
            self.trigger.set_trigger_mask(high_level=1 << channel)
        elif condition in ("rise", "rising"):
            self.trigger.set_trigger_mask(rising_edge=1 << channel)
        elif condition in ("fall", "falling"):
            self.trigger.set_trigger_mask(falling_edge=1 << channel)
        elif condition == "edge":
            self.trigger.set_trigger_mask(rising_edge=1 << channel, falling_edge=1 << channel)
        else:
            raise ValueError("Trigger condition must be 'ignore', 'low', 'high', 'rising', 'falling', or 'edge'")

    def setup_glitch_trigger(self, channel: int, polarity: str, less_than: float) -> None:
        """Sets up a glitch trigger.

        Parameters
        ----------
        channel : int
            The trigger channel.
        polarity : str
            The trigger polarity. Can be 'positive' or 'negative'.
        less_than : float
            The maximum pulse width in seconds.
        """
        self._setup_pulse_trigger(channel=channel, polarity=polarity, min_length=0, max_length=less_than)

    def setup_timeout_trigger(self, channel: int, polarity: str, more_than: float) -> None:
        """Sets up a timeout trigger.

        Parameters
        ----------
        channel : int
            The trigger channel.
        polarity : str
            The trigger polarity. Can be 'positive' or 'negative'.
        more_than : float
            The minimum pulse width in seconds.
        """
        self._setup_pulse_trigger(channel=channel, polarity=polarity, min_length=more_than, max_length=0)

    def setup_more_trigger(self, channel: int, polarity: str, more_than: float) -> None:
        """Sets up a more trigger.

        Parameters
        ----------
        channel : int
            The trigger channel.
        polarity : str
            The trigger polarity. Can be 'positive' or 'negative'.
        more_than : float
            The minimum pulse width in seconds.
        """
        self._setup_pulse_trigger(channel=channel, polarity=polarity, min_length=more_than, max_length=-1)

    def setup_length_trigger(self, channel: int, polarity: str, length: float, hysteresis: float = 0.0) -> None:
        """Sets up a length trigger.

        Parameters
        ----------
        channel : int
            The trigger channel.
        polarity : str
            The trigger polarity. Can be 'positive' or 'negative'.
        length : float
            The minimum pulse width in seconds.
        hysteresis : float, optional
            The pulse width hysteresis in seconds.
        """
        self._setup_pulse_trigger(channel=channel, polarity=polarity, min_length=length, max_length=length + hysteresis)

    def _setup_pulse_trigger(self, channel, polarity, min_length, max_length) -> None:
        self._trigger.source = TriggerSource.DETECTOR_DIGITAL_IN

        if polarity in ("pos", "positive"):
            self.trigger.set_trigger_mask(high_level=1 << channel)
            self.trigger.set_reset_mask(rising_edge=1 << channel)
        elif polarity in ("neg", "negative"):
            self.trigger.set_trigger_mask(low_level=1 << channel)
            self.trigger.set_reset_mask(falling_edge=1 << channel)
        else:
            raise ValueError("Trigger polarity must be 'positive' or 'negative'")

        self._trigger.set_length(min_length, max_length, 0)
        self._trigger.set_counter(1)

    def setup_counter_trigger(
        self,
        channel: int,
        condition: str,
        reset_channel: int,
        reset_condition: str,
        max_counter: int,
    ) -> None:
        """Sets up a counter trigger.

        Parameters
        ----------
        channel : int
            The trigger channel.
        condition : str
            The trigger condition.
            Can be 'ignore', 'low', 'high', 'rise', 'fall', or 'edge'.
        reset_channel : int
            The counter reset channel.
        reset_condition : str
            The reset condition.
            Can be 'ignore', 'low', 'high', 'rise', 'fall', or 'edge'.
        max_counter : int
            The maximum counter value.
        """
        self._trigger.source = TriggerSource.DETECTOR_DIGITAL_IN
        self._channels[channel].setup_trigger(condition)
        self._channels[reset_channel].setup_reset_trigger(reset_condition)
        self._trigger.set_counter(max_counter)

    def setup_acquisition(
        self,
        mode: Optional[Union[str, AcquisitionMode]] = None,
        sample_rate: Optional[float] = None,
        sample_format: Optional[int] = None,
        buffer_size: Optional[Union[int, float]] = None,
        position: Optional[Union[int, float]] = None,
        prefill: Optional[Union[int, float]] = None,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Sets up a new data acquisition.

        Parameters
        ----------
        mode : str, optional
            The sampling mode.
            Can be 'single', 'scan-shift', 'scan-screen', or 'record'.
        sample_rate : float, optional
            The sampling frequency in Hz.
        sample_format : int, optional
            The number of bits to be sampled. Can be 8, 16, or 32.
        buffer_size : int or float, optional
            The buffer size.
        position : int or float, optional
            The number of samples to be acquired after the trigger.
        prefill : int or float, optional
            The number of samples to be acquired before the trigger (record mode only).
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the acquisition is started (default False).
        """
        if mode is not None:
            self.acquisition_mode = Helpers.map_acquisition_mode(mode)
        if sample_rate is not None:
            self.sample_rate = sample_rate
        if sample_format is not None:
            self.sample_format = sample_format
        if buffer_size is not None:
            self.buffer_size = int(buffer_size)
        if position is not None:
            self.trigger.position = int(position)
        if prefill is not None:
            self.trigger.prefill = int(prefill)
        if configure or start:
            self.configure(reconfigure=configure, start=start)

    def single(
        self,
        sample_rate: Optional[float] = None,
        sample_format: Optional[int] = None,
        buffer_size: Optional[Union[int, float]] = None,
        position: Optional[Union[int, float]] = None,
        continuous: bool = True,
        configure: bool = False,
        start: bool = False,
    ) -> Optional[Tuple]:
        """Starts a single data acquisition.

        Parameters
        ----------
        sample_rate : float, optional
            The sampling frequency in Hz.
        sample_format : int, optional
            The number of bits to be sampled. Can be 8, 16, or 32.
        buffer_size : int or float, optional
            The buffer size.
        position : int or float, optional
            The number of samples to be acquired after the trigger.
        continuous : bool, optional
            If True, then the instrument is rearmed after the data is retrieved. (default True).
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the acquisition is started (default False).

        Returns
        -------
        tuple
            If ``start`` is True, a tuple of integers containing the data samples.
            None otherwise.
        """
        self.setup_acquisition(
            AcquisitionMode.SINGLE if continuous else AcquisitionMode.SINGLE1,
            sample_rate=sample_rate,
            sample_format=sample_format,
            buffer_size=buffer_size,
            position=position,
            configure=configure,
            start=start,
        )

        if start:
            self.wait_for_status(Status.DONE, read_data=True)
            return self.get_data()

        return None

    def record(
        self,
        sample_rate: Optional[float] = None,
        sample_format: Optional[int] = None,
        sample_sensible: Optional[int] = None,
        sample_count: Optional[Union[int, float]] = None,
        prefill: Optional[Union[int, float]] = None,
        callback: Optional[Callable[["DigitalRecorder"], bool]] = None,
        configure: bool = False,
        start: bool = False,
    ) -> DigitalRecorder:
        """Starts a data recording.

        Parameters
        ----------
        sample_rate : float, optional
            The sampling frequency in Hz.
        sample_format : int, optional
            The number of bits to be sampled. Can be 8, 16, or 32.
        sample_sensible : int, optional
            The signals to be used for data compression, as a bit-mask.
        sample_count : int or float, optional
            The number of samples to be acquired after the trigger.
        prefill : int or float, optional
            The number of samples to be acquired before the trigger.
        callback : function, optional
            A custom function to monitor the recording process.
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the recording is started (default False).

        Returns
        -------
        DigitalRecorder
            The recorder instance.
        """
        if sample_sensible is not None:
            self.sample_sensible = sample_sensible

        self.setup_acquisition(
            AcquisitionMode.RECORD,
            sample_rate=sample_rate,
            sample_format=sample_format,
            position=sample_count,
            prefill=prefill,
            configure=configure,
        )

        recorder = DigitalRecorder(self)

        if start:
            recorder.record(callback)

        return recorder

    def stream(
        self,
        callback: Callable[[DigitalRecorder], bool],
        sample_rate: Optional[float] = None,
        sample_format: Optional[int] = None,
        sample_sensible: Optional[int] = None,
        configure: bool = False,
        start: bool = False,
    ) -> DigitalRecorder:
        """Streams data to a callback function.

        Parameters
        ----------
        callback : function
            A user-defined function to receive the streaming data.
        sample_rate : float, optional
            The sampling frequency in Hz.
        sample_format : int, optional
            The number of bits to be sampled. Can be 8, 16, or 32.
        sample_sensible : int, optional
            The signals to be used for data compression.
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the streaming is started (default False).

        Returns
        -------
        DigitalRecorder
            The recorder instance.
        """
        self.trigger.prefill = 0
        self.trigger.position = 0

        if sample_sensible is not None:
            self.sample_sensible = sample_sensible

        self.setup_acquisition(
            AcquisitionMode.RECORD,
            sample_rate=sample_rate,
            sample_format=sample_format,
            configure=configure,
        )

        recorder = DigitalRecorder(self)

        if start:
            recorder.stream(callback)

        return recorder
