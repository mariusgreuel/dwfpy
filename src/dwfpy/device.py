"""
Support for Digilent WaveForms devices.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

import logging
from typing import Optional, Tuple, Union
from . import bindings as api
from .constants import DeviceId, DeviceType, GlobalParameter, TriggerSlope, TriggerSource
from .exceptions import WaveformsError, DeviceNotFound, DeviceNotOpenError, FeatureNotSupportedError
from .helpers import Helpers
from .application import Application
from .configuration import Configuration
from .device_info import DeviceInfo
from .analog_io import AnalogIo
from .analog_input import AnalogInput
from .analog_output import AnalogOutput
from .digital_io import DigitalIo
from .digital_input import DigitalInput
from .digital_output import DigitalOutput
from .protocols import Protocols


class DeviceBase:
    """Base class for Digilent WaveForms devices."""

    class _EnumeratedIndex:
        def __init__(self, index):
            self.index = index

    def __init__(
        self,
        configuration: Optional[Union[int, str]] = None,
        serial_number: Optional[str] = None,
        device_id: Optional[int] = None,
        device_type: Optional[int] = None,
        device_index: Optional[Union[int, _EnumeratedIndex]] = None,
    ):
        """
        :param configuration: Select the active configuration.
        :param serial_number: Filter devices by serial number.
        :param device_id: Filter devices by device ID.
        :param device_type: Filter devices by device type.
        :param device_index: Filter devices by device index.
        """
        super().__init__()

        self._application = Application()
        self._logger = Application.get_logger()
        self._device_info = DeviceInfo()
        self._analog_io = None
        self._analog_input = None
        self._analog_output = None
        self._digital_io = None
        self._digital_input = None
        self._digital_output = None
        self._protocols = None

        self._hdwf = None
        self._auto_reset = True

        self._configuration = configuration
        self._enum_serial_number = DeviceInfo.normalize_serial_number(serial_number) if serial_number else None
        self._enum_device_id = device_id
        self._enum_device_type = device_type
        self._enum_device_index = device_index

        if isinstance(device_index, self._EnumeratedIndex):
            self._device_info.get_properties(device_index.index)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        del exception_type, exception_value, traceback
        self.close()

    @property
    def application(self) -> Application:
        """Gets the WaveForms application."""
        return self._application

    @property
    def analog_io(self) -> AnalogIo:
        """Gets the Analog IO module."""
        return self._ensure_module(self._analog_io, "Analog IO")

    @property
    def analog_input(self) -> AnalogInput:
        """Gets the Analog Input module (Oscilloscope)."""
        return self._ensure_module(self._analog_input, "Analog Input")

    @property
    def analog_output(self) -> AnalogOutput:
        """Gets the Analog Output module (Arbitrary Waveform Generator)."""
        return self._ensure_module(self._analog_output, "Analog Output")

    @property
    def digital_io(self) -> DigitalIo:
        """Gets the Digital IO module."""
        return self._ensure_module(self._digital_io, "Digital IO")

    @property
    def digital_input(self) -> DigitalInput:
        """Gets the Digital Input module (Logic Analyzer)."""
        return self._ensure_module(self._digital_input, "Digital Input")

    @property
    def digital_output(self) -> DigitalOutput:
        """Gets the Digital Output module (Pattern Generator)."""
        return self._ensure_module(self._digital_output, "Digital Output")

    @property
    def protocols(self) -> Protocols:
        """Gets the Digital Protocols module."""
        return self._ensure_module(self._protocols, "Digital Protocols")

    @property
    def handle(self) -> object:
        """Gets a handle to the device."""
        return self._hdwf

    @property
    def is_open(self) -> bool:
        """Returns true if the device has been opened."""
        return self._hdwf is not None or self._device_info.is_open

    @property
    # pylint: disable-next=invalid-name
    def id(self) -> DeviceId:
        """Gets the device ID."""
        self._ensure_device_info()
        return DeviceId(self._device_info.id)

    @property
    def revision(self) -> str:
        """Gets the device revision."""
        self._ensure_device_info()
        return chr(0x40 + (self._device_info.revision & 0xF))

    @property
    def name(self) -> str:
        """Gets the device name."""
        self._ensure_device_info()
        return self._device_info.name

    @property
    def user_name(self) -> str:
        """Gets the user-defined device name."""
        self._ensure_device_info()
        return self._device_info.user_name

    @property
    def serial_number(self) -> str:
        """Gets the 12-digit, unique device serial number."""
        self._ensure_device_info()
        return self._device_info.serial_number

    @property
    def configurations(self) -> Tuple[Configuration, ...]:
        """Returns a list of device configurations."""
        self._ensure_device_info()
        return self._device_info.configurations

    @property
    def configuration(self) -> Optional[Union[int, str]]:
        """Gets the selected configuration index."""
        return self._configuration

    @property
    def auto_configure(self) -> int:
        """Gets or sets a value indicating to automatically configure
        the device when parameters are changed."""
        self._ensure_handle()
        return api.dwf_device_auto_configure_get(self._hdwf)

    @auto_configure.setter
    def auto_configure(self, value: int) -> None:
        self._ensure_handle()
        api.dwf_device_auto_configure_set(self._hdwf, value)

    @property
    def auto_reset(self) -> bool:
        """Gets or sets a value indicating to reset the device automatically on exit."""
        return self._auto_reset

    @auto_reset.setter
    def auto_reset(self, value: bool) -> None:
        self._auto_reset = value

    @property
    def trigger_info(self) -> Tuple[TriggerSource, ...]:
        """Gets the supported trigger source options for the global trigger bus."""
        self._ensure_handle()
        return Helpers.map_enum_values(TriggerSource, api.dwf_device_trigger_info(self._hdwf))

    @property
    def trigger_slope_info(self) -> Tuple[TriggerSlope, ...]:
        """Gets the supported trigger slopes."""
        self._ensure_handle()
        return Helpers.map_enum_values(TriggerSlope, api.dwf_device_trigger_slope_info(self._hdwf))

    def open(self) -> None:
        """Opens the device."""
        if self._hdwf is not None:
            raise WaveformsError("Device is already open")

        device_index = self._enum_get_device_index()
        if device_index is None:
            devices = api.dwf_enum(api.ENUMFILTER_ALL)
            if devices > 0:
                raise DeviceNotFound(f"No devices match the filter {self._friendly_filter_spec()}")

            raise DeviceNotFound("Device not found")

        if not self._device_info.has_properties:
            self._device_info.get_properties(device_index)

        if self._device_info.is_open:
            raise WaveformsError("Device is already in use by another application")

        if self._configuration is None:
            self._hdwf = api.dwf_device_open(device_index)
        else:
            configuration = self._get_configuration()
            self._logger.info("Using configuration %s", configuration)
            self._hdwf = api.dwf_device_config_open(device_index, configuration)

        if self._hdwf is None:
            raise WaveformsError("Failed to open device")

        if api.dwf_analog_io_channel_count(self._hdwf) > 0:
            self._analog_io = AnalogIo(self)

        if api.dwf_analog_in_channel_count(self._hdwf) > 0:
            self._analog_input = AnalogInput(self)

        if api.dwf_analog_out_count(self._hdwf) > 0:
            self._analog_output = AnalogOutput(self)

        if api.dwf_digital_in_bits_info(self._hdwf) > 0:
            self._digital_io = DigitalIo(self)

        if api.dwf_digital_in_bits_info(self._hdwf) > 0:
            self._digital_input = DigitalInput(self)

        if api.dwf_digital_out_count(self._hdwf) > 0:
            self._digital_output = DigitalOutput(self)

        self._protocols = Protocols(self)

    def close(self) -> None:
        """Closes the device."""
        if self._hdwf is not None:
            if self._auto_reset:
                self.reset()

            api.dwf_device_close(self._hdwf)
            self._hdwf = None

            self._analog_io = None
            self._analog_input = None
            self._analog_output = None
            self._digital_io = None
            self._digital_input = None
            self._digital_output = None
            self._protocols = None

    def reset(self) -> None:
        """Resets and configures all device and instrument parameters to default values."""
        self._ensure_handle()
        api.dwf_device_reset(self._hdwf)

    def get_trigger(self, pin: int) -> TriggerSource:
        """Gets the configured trigger setting for a trigger I/O pin."""
        return TriggerSource(api.dwf_device_trigger_get(self._hdwf, pin))

    def set_trigger(self, pin: int, trigger_source: TriggerSource) -> None:
        """Sets the trigger I/O pin with a specific TriggerSource option."""
        api.dwf_device_trigger_set(self._hdwf, pin, trigger_source)

    def trigger_pc(self) -> None:
        """Generates one pulse on the PC trigger line."""
        api.dwf_device_trigger_pc(self._hdwf)

    def get_parameter(self, parameter: GlobalParameter) -> int:
        """Gets a device parameter."""
        return api.dwf_device_param_get(self._hdwf, parameter)

    def set_parameter(self, parameter: GlobalParameter, value: int) -> None:
        """Sets a device parameter."""
        api.dwf_device_param_set(self._hdwf, parameter, value)

    def _enum_get_device_index(self) -> Optional[int]:
        if self._enum_device_type:
            enumfilter = api.ENUMFILTER_TYPE | self._enum_device_type
        elif self._enum_device_id:
            enumfilter = self._enum_device_id
        else:
            enumfilter = api.ENUMFILTER_ALL

        self._logger.info("Enumerating devices...")
        device_count = api.dwf_enum(enumfilter)
        self._logger.info("Found %s device(s)", device_count)

        if self._logger.isEnabledFor(logging.INFO):
            for i in range(device_count):
                info = DeviceInfo(i)
                self._logger.info("> Device %s: %s (%s)", i + 1, info.name, info.serial_number)

        device_index = self._filter_devices(device_count, skip_open_devices=True)
        if device_index is not None:
            return device_index

        return self._filter_devices(device_count, skip_open_devices=False)

    def _filter_devices(self, device_count, skip_open_devices=False) -> Optional[int]:
        for device_index in range(device_count):
            if skip_open_devices and api.dwf_enum_device_is_opened(device_index):
                continue

            if self._device_info.serial_number:
                if DeviceInfo.get_serial_number(device_index) == self._device_info.serial_number:
                    return device_index
            elif self._enum_serial_number:
                if DeviceInfo.get_serial_number(device_index) == self._enum_serial_number:
                    return device_index
            elif self._enum_device_type and self._enum_device_id:
                device_id, _ = api.dwf_enum_device_type(device_index)
                if abs(device_id) == self._enum_device_id:
                    return device_index
            elif self._enum_device_index:
                if device_index == self._enum_device_index:
                    return device_index
            else:
                return device_index

        return None

    def _friendly_filter_spec(self):
        spec = []
        if self._enum_serial_number:
            spec.append(f"Serial Number: {self._enum_serial_number}")
        if self._enum_device_id:
            spec.append(f"Device ID: {self._friendly_device_id(self._enum_device_id)}")
        if self._enum_device_type:
            spec.append(f"Device type: {self._friendly_device_type(self._enum_device_type)}")
        if self._enum_device_index:
            spec.append(f"Device index: {self._enum_device_index}")
        return spec

    def _friendly_device_id(self, device_id: int):
        if device_id == DeviceId.ANALOG_DISCOVERY:
            return "Analog Discovery"
        elif device_id == DeviceId.ANALOG_DISCOVERY2:
            return "Analog Discovery 2"
        elif device_id == DeviceId.ANALOG_DISCOVERY3:
            return "Analog Discovery 3"
        elif device_id == DeviceId.DIGITAL_DISCOVERY:
            return "Digital Discovery"
        else:
            return str(device_id)

    def _friendly_device_type(self, device_type: int):
        types = []
        if device_type & DeviceType.USB:
            types.append("USB")
        if device_type & DeviceType.NETWORK:
            types.append("NETWORK")
        if device_type & DeviceType.AXI:
            types.append("AXI")
        if device_type & DeviceType.REMOTE:
            types.append("REMOTE")
        if device_type & DeviceType.SOUND_CARD:
            types.append("SOUND_CARD")
        if device_type & DeviceType.DEMO:
            types.append("DEMO")
        if len(types) > 0:
            return "|".join(types)
        else:
            return str(device_type)

    def _ensure_handle(self) -> None:
        if self._hdwf is None:
            raise DeviceNotOpenError("Device is not open")

    def _ensure_device_info(self) -> None:
        if not self._device_info.has_properties:
            device_index = self._enum_get_device_index()
            if device_index is not None:
                self._device_info.get_properties(device_index)

    def _ensure_module(self, module, description):
        if module is None and self._hdwf is not None:
            raise FeatureNotSupportedError(f"The device does have a '{description}' module")

        return module

    def _get_configuration(self):
        if isinstance(self._configuration, str):
            if self._configuration == "generic":
                return 0
            elif self._configuration == "scope":
                if self.id in (
                    DeviceId.ANALOG_DISCOVERY,
                    DeviceId.ANALOG_DISCOVERY2,
                    DeviceId.ANALOG_DISCOVERY3,
                ):
                    return 1
            elif self._configuration == "wavegen":
                if self.id in (
                    DeviceId.ANALOG_DISCOVERY,
                    DeviceId.ANALOG_DISCOVERY2,
                    DeviceId.ANALOG_DISCOVERY3,
                ):
                    return 2
            elif self._configuration == "logic":
                if self.id in (
                    DeviceId.ANALOG_DISCOVERY,
                    DeviceId.ANALOG_DISCOVERY2,
                    DeviceId.ANALOG_DISCOVERY3,
                ):
                    return 3
                elif self.id == DeviceId.DIGITAL_DISCOVERY:
                    return 0
            elif self._configuration == "pattern":
                if self.id in (DeviceId.ANALOG_DISCOVERY, DeviceId.ANALOG_DISCOVERY2):
                    return 3
                elif self.id == DeviceId.ANALOG_DISCOVERY3:
                    return 4
                elif self.id == DeviceId.DIGITAL_DISCOVERY:
                    return 0
            elif self._configuration == "1v8":
                if self.id in (DeviceId.ANALOG_DISCOVERY, DeviceId.ANALOG_DISCOVERY2):
                    return 4
            elif self._configuration == "logic-1v8":
                if self.id == DeviceId.ANALOG_DISCOVERY2:
                    return 6
                elif self.id == DeviceId.DIGITAL_DISCOVERY:
                    return 0
            else:
                raise WaveformsError(
                    "Invalid configuration: "
                    "Must be 'generic', 'scope', 'wavegen', 'logic', 'pattern', '1v8', or 'logic-1v8'."
                )

            raise WaveformsError(
                f"The device '{self._device_info.name}' does not support " "the configuration '{self._configuration}'."
            )

        return self._configuration


class ElectronicsExplorer(DeviceBase):
    """Digilent Electronics Explorer device."""

    class Supplies:
        """The power supplies."""

        class Fixed:
            """The fixed power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables or disables the fixed power supply."""
                return bool(self._device.analog_io[0][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[0][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the fixed power supply."""
                return self._device.analog_io[0][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[0][1].value = value

            @property
            def current(self) -> float:
                """Gets the current of the fixed power supply."""
                return self._device.analog_io[0][2].status

            def setup(self, voltage: float, enabled: bool = True) -> None:
                """Sets up the power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage.
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if enabled is not None:
                    self.enabled = enabled

        class Positive:
            """The positive power supply."""

            def __init__(self, device) -> None:
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables or disables the positive power supply."""
                return bool(self._device.analog_io[1][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[1][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the positive power supply."""
                return self._device.analog_io[1][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[1][1].value = value

            @property
            def current(self) -> float:
                """Gets the current of the positive power supply."""
                return self._device.analog_io[1][2].status

            @property
            def current_limit(self) -> float:
                """Gets or sets the current limit of the positive power supply."""
                return self._device.analog_io[1][2].value

            @current_limit.setter
            def current_limit(self, value: bool) -> None:
                self._device.analog_io[1][2].value = value

            def setup(self, voltage: float, current_limit: Optional[float] = None, enabled: bool = True) -> None:
                """Sets up the positive power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage.
                current_limit : float, optional
                    The power supply current limit in A.
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if current_limit is not None:
                    self.current_limit = current_limit
                if enabled is not None:
                    self.enabled = enabled

        class Negative:
            """The negative power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables the negative power supply."""
                return bool(self._device.analog_io[2][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[2][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the negative power supply."""
                return self._device.analog_io[2][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[2][1].value = value

            @property
            def current(self) -> float:
                """Gets the current of the negative power supply."""
                return self._device.analog_io[2][2].status

            @property
            def current_limit(self) -> float:
                """Gets or sets the current limit of the negative power supply."""
                return self._device.analog_io[2][2].value

            @current_limit.setter
            def current_limit(self, value: bool) -> None:
                self._device.analog_io[2][2].value = value

            def setup(self, voltage: float, current_limit: Optional[float] = None, enabled: bool = True) -> None:
                """Sets up the negative power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage (must be a negative value).
                current_limit : float, optional
                    The power supply current limit in A.
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if current_limit is not None:
                    self.current_limit = current_limit
                if enabled is not None:
                    self.enabled = enabled

        class Reference1:
            """The voltage reference 1."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables the voltage reference 1."""
                return bool(self._device.analog_io[3][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[3][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the voltage reference 1."""
                return self._device.analog_io[3][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[3][1].value = value

            def setup(self, voltage: float, enabled: bool = True) -> None:
                """Sets up the voltage reference.

                Parameters
                ----------
                voltage : float
                    The output voltage.
                enabled : bool, optional
                    If True, then the voltage reference is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if enabled is not None:
                    self.enabled = enabled

        class Reference2:
            """The voltage reference 2."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables the voltage reference 2."""
                return bool(self._device.analog_io[4][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[4][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the voltage reference 2."""
                return self._device.analog_io[4][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[4][1].value = value

            def setup(self, voltage: float, enabled: bool = True) -> None:
                """Sets up the voltage reference.

                Parameters
                ----------
                voltage : float
                    The output voltage.
                enabled : bool, optional
                    If True, then the voltage reference is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if enabled is not None:
                    self.enabled = enabled

        def __init__(self, device):
            self._device = device
            self._fixed = self.Fixed(device)
            self._positive = self.Positive(device)
            self._negative = self.Negative(device)
            self._reference1 = self.Reference1(device)
            self._reference2 = self.Reference2(device)

        @property
        def fixed(self) -> Fixed:
            """Gets the fixed power supply."""
            return self._fixed

        @property
        def positive(self) -> Positive:
            """Gets the positive power supply."""
            return self._positive

        @property
        def negative(self) -> Negative:
            """Gets the negative power supply."""
            return self._negative

        @property
        def reference1(self) -> Reference1:
            """Gets the voltage reference 1."""
            return self._reference1

        @property
        def reference2(self) -> Reference2:
            """Gets the voltage reference 2."""
            return self._reference2

        @property
        def master_enable(self) -> bool:
            """Gets or sets the master enable switch."""
            return self._device.analog_io.master_enable

        @master_enable.setter
        def master_enable(self, value: bool) -> None:
            self._device.analog_io.master_enable = value

        @property
        def master_enable_status(self) -> bool:
            """Gets the master enable status."""
            return self._device.analog_io.master_enable_status

    class Voltmeters:
        """The devices voltmeters."""

        def __init__(self, device):
            self._device = device

        @property
        def voltmeter1(self) -> float:
            """Reads the voltage of voltmeter 1."""
            return self._device.analog_io[5][0].status

        @property
        def voltmeter2(self) -> float:
            """Reads the voltage of voltmeter 2."""
            return self._device.analog_io[6][0].status

        @property
        def voltmeter3(self) -> float:
            """Reads the voltage of voltmeter 3."""
            return self._device.analog_io[7][0].status

        @property
        def voltmeter4(self) -> float:
            """Reads the voltage of voltmeter 4."""
            return self._device.analog_io[8][0].status

    def __init__(self, configuration=None, serial_number=None, device_type=None, device_index=None):
        super().__init__(
            configuration=configuration,
            serial_number=serial_number,
            device_id=DeviceId.ELECTRONICS_EXPLORER,
            device_type=device_type,
            device_index=device_index,
        )
        self._supplies = self.Supplies(self)
        self._voltmeters = self.Voltmeters(self)

    @property
    def supplies(self) -> Supplies:
        """Gets the power supplies."""
        return self._supplies

    @property
    def voltmeters(self) -> Voltmeters:
        """Gets the voltmeters."""
        return self._voltmeters


class AnalogDiscovery(DeviceBase):
    """Digilent Analog Discovery device."""

    class Supplies:
        """The power supplies."""

        class Positive:
            """The positive power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables or disables the positive power supply."""
                return bool(self._device.analog_io[0][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[0][0].value = value

            def setup(self, enabled: bool = True) -> None:
                """Sets up the positive power supply.

                Parameters
                ----------
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if enabled is not None:
                    self.enabled = enabled

        class Negative:
            """The negative power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables the negative power supply."""
                return bool(self._device.analog_io[1][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[1][0].value = value

            def setup(self, enabled: bool = True) -> None:
                """Sets up the negative power supply.

                Parameters
                ----------
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if enabled is not None:
                    self.enabled = enabled

        def __init__(self, device):
            self._device = device
            self._positive = self.Positive(device)
            self._negative = self.Negative(device)

        @property
        def positive(self) -> Positive:
            """Gets the positive power supply."""
            return self._positive

        @property
        def negative(self) -> Negative:
            """Gets the negative power supply."""
            return self._negative

        @property
        def master_enable(self) -> bool:
            """Gets or sets the master enable switch."""
            return self._device.analog_io.master_enable

        @master_enable.setter
        def master_enable(self, value: bool) -> None:
            self._device.analog_io.master_enable = value

        @property
        def master_enable_status(self) -> bool:
            """Gets the master enable status."""
            return self._device.analog_io.master_enable_status

        @property
        def regulator_voltage(self) -> float:
            """Gets the voltage input for the supply regulators."""
            return self._device.analog_io[3][0].status

        @property
        def regulator_current(self) -> float:
            """Gets the current taken by the supply regulators."""
            return self._device.analog_io[3][1].status

    def __init__(self, configuration=None, serial_number=None, device_type=None, device_index=None):
        super().__init__(
            configuration=configuration,
            serial_number=serial_number,
            device_id=DeviceId.ANALOG_DISCOVERY,
            device_type=device_type,
            device_index=device_index,
        )
        self._supplies = self.Supplies(self)

    @property
    def supplies(self) -> Supplies:
        """Gets the power supplies."""
        return self._supplies

    @property
    def usb_voltage(self) -> float:
        """Gets the USB voltage."""
        return self.analog_io[2][0].status

    @property
    def usb_current(self) -> float:
        """Gets the USB current."""
        return self.analog_io[2][1].status

    @property
    def temperature(self) -> float:
        """Gets the temperature of the device."""
        return self.analog_io[2][2].status


class AnalogDiscovery2(DeviceBase):
    """Digilent Analog Discovery 2 device."""

    class Supplies:
        """The power supplies."""

        class Positive:
            """The positive power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables or disables the positive power supply."""
                return bool(self._device.analog_io[0][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[0][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the positive power supply."""
                return self._device.analog_io[0][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[0][1].value = value

            def setup(self, voltage: float, enabled: bool = True) -> None:
                """Sets up the positive power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage.
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if enabled is not None:
                    self.enabled = enabled

        class Negative:
            """The negative power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables the negative power supply."""
                return bool(self._device.analog_io[1][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[1][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the negative power supply."""
                return self._device.analog_io[1][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[1][1].value = value

            def setup(self, voltage: float, enabled: bool = True) -> None:
                """Sets up the negative power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage (must be a negative value).
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if enabled is not None:
                    self.enabled = enabled

        def __init__(self, device):
            self._device = device
            self._positive = self.Positive(device)
            self._negative = self.Negative(device)

        @property
        def positive(self) -> Positive:
            """Gets the positive power supply."""
            return self._positive

        @property
        def negative(self) -> Negative:
            """Gets the negative power supply."""
            return self._negative

        @property
        def master_enable(self) -> bool:
            """Gets or sets the master enable switch."""
            return self._device.analog_io.master_enable

        @master_enable.setter
        def master_enable(self, value: bool) -> None:
            self._device.analog_io.master_enable = value

        @property
        def master_enable_status(self) -> bool:
            """Gets the master enable status."""
            return self._device.analog_io.master_enable_status

    def __init__(self, configuration=None, serial_number=None, device_type=None, device_index=None):
        super().__init__(
            configuration=configuration,
            serial_number=serial_number,
            device_id=DeviceId.ANALOG_DISCOVERY2,
            device_type=device_type,
            device_index=device_index,
        )
        self._supplies = self.Supplies(self)

    @property
    def supplies(self) -> Supplies:
        """Gets the power supplies."""
        return self._supplies

    @property
    def usb_voltage(self) -> float:
        """Gets the USB voltage."""
        return self.analog_io[2][0].status

    @property
    def usb_current(self) -> float:
        """Gets the USB current."""
        return self.analog_io[2][1].status

    @property
    def temperature(self) -> float:
        """Gets the temperature of the device."""
        return self.analog_io[2][2].status

    @property
    def aux_voltage(self) -> float:
        """Gets the AUX line voltage."""
        return self.analog_io[3][0].status

    @property
    def aux_current(self) -> float:
        """Gets the AUX line current."""
        return self.analog_io[3][1].status


class AnalogDiscovery3(DeviceBase):
    """Digilent Analog Discovery 3 device."""

    class Supplies:
        """The power supplies."""

        class Positive:
            """The positive power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables or disables the positive power supply."""
                return bool(self._device.analog_io[0][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[0][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the positive power supply."""
                return self._device.analog_io[0][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[0][1].value = value

            def setup(self, voltage: float, enabled: bool = True) -> None:
                """Sets up the positive power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage.
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if enabled is not None:
                    self.enabled = enabled

        class Negative:
            """The negative power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def enabled(self) -> bool:
                """Enables the negative power supply."""
                return bool(self._device.analog_io[1][0].value)

            @enabled.setter
            def enabled(self, value: bool) -> None:
                self._device.analog_io[1][0].value = value

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the negative power supply."""
                return self._device.analog_io[1][1].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[1][1].value = value

            def setup(self, voltage: float, enabled: bool = True) -> None:
                """Sets up the negative power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage (must be a negative value).
                enabled : bool, optional
                    If True, then the power supply is enabled (default True).
                """
                if voltage is not None:
                    self.voltage = voltage
                if enabled is not None:
                    self.enabled = enabled

        def __init__(self, device):
            self._device = device
            self._positive = self.Positive(device)
            self._negative = self.Negative(device)

        @property
        def positive(self) -> Positive:
            """Gets the positive power supply."""
            return self._positive

        @property
        def negative(self) -> Negative:
            """Gets the negative power supply."""
            return self._negative

        @property
        def master_enable(self) -> bool:
            """Gets or sets the master enable switch."""
            return self._device.analog_io.master_enable

        @master_enable.setter
        def master_enable(self, value: bool) -> None:
            self._device.analog_io.master_enable = value

        @property
        def master_enable_status(self) -> bool:
            """Gets the master enable status."""
            return self._device.analog_io.master_enable_status

    def __init__(self, configuration=None, serial_number=None, device_type=None, device_index=None):
        super().__init__(
            configuration=configuration,
            serial_number=serial_number,
            device_id=DeviceId.ANALOG_DISCOVERY3,
            device_type=device_type,
            device_index=device_index,
        )
        self._supplies = self.Supplies(self)

    @property
    def supplies(self) -> Supplies:
        """Gets the power supplies."""
        return self._supplies

    @property
    def pcb_temperature(self) -> float:
        """Gets the temperature of the PCB."""
        return self.analog_io[2][0].status

    @property
    def fpga_temperature(self) -> float:
        """Gets the temperature of the FPGA."""
        return self.analog_io[2][1].status

    @property
    def usb_voltage(self) -> float:
        """Gets the USB voltage."""
        return self.analog_io[2][2].status

    @property
    def usb_current(self) -> float:
        """Gets the USB current."""
        return self.analog_io[2][3].status

    @property
    def aux_voltage(self) -> float:
        """Gets the AUX line voltage."""
        return self.analog_io[3][4].status

    @property
    def aux_current(self) -> float:
        """Gets the AUX line current."""
        return self.analog_io[3][5].status

    @property
    def usb_cc1_voltage(self) -> float:
        """Gets the USB CC1 voltage."""
        return self.analog_io[2][6].status

    @property
    def usb_cc2_voltage(self) -> float:
        """Gets the USB CC2 voltage."""
        return self.analog_io[2][7].status


class DigitalDiscovery(DeviceBase):
    """Digilent Digital Discovery device."""

    class Supplies:
        """The power supplies."""

        class Digital:
            """The digital power supply."""

            def __init__(self, device):
                self._device = device

            @property
            def voltage(self) -> float:
                """Gets or sets the voltage of the digital power supply."""
                return self._device.analog_io[0][0].value

            @voltage.setter
            def voltage(self, value: float) -> None:
                self._device.analog_io[0][0].value = value

            def setup(self, voltage: float) -> None:
                """Sets up the power supply.

                Parameters
                ----------
                voltage : float
                    The output voltage.
                """
                if voltage is not None:
                    self.voltage = voltage

        def __init__(self, device):
            self._device = device
            self._digital = self.Digital(device)

        @property
        def digital(self) -> Digital:
            """Gets the digital power supply."""
            return self._digital

        @property
        def master_enable(self) -> bool:
            """Gets or sets the master enable switch."""
            return self._device.analog_io.master_enable

        @master_enable.setter
        def master_enable(self, value: bool) -> None:
            self._device.analog_io.master_enable = value

        @property
        def master_enable_status(self) -> bool:
            """Gets the master enable status."""
            return self._device.analog_io.master_enable_status

    def __init__(self, configuration=None, serial_number=None, device_type=None, device_index=None):
        super().__init__(
            configuration=configuration,
            serial_number=serial_number,
            device_id=DeviceId.DIGITAL_DISCOVERY,
            device_type=device_type,
            device_index=device_index,
        )
        self._supplies = self.Supplies(self)

    @property
    def supplies(self) -> Supplies:
        """Gets the power supplies."""
        return self._supplies

    @property
    def din_pull_up_down(self) -> float:
        """Gets or sets the weak pull for DIN lines.
        Can be 0.0=low, 0.5=middle, 1.0=high
        """
        return self.analog_io[0][1].value

    @din_pull_up_down.setter
    def din_pull_up_down(self, value: float) -> None:
        self.analog_io[0][1].value = value

    @property
    def dio_pull_enable(self) -> int:
        """Gets or sets the pull enable for DIO 39-24 as bit-field set."""
        return int(self.analog_io[0][2].value)

    @dio_pull_enable.setter
    def dio_pull_enable(self, value: int) -> None:
        self.analog_io[0][2].value = value

    @property
    def dio_pull_up_down(self) -> int:
        """Gets or sets the pull up/down for DIO 39-24 as bit-field set."""
        return int(self.analog_io[0][3].value)

    @dio_pull_up_down.setter
    def dio_pull_up_down(self, value: int) -> None:
        self.analog_io[0][3].value = value

    @property
    def dio_drive_strength(self) -> float:
        """Gets or sets the drive strength for DIO lines.
        Can be 0 (auto based on digital voltage), 2, 4, 6, 8, 12, or 16mA
        """
        return self.analog_io[0][4].value

    @dio_drive_strength.setter
    def dio_drive_strength(self, value: float) -> None:
        self.analog_io[0][4].value = value

    @property
    def dio_slew(self) -> int:
        """Gets or sets the slew rate for DIO lines.
        0=QuietIO, 1=Slow, 2=Fast"""
        return int(self.analog_io[0][5].value)

    @dio_slew.setter
    def dio_slew(self, value: int) -> None:
        self.analog_io[0][5].value = value

    @property
    def digital_frequency(self) -> float:
        """Gets or sets the frequency for DIO lines."""
        return self.analog_io[0][6].value

    @digital_frequency.setter
    def digital_frequency(self, value: float) -> None:
        self.analog_io[0][6].value = value

    @property
    def vio_voltage(self) -> float:
        """Gets the VIO voltage reading."""
        return self.analog_io[1][0].status

    @property
    def vio_current(self) -> float:
        """Gets the VIO current reading."""
        return self.analog_io[1][1].status

    @property
    def usb_voltage(self) -> float:
        """Gets the USB voltage."""
        return self.analog_io[2][0].status

    @property
    def usb_current(self) -> float:
        """Gets the USB current."""
        return self.analog_io[2][1].status


class Device(DeviceBase):
    """Generic Digilent WaveForms device."""

    @staticmethod
    def enumerate(enum_filter=api.ENUMFILTER_ALL) -> tuple:
        """Enumerates all devices."""
        return tuple(Device(device_index=Device._EnumeratedIndex(i)) for i in range(api.dwf_enum(enum_filter)))

    @staticmethod
    def close_all() -> None:
        """Closes all opened devices by the calling process."""
        api.dwf_device_close_all()
