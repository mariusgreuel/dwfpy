"""
Analog Output module for Digilent WaveForms devices.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import ctypes
from typing import Optional, Tuple, List
from . import bindings as api
from . import device as fwd  # pylint: disable=unused-import
from .constants import (
    AnalogOutputIdle,
    AnalogOutputMode,
    AnalogOutputNode,
    Function,
    Status,
    TriggerSlope,
    TriggerSource,
)
from .helpers import Helpers


class AnalogOutputChannelTrigger:
    """Represents the trigger unit of an Analog Output channel."""

    def __init__(self, channel):
        self._device = channel.device
        self._channel = channel.index

    @property
    def source(self) -> TriggerSource:
        """Gets or sets the current trigger source setting for the instrument."""
        return TriggerSource(api.dwf_analog_out_trigger_source_get(self._device.handle, self._channel))

    @source.setter
    def source(self, value: TriggerSource) -> None:
        api.dwf_analog_out_trigger_source_set(self._device.handle, self._channel, value)

    @property
    def slope(self) -> TriggerSlope:
        """Gets or sets the trigger slope for the instrument."""
        return TriggerSlope(api.dwf_analog_out_trigger_slope_get(self._device.handle, self._channel))

    @slope.setter
    def slope(self, value: TriggerSlope) -> None:
        api.dwf_analog_out_trigger_slope_set(self._device.handle, self._channel, value)


class AnalogOutputChannelNode:
    """Represents an Analog Output channel node."""

    def __init__(self, channel, node):
        self._device = channel.device
        self._channel = channel.index
        self._node = node.value

    @property
    def type(self) -> AnalogOutputNode:
        """Gets the node type."""
        return AnalogOutputNode(self._node)

    @property
    def enabled(self) -> bool:
        """Enables the node."""
        return bool(api.dwf_analog_out_node_enable_get(self._device.handle, self._channel, self._node))

    @enabled.setter
    def enabled(self, value: bool) -> None:
        api.dwf_analog_out_node_enable_set(self._device.handle, self._channel, self._node, value)

    @property
    def function_info(self) -> Tuple[Function, ...]:
        """Gets the supported channel nodes."""
        return Helpers.map_enum_values(
            Function,
            api.dwf_analog_out_node_function_info(self._device.handle, self._channel, self._node),
        )

    @property
    def function(self) -> Function:
        """Gets or sets the generator function."""
        return Function(api.dwf_analog_out_node_function_get(self._device.handle, self._channel, self._node))

    @function.setter
    def function(self, value: Function) -> None:
        api.dwf_analog_out_node_function_set(self._device.handle, self._channel, self._node, value)

    @property
    def frequency_min(self) -> float:
        """Gets the minimum frequency."""
        return api.dwf_analog_out_node_frequency_info(self._device.handle, self._channel, self._node)[0]

    @property
    def frequency_max(self) -> float:
        """Gets the maximum frequency."""
        return api.dwf_analog_out_node_frequency_info(self._device.handle, self._channel, self._node)[1]

    @property
    def frequency(self) -> float:
        """Gets or sets the frequency."""
        return api.dwf_analog_out_node_frequency_get(self._device.handle, self._channel, self._node)

    @frequency.setter
    def frequency(self, value: float) -> None:
        api.dwf_analog_out_node_frequency_set(self._device.handle, self._channel, self._node, value)

    @property
    def amplitude_min(self) -> float:
        """Gets the minimum amplitude."""
        return api.dwf_analog_out_node_amplitude_info(self._device.handle, self._channel, self._node)[0]

    @property
    def amplitude_max(self) -> float:
        """Gets the maximum amplitude."""
        return api.dwf_analog_out_node_amplitude_info(self._device.handle, self._channel, self._node)[1]

    @property
    def amplitude(self) -> float:
        """Gets or sets the amplitude."""
        return api.dwf_analog_out_node_amplitude_get(self._device.handle, self._channel, self._node)

    @amplitude.setter
    def amplitude(self, value: float) -> None:
        api.dwf_analog_out_node_amplitude_set(self._device.handle, self._channel, self._node, value)

    @property
    def offset_min(self) -> float:
        """Gets the minimum offset."""
        return api.dwf_analog_out_node_offset_info(self._device.handle, self._channel, self._node)[0]

    @property
    def offset_max(self) -> float:
        """Gets the maximum offset."""
        return api.dwf_analog_out_node_offset_info(self._device.handle, self._channel, self._node)[1]

    @property
    def offset(self) -> float:
        """Gets or sets the offset."""
        return api.dwf_analog_out_node_offset_get(self._device.handle, self._channel, self._node)

    @offset.setter
    def offset(self, value: float) -> None:
        api.dwf_analog_out_node_offset_set(self._device.handle, self._channel, self._node, value)

    @property
    def symmetry_min(self) -> float:
        """Gets the minimum symmetry percentage."""
        return api.dwf_analog_out_node_symmetry_info(self._device.handle, self._channel, self._node)[0]

    @property
    def symmetry_max(self) -> float:
        """Gets the maximum symmetry percentage."""
        return api.dwf_analog_out_node_symmetry_info(self._device.handle, self._channel, self._node)[1]

    @property
    def symmetry(self) -> float:
        """Gets or sets the symmetry percentage."""
        return api.dwf_analog_out_node_symmetry_get(self._device.handle, self._channel, self._node)

    @symmetry.setter
    def symmetry(self, value: float) -> None:
        api.dwf_analog_out_node_symmetry_set(self._device.handle, self._channel, self._node, value)

    @property
    def phase_min(self) -> float:
        """Gets the minimum phase."""
        return api.dwf_analog_out_node_phase_info(self._device.handle, self._channel, self._node)[0]

    @property
    def phase_max(self) -> float:
        """Gets the maximum phase."""
        return api.dwf_analog_out_node_phase_info(self._device.handle, self._channel, self._node)[1]

    @property
    def phase(self) -> float:
        """Gets or sets the phase."""
        return api.dwf_analog_out_node_phase_get(self._device.handle, self._channel, self._node)

    @phase.setter
    def phase(self, value: float) -> None:
        api.dwf_analog_out_node_phase_set(self._device.handle, self._channel, self._node, value)

    @property
    def data_samples_min(self) -> int:
        """Gets the minimum number of samples allowed for custom data generation."""
        return int(api.dwf_analog_out_node_data_info(self._device.handle, self._channel, self._node)[0])

    @property
    def data_samples_max(self) -> int:
        """Gets the maximum number of samples allowed for custom data generation."""
        return int(api.dwf_analog_out_node_data_info(self._device.handle, self._channel, self._node)[1])

    @property
    def play_status(self) -> Tuple[int, int, int]:
        """Gets information about the recording process.
        Returns (samples_free, lost_samples, corrupted_samples)"""
        return api.dwf_analog_out_node_play_status(self._device.handle, self._channel, self._node)

    def set_data_samples(self, samples: List[float]) -> None:
        """Sets the custom data or to prefill the buffer with play samples."""
        data = (ctypes.c_double * len(samples))(*samples)
        api.dwf_analog_out_node_data_set(self._device.handle, self._channel, self._node, data, len(data))

    def set_play_samples(self, samples) -> None:
        """Sets new data samples for play mode."""
        api.dwf_analog_out_node_play_data(self._device.handle, self._channel, self._node, samples, len(samples))


class AnalogOutputChannel:
    """Represents an Analog Output channel."""

    def __init__(self, module, channel):
        self._device = module.device
        self._module = module
        self._channel = channel
        self._label = "ch" + str(channel + 1)
        self._trigger = AnalogOutputChannelTrigger(self)

        nodes = api.dwf_analog_out_node_info(self._device.handle, self._channel)
        self._nodes = tuple(AnalogOutputChannelNode(self, v) for v in AnalogOutputNode if (nodes & (1 << v.value)) != 0)

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def module(self) -> "AnalogOutput":
        """Gets the Analog Output module."""
        return self._module

    @property
    def index(self) -> int:
        """Gets the channel index."""
        return self._channel

    @property
    def nodes(self) -> Tuple[AnalogOutputChannelNode, ...]:
        """Gets the channel nodes."""
        return self._nodes

    def __getitem__(self, key) -> AnalogOutputChannelNode:
        if isinstance(key, AnalogOutputNode):
            for node in self._nodes:
                if node.type == key:
                    return node

        if isinstance(key, int):
            return self._nodes[key]

        raise IndexError(key)

    @property
    def label(self) -> str:
        """Gets or sets the channel label."""
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @property
    def trigger(self) -> AnalogOutputChannelTrigger:
        """Gets the trigger unit."""
        return self._trigger

    @property
    def master(self) -> int:
        """Gets or sets the master node index."""
        return bool(api.dwf_analog_out_master_get(self._device.handle, self._channel))

    @master.setter
    def master(self, value: int) -> None:
        api.dwf_analog_out_master_set(self._device.handle, self._channel, value)

    @property
    def run_length_min(self) -> float:
        """Gets the minimum run length in seconds."""
        return api.dwf_analog_out_run_info(self._device.handle, self._channel)[0]

    @property
    def run_length_max(self) -> float:
        """Gets the maximum run length in seconds."""
        return api.dwf_analog_out_run_info(self._device.handle, self._channel)[1]

    @property
    def run_length(self) -> float:
        """Gets or sets the run length in seconds."""
        return api.dwf_analog_out_run_get(self._device.handle, self._channel)

    @run_length.setter
    def run_length(self, value: float) -> None:
        api.dwf_analog_out_run_set(self._device.handle, self._channel, value)

    @property
    def run_length_status(self) -> float:
        """Gets the remaining run length in seconds."""
        return api.dwf_analog_out_run_status(self._device.handle, self._channel)

    @property
    def wait_length_min(self) -> float:
        """Gets the minimum wait length in seconds."""
        return api.dwf_analog_out_wait_info(self._device.handle, self._channel)[0]

    @property
    def wait_length_max(self) -> float:
        """Gets the maximum wait length in seconds."""
        return api.dwf_analog_out_wait_info(self._device.handle, self._channel)[1]

    @property
    def wait_length(self) -> float:
        """Gets or sets the wait length in seconds."""
        return api.dwf_analog_out_wait_get(self._device.handle, self._channel)

    @wait_length.setter
    def wait_length(self, value: float) -> None:
        api.dwf_analog_out_wait_set(self._device.handle, self._channel, value)

    @property
    def repeat_count_min(self) -> int:
        """Gets the minimum repeat count."""
        return api.dwf_analog_out_repeat_info(self._device.handle, self._channel)[0]

    @property
    def repeat_count_max(self) -> int:
        """Gets the maximum repeat count."""
        return api.dwf_analog_out_repeat_info(self._device.handle, self._channel)[1]

    @property
    def repeat_count(self) -> int:
        """Gets or sets the repeat count."""
        return api.dwf_analog_out_repeat_get(self._device.handle, self._channel)

    @repeat_count.setter
    def repeat_count(self, value: int) -> None:
        api.dwf_analog_out_repeat_set(self._device.handle, self._channel, value)

    @property
    def repeat_count_status(self) -> float:
        """Gets the remaining repeat count."""
        return api.dwf_analog_out_repeat_status(self._device.handle, self._channel)

    @property
    def enable_repeat_trigger(self) -> bool:
        """Enables the repeat count trigger in wait-run repeat cycles."""
        return bool(api.dwf_analog_out_repeat_trigger_get(self._device.handle, self._channel))

    @enable_repeat_trigger.setter
    def enable_repeat_trigger(self, value: bool) -> None:
        api.dwf_analog_out_repeat_trigger_set(self._device.handle, self._channel, value)

    @property
    def limitation_min(self) -> float:
        """Gets the minimum limitation value."""
        return api.dwf_analog_out_limitation_info(self._device.handle, self._channel)[0]

    @property
    def limitation_max(self) -> float:
        """Gets the maximum limitation value."""
        return api.dwf_analog_out_limitation_info(self._device.handle, self._channel)[1]

    @property
    def limitation(self) -> float:
        """Gets or sets the limitation value.
        Voltage offset in volts or modulation offset percentage."""
        return api.dwf_analog_out_limitation_get(self._device.handle, self._channel)

    @limitation.setter
    def limitation(self, value: float) -> None:
        api.dwf_analog_out_limitation_set(self._device.handle, self._channel, value)

    @property
    def mode(self) -> AnalogOutputMode:
        """Gets or sets the generator mode option."""
        return AnalogOutputMode(api.dwf_analog_out_mode_get(self._device.handle, self._channel))

    @mode.setter
    def mode(self, value: AnalogOutputMode) -> None:
        api.dwf_analog_out_mode_set(self._device.handle, self._channel, value)

    @property
    def idle_info(self) -> Tuple[AnalogOutputIdle, ...]:
        """Gets the supported channel nodes."""
        return Helpers.map_enum_values(
            AnalogOutputIdle, api.dwf_analog_out_idle_info(self._device.handle, self._channel)
        )

    @property
    def idle(self) -> AnalogOutputIdle:
        """Gets or sets the generator idle output option."""
        return AnalogOutputIdle(api.dwf_analog_out_idle_get(self._device.handle, self._channel))

    @idle.setter
    def idle(self, value: AnalogOutputIdle) -> None:
        api.dwf_analog_out_idle_set(self._device.handle, self._channel, value)

    def reset(self) -> None:
        """Resets and configures all instrument parameters to default values."""
        api.dwf_analog_out_reset(self._device.handle, self._channel)

    def configure(self, start: bool = False) -> None:
        """Configures and optionally starts the instrument."""
        api.dwf_analog_out_configure(self._device.handle, self._channel, start)

    def apply(self) -> None:
        """Applies changes to the instrument."""
        api.dwf_analog_out_configure(self._device.handle, self._channel, 3)

    def read_status(self) -> Status:
        """Gets the instrument status."""
        return Status(api.dwf_analog_out_status(self._device.handle, self._channel))

    def setup(
        self,
        function: Optional[str] = None,
        frequency: Optional[float] = None,
        amplitude: Optional[float] = None,
        offset: Optional[float] = None,
        symmetry: Optional[float] = None,
        phase: Optional[float] = None,
        data_samples: Optional[float] = None,
        enabled: bool = True,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Sets up a new carrier waveform.

        Parameters
        ----------
        function : str, optional
            The generator function.
            Can be 'dc', 'sine', 'square', 'triangle', 'ramp-up', 'ramp-down',
            'noise', 'pulse', 'trapezium', 'sine-power', 'custom', 'play', 'custom-pattern', or 'play-pattern'.
        frequency : float, optional
            The waveform frequency in Hz.
        amplitude : float, optional
            The waveform amplitude in Volts.
        offset : float, optional
            The waveform offset in Volts.
        symmetry : float, optional
            The waveform symmetry (or duty cycle) in percent.
        phase : float, optional
            The waveform phase in degree.
        data_samples : float, optional
            The waveform data samples normalized to +/-1.
        enabled : bool, optional
            If True, then the node is enabled (default True).
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the instrument is started (default False).
        """
        self._setup_node(
            AnalogOutputNode.CARRIER,
            function=function,
            frequency=frequency,
            amplitude=amplitude,
            offset=offset,
            symmetry=symmetry,
            phase=phase,
            data_samples=data_samples,
            enabled=enabled,
            configure=configure,
            start=start,
        )

    def setup_am(
        self,
        function: Optional[str] = None,
        frequency: Optional[float] = None,
        amplitude: Optional[float] = None,
        offset: Optional[float] = None,
        symmetry: Optional[float] = None,
        phase: Optional[float] = None,
        data_samples: Optional[float] = None,
        enabled: bool = True,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Applies an AM modulation to a waveform.

        Parameters
        ----------
        function : str, optional
            The generator function.
            Can be 'dc', 'sine', 'square', 'triangle', 'ramp-up',
            'ramp-down', 'noise', 'pulse', 'trapezium', or 'sine-power'.
        frequency : float, optional
            The waveform frequency in Hz.
        amplitude : float, optional
            The waveform amplitude in percent.
        offset : float, optional
            The waveform offset in percent.
        symmetry : float, optional
            The waveform symmetry (or duty cycle) in percent.
        phase : float, optional
            The waveform phase in degree.
        data_samples : float, optional
            The waveform data samples normalized to +/-1.
        enabled : bool, optional
            If True, then the node is enabled (default True).
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the instrument is started (default False).
        """
        self._setup_node(
            AnalogOutputNode.AM,
            function=function,
            frequency=frequency,
            amplitude=amplitude,
            offset=offset,
            symmetry=symmetry,
            phase=phase,
            data_samples=data_samples,
            enabled=enabled,
            configure=configure,
            start=start,
        )

    def setup_fm(
        self,
        function: Optional[str] = None,
        frequency: Optional[float] = None,
        amplitude: Optional[float] = None,
        offset: Optional[float] = None,
        symmetry: Optional[float] = None,
        phase: Optional[float] = None,
        data_samples: Optional[float] = None,
        enabled: bool = True,
        configure: bool = False,
        start: bool = False,
    ) -> None:
        """Applies an FM modulation to a waveform.

        Parameters
        ----------
        function : str, optional
            The generator function.
            Can be 'dc', 'sine', 'square', 'triangle', 'ramp-up',
            'ramp-down', 'noise', 'pulse', 'trapezium', or 'sine-power'.
        frequency : float, optional
            The waveform frequency in Hz.
        amplitude : float, optional
            The waveform amplitude in percent.
        offset : float, optional
            The waveform offset in percent.
        symmetry : float, optional
            The waveform symmetry (or duty cycle) in percent.
        phase : float, optional
            The waveform phase in degree.
        data_samples : float, optional
            The waveform data samples normalized to +/-1.
        enabled : bool, optional
            If True, then the node is enabled (default True).
        configure : bool, optional
            If True, then the instrument is configured (default False).
        start : bool, optional
            If True, then the instrument is started (default False).
        """
        self._setup_node(
            AnalogOutputNode.FM,
            function=function,
            frequency=frequency,
            amplitude=amplitude,
            offset=offset,
            symmetry=symmetry,
            phase=phase,
            data_samples=data_samples,
            enabled=enabled,
            configure=configure,
            start=start,
        )

    def _setup_node(
        self,
        node_type,
        function,
        frequency,
        amplitude,
        offset,
        symmetry,
        phase,
        data_samples,
        enabled,
        configure,
        start,
    ) -> None:
        node = self.nodes[node_type]
        if function is not None:
            node.function = Helpers.map_function(function)
        if frequency is not None:
            node.frequency = frequency
        if amplitude is not None:
            node.amplitude = amplitude
        if offset is not None:
            node.offset = offset
        if symmetry is not None:
            node.symmetry = symmetry
        if phase is not None:
            node.phase = phase
        if phase is not None:
            node.phase = phase
        if data_samples is not None:
            node.set_data_samples(data_samples)
        if enabled is not None:
            node.enabled = enabled
        if configure or start:
            self.configure(start=start)


class AnalogOutput:
    """Analog Output module (Arbitrary Waveform Generator)."""

    def __init__(self, device):
        self._device = device
        self._channels = tuple(
            AnalogOutputChannel(self, i) for i in range(api.dwf_analog_out_count(self._device.handle))
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        del exception_type, exception_value, traceback
        for channel in self._channels:
            channel.reset()

    @property
    def device(self) -> "fwd.Device":
        """Gets the device."""
        return self._device

    @property
    def channels(self) -> Tuple[AnalogOutputChannel, ...]:
        """Gets a collection of Analog Output channels."""
        return self._channels

    def __getitem__(self, key) -> AnalogOutputChannel:
        if isinstance(key, int):
            return self._channels[key]

        if isinstance(key, str):
            for channel in self._channels:
                if channel.label == key:
                    return channel

        raise IndexError(key)
