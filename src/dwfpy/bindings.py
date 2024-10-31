"""
Python bindings for Digilent WaveForms API.
"""

#
# This file is part of dwfpy: https://github.com/mariusgreuel/dwfpy
# Copyright (C) 2019 Marius Greuel
#
# SPDX-License-Identifier: MIT
#

from ctypes import (
    cdll,
    CFUNCTYPE,
    POINTER,
    c_char,
    c_ubyte,
    c_short,
    c_ushort,
    c_int,
    c_uint,
    c_ulonglong,
    c_double,
    c_void_p,
    c_char_p,
    create_string_buffer,
)
import logging
import sys

_logger = logging.getLogger('dwfpy')


def _load_dwf_library():
    try:
        if sys.platform.startswith('win'):
            path = 'dwf'
        elif sys.platform.startswith('darwin'):
            path = '/Library/Frameworks/dwf.framework/dwf'
        else:
            path = 'libdwf.so'
        _logger.info('Loading library: %s', path)
        return cdll.LoadLibrary(path)
    except OSError as ex:
        _logger.error(
            'Failed to load Digilent WaveForms runtime components.'
            ' You may need to reinstall the WaveForms software: %s',
            ex,
        )
        return FileNotFoundError(f'Failed to load Digilent WaveForms runtime components: {ex}')


_dwf_library = _load_dwf_library()


def _get_dwf_version():
    if isinstance(_dwf_library, Exception):
        return '0.0.0'

    try:
        buffer = create_string_buffer(32)
        _dwf_library.FDwfGetVersion(buffer)
        return buffer.value.decode('ascii')
    except AttributeError as ex:
        raise AttributeError(f'Failed to get Digilent WaveForms version: {ex}') from None


_version_string = _get_dwf_version()
_logger.info('DWF version: %s', _version_string)
_version = tuple(map(int, _version_string.split('.')))


def _default_error_handler(result, _, args):
    if not result:
        raise SystemError()

    return args


_error_handler = _default_error_handler


def set_error_handler(handler):
    """Set the error handle for checking the return code of the DWF API."""
    # pylint: disable-next=invalid-name
    # pylint: disable-next=global-statement
    global _error_handler
    _error_handler = handler


def _dwf_library_error_handler(*_):
    raise _dwf_library


def _dwf_function(name, *args):
    def errcheck(result, func, args):
        _logger.debug('%s%s=%s', function.name, args, result)
        return args if _error_handler is None else _error_handler(result, func, args)

    if isinstance(_dwf_library, Exception):
        return _dwf_library_error_handler

    argtypes = (arg[1] for arg in args)
    paramflags = tuple((arg[0], arg[2]) for arg in args)
    prototype = CFUNCTYPE(c_int, *argtypes)
    function = prototype((name, _dwf_library), paramflags)
    function.name = name
    function.errcheck = errcheck
    return function


_IN = 1
_OUT = 2

HDWF = c_int
HDWF_NONE = 0

DwfEnumFilter = c_int
ENUMFILTER_ALL = 0
ENUMFILTER_TYPE = 0x8000000
ENUMFILTER_USB = 0x0000001
ENUMFILTER_NETWORK = 0x0000002
ENUMFILTER_AXI = 0x0000004
ENUMFILTER_REMOTE = 0x1000000
ENUMFILTER_AUDIO = 0x2000000
ENUMFILTER_DEMO = 0x4000000

DwfDevId = c_int
DEVID_EEXPLORER = 1
DEVID_DISCOVERY = 2
DEVID_DISCOVERY2 = 3
DEVID_DDISCOVERY = 4
DEVID_ADP3X50 = 6
DEVID_ECLYPSE = 7
DEVID_ADP5250 = 8
DEVID_DPS3340 = 9
DEVID_DISCOVERY3 = 10

DwfDevVer = c_int
DEVVER_EEXPLORER_C = 2
DEVVER_EEXPLORER_E = 4
DEVVER_EEXPLORER_F = 5
DEVVER_DISCOVERY_A = 1
DEVVER_DISCOVERY_B = 2
DEVVER_DISCOVERY_C = 3

DwfTrigSrc = c_ubyte
TRIGSRC_NONE = 0
TRIGSRC_PC = 1
TRIGSRC_DETECTOR_ANALOG_IN = 2
TRIGSRC_DETECTOR_DIGITAL_IN = 3
TRIGSRC_ANALOG_IN = 4
TRIGSRC_DIGITAL_IN = 5
TRIGSRC_DIGITAL_OUT = 6
TRIGSRC_ANALOG_OUT1 = 7
TRIGSRC_ANALOG_OUT2 = 8
TRIGSRC_ANALOG_OUT3 = 9
TRIGSRC_ANALOG_OUT4 = 10
TRIGSRC_EXTERNAL1 = 11
TRIGSRC_EXTERNAL2 = 12
TRIGSRC_EXTERNAL3 = 13
TRIGSRC_EXTERNAL4 = 14
TRIGSRC_HIGH = 15
TRIGSRC_LOW = 16
TRIGSRC_CLOCK = 17

DwfState = c_ubyte
STATE_READY = 0
STATE_CONFIG = 4
STATE_PREFILL = 5
STATE_ARMED = 1
STATE_WAIT = 7
STATE_TRIGGERED = 3
STATE_RUNNING = 3
STATE_DONE = 2

DwfDeci = c_int
DECI_ANALOG_IN_CHANNEL_COUNT = 1
DECI_ANALOG_OUT_CHANNEL_COUNT = 2
DECI_ANALOG_IO_CHANNEL_COUNT = 3
DECI_DIGITAL_IN_CHANNEL_COUNT = 4
DECI_DIGITAL_OUT_CHANNEL_COUNT = 5
DECI_DIGITAL_IO_CHANNEL_COUNT = 6
DECI_ANALOG_IN_BUFFER_SIZE = 7
DECI_ANALOG_OUT_BUFFER_SIZE = 8
DECI_DIGITAL_IN_BUFFER_SIZE = 9
DECI_DIGITAL_OUT_BUFFER_SIZE = 10
DECI_TEXT_INFO = -2

DwfAcqMode = c_int
ACQMODE_SINGLE = 0
ACQMODE_SCAN_SHIFT = 1
ACQMODE_SCAN_SCREEN = 2
ACQMODE_RECORD = 3
ACQMODE_OVERS = 4
ACQMODE_SINGLE1 = 5
ACQMODE_RECORD2 = 6

DwfFilter = c_int
FILTER_DECIMATE = 0
FILTER_AVERAGE = 1
FILTER_MINMAX = 2
FILTER_AVERAGEFIT  = 3

DwfTrigType = c_int
TRIGTYPE_EDGE = 0
TRIGTYPE_PULSE = 1
TRIGTYPE_TRANSITION = 2
TRIGTYPE_WINDOW = 3

DwfTriggerSlope = c_int
TRIGGER_SLOPE_RISE = 0
TRIGGER_SLOPE_FALL = 1
TRIGGER_SLOPE_EITHER = 2

DwfTrigLen = c_int
TRIGLEN_LESS = 0
TRIGLEN_TIMEOUT = 1
TRIGLEN_MORE = 2

DwfErc = c_int
DWFERC_NO_ERC = 0  # No error occurred
DWFERC_UNKNOWN_ERROR = 1  # API waiting on pending API timed out
DWFERC_API_LOCK_TIMEOUT = 2  # API waiting on pending API timed out
DWFERC_ALREADY_OPENED = 3  # Device already opened
DWFERC_NOT_SUPPORTED = 4  # Device not supported
DWFERC_INVALID_PARAMETER0 = 0x10  # Invalid parameter sent in API call
DWFERC_INVALID_PARAMETER1 = 0x11  # Invalid parameter sent in API call
DWFERC_INVALID_PARAMETER2 = 0x12  # Invalid parameter sent in API call
DWFERC_INVALID_PARAMETER3 = 0x13  # Invalid parameter sent in API call
DWFERC_INVALID_PARAMETER4 = 0x14  # Invalid parameter sent in API call

DwfFunc = c_ubyte
FUNC_DC = 0
FUNC_SINE = 1
FUNC_SQUARE = 2
FUNC_TRIANGLE = 3
FUNC_RAMP_UP = 4
FUNC_RAMP_DOWN = 5
FUNC_NOISE = 6
FUNC_PULSE = 7
FUNC_TRAPEZIUM = 8
FUNC_SINE_POWER = 9
FUNC_CUSTOM_PATTERN = 28
FUNC_PLAY_PATTERN = 29
FUNC_CUSTOM = 30
FUNC_PLAY = 31
FUNC_ANALOG_IN1 = 64
FUNC_ANALOG_IN2 = 65
FUNC_ANALOG_IN3 = 66
FUNC_ANALOG_IN4 = 67
FUNC_ANALOG_IN5 = 68
FUNC_ANALOG_IN6 = 69
FUNC_ANALOG_IN7 = 70
FUNC_ANALOG_IN8 = 71
FUNC_ANALOG_IN9 = 72
FUNC_ANALOG_IN10 = 73
FUNC_ANALOG_IN11 = 74
FUNC_ANALOG_IN12 = 75
FUNC_ANALOG_IN13 = 76
FUNC_ANALOG_IN14 = 77
FUNC_ANALOG_IN15 = 78
FUNC_ANALOG_IN16 = 79

DwfAnalogIO = c_ubyte
ANALOGIO_ENABLE = 1
ANALOGIO_VOLTAGE = 2
ANALOGIO_CURRENT = 3
ANALOGIO_POWER = 4
ANALOGIO_TEMPERATURE = 5
ANALOGIO_DMM = 6
ANALOGIO_RANGE = 7
ANALOGIO_MEASURE = 8
ANALOGIO_TIME = 9
ANALOGIO_FREQUENCY = 10
ANALOGIO_RESISTANCE = 11
ANALOGIO_SLEW = 12

DwfDmm = c_int
DMM_RESISTANCE = 1
DMM_CONTINUITY = 2
DMM_DIODE = 3
DMM_DC_VOLTAGE = 4
DMM_AC_VOLTAGE = 5
DMM_DC_CURRENT = 6
DMM_AC_CURRENT = 7
DMM_DC_LOW_CURRENT = 8
DMM_AC_LOW_CURRENT = 9
DMM_TEMPERATURE = 10

DwfAnalogOutNode = c_int
ANALOG_OUT_NODE_CARRIER = 0
ANALOG_OUT_NODE_FM = 1
ANALOG_OUT_NODE_AM = 2

DwfAnalogOutMode = c_int
ANALOG_OUT_MODE_VOLTAGE = 0
ANALOG_OUT_MODE_CURRENT = 1

DwfAnalogOutIdle = c_int
ANALOG_OUT_IDLE_DISABLE = 0
ANALOG_OUT_IDLE_OFFSET = 1
ANALOG_OUT_IDLE_INITIAL = 2

DwfDigitalInClockSource = c_int
DIGITAL_IN_CLOCK_SOURCE_INTERNAL = 0
DIGITAL_IN_CLOCK_SOURCE_EXTERNAL = 1
DIGITAL_IN_CLOCK_SOURCE_EXTERNAL2 = 2

DwfDigitalInSampleMode = c_int
DIGITAL_IN_SAMPLE_MODE_SIMPLE = 0
DIGITAL_IN_SAMPLE_MODE_NOISE = 1

DwfDigitalOutOutput = c_int
DIGITAL_OUT_OUTPUT_PUSH_PULL = 0
DIGITAL_OUT_OUTPUT_OPEN_DRAIN = 1
DIGITAL_OUT_OUTPUT_OPEN_SOURCE = 2
DIGITAL_OUT_OUTPUT_THREE_STATE = 3

DwfDigitalOutType = c_int
DIGITAL_OUT_TYPE_PULSE = 0
DIGITAL_OUT_TYPE_CUSTOM = 1
DIGITAL_OUT_TYPE_RANDOM = 2
DIGITAL_OUT_TYPE_ROM = 3
DIGITAL_OUT_TYPE_STATE = 4
DIGITAL_OUT_TYPE_PLAY = 5

DwfDigitalOutIdle = c_int
DIGITAL_OUT_IDLE_INIT = 0
DIGITAL_OUT_IDLE_LOW = 1
DIGITAL_OUT_IDLE_HIGH = 2
DIGITAL_OUT_IDLE_ZET = 3

DwfAnalogImpedance = c_int
ANALOG_IMPEDANCE_IMPEDANCE = 0  # Ohms
ANALOG_IMPEDANCE_IMPEDANCE_PHASE = 1  # Radians
ANALOG_IMPEDANCE_RESISTANCE = 2  # Ohms
ANALOG_IMPEDANCE_REACTANCE = 3  # Ohms
ANALOG_IMPEDANCE_ADMITTANCE = 4  # Siemens
ANALOG_IMPEDANCE_ADMITTANCE_PHASE = 5  # Radians
ANALOG_IMPEDANCE_CONDUCTANCE = 6  # Siemens
ANALOG_IMPEDANCE_SUSCEPTANCE = 7  # Siemens
ANALOG_IMPEDANCE_SERIES_CAPACITANCE = 8  # Farad
ANALOG_IMPEDANCE_PARALLEL_CAPACITANCE = 9  # Farad
ANALOG_IMPEDANCE_SERIES_INDUCTANCE = 10  # Henry
ANALOG_IMPEDANCE_PARALLEL_INDUCTANCE = 11  # Henry
ANALOG_IMPEDANCE_DISSIPATION = 12  # factor
ANALOG_IMPEDANCE_QUALITY = 13  # factor
ANALOG_IMPEDANCE_VRMS = 14  # Vrms
ANALOG_IMPEDANCE_VREAL = 15  # V real
ANALOG_IMPEDANCE_VIMAG = 16  # V imag
ANALOG_IMPEDANCE_IRMS = 17  # Irms
ANALOG_IMPEDANCE_IREAL = 18  # I real
ANALOG_IMPEDANCE_IIMAG = 19  # I imag

DwfParam = c_int
PARAM_USB_POWER = 2  # 1 keep the USB power enabled even when AUX is connected, Analog Discovery 2
PARAM_LED_BRIGHTNESS = 3  # LED brightness 0 ... 100%, Digital Discovery
PARAM_ON_CLOSE = 4  # 0 continue, 1 stop, 2 shutdown
PARAM_AUDIO_OUT = 5  # 0 disable / 1 enable audio output, Analog Discovery 1, 2
PARAM_USB_LIMIT = 6  # 0..1000 mA USB power limit, -1 no limit, Analog Discovery 1, 2
PARAM_ANALOG_OUT = 7  # 0 disable / 1 enable
PARAM_FREQUENCY = 8  # Hz
PARAM_EXT_FREQ = 9  # Hz
PARAM_CLOCK_MODE = 10  # 0 internal, 1 output, 2 input, 3 IO
PARAM_TEMP_LIMIT = 11
PARAM_FREQ_PHASE = 12
PARAM_DIGITAL_VOLTAGE = 13
PARAM_FREQ_PHASE_STEPS = 14

DwfWindow = c_int
WINDOW_RECTANGULAR = 0
WINDOW_TRIANGULAR = 1
WINDOW_HAMMING = 2
WINDOW_HANN = 3
WINDOW_COSINE = 4
WINDOW_BLACKMAN_HARRIS = 5
WINDOW_FLAT_TOP = 6
WINDOW_KAISER = 7
WINDOW_BLACKMAN = 8
WINDOW_FLAT_TOP_M = 9

DwfAnalogCoupling = c_int
ANALOG_COUPLING_DC = 0
ANALOG_COUPLING_AC = 1

DwfFiirMode = c_int
FIIR_WINDOW = 0
FIIR_FIR = 1
FIIR_IIR_BUTTERWORTH = 2
FIIR_IIR_CHEBYSHEV = 3

DwfFiirType = c_int
FIIR_LOW_PASS = 0
FIIR_HIGH_PASS = 1
FIIR_BAND_PASS = 2
FIIR_BAND_STOP = 3

DwfFiirInput = c_int
FIIR_RAW = 0
FIIR_DECIMATE = 1
FIIR_AVERAGE = 2

# pylint:disable=line-too-long

### SYSTEM

dwf_get_last_error = _dwf_function('FDwfGetLastError', (_OUT, POINTER(DwfErc), 'pdwferc'))
dwf_get_last_error_msg = _dwf_function('FDwfGetLastErrorMsg', (_IN, c_char_p, 'szError'))
dwf_get_version = _dwf_function('FDwfGetVersion', (_IN, c_char_p, 'szVersion'))

if _version >= (3, 9, 1):
    dwf_param_set = _dwf_function('FDwfParamSet', (_IN, DwfParam, 'param'), (_IN, c_int, 'value'))
    dwf_param_get = _dwf_function('FDwfParamGet', (_IN, DwfParam, 'param'), (_OUT, POINTER(c_int), 'pvalue'))

### DEVICE MANAGMENT FUNCTIONS

# Enumeration

dwf_enum = _dwf_function('FDwfEnum', (_IN, DwfEnumFilter, 'enumfilter'), (_OUT, POINTER(c_int), 'pcDevice'))
if _version >= (3, 17, 1):
    dwf_enum_start = _dwf_function('FDwfEnumStart', (_IN, DwfEnumFilter, 'enumfilter'))
    dwf_enum_stop = _dwf_function('FDwfEnumStop', (_OUT, POINTER(c_int), 'pcDevice'))
    dwf_enum_info = _dwf_function('FDwfEnumInfo', (_IN, c_int, 'idxDevice'), (_IN, c_char_p, 'szOpt'))
dwf_enum_device_type = _dwf_function('FDwfEnumDeviceType', (_IN, c_int, 'idxDevice'), (_OUT, POINTER(DwfDevId), 'pDeviceId'), (_OUT, POINTER(DwfDevVer), 'pDeviceRevision'))
dwf_enum_device_is_opened = _dwf_function('FDwfEnumDeviceIsOpened', (_IN, c_int, 'idxDevice'), (_OUT, POINTER(c_int), 'pfIsUsed'))
dwf_enum_user_name = _dwf_function('FDwfEnumUserName', (_IN, c_int, 'idxDevice'), (_IN, c_char_p, 'szUserName'))
dwf_enum_device_name = _dwf_function('FDwfEnumDeviceName', (_IN, c_int, 'idxDevice'), (_IN, c_char_p, 'szDeviceName'))
dwf_enum_sn = _dwf_function('FDwfEnumSN', (_IN, c_int, 'idxDevice'), (_IN, c_char_p, 'szSN'))
dwf_enum_config = _dwf_function('FDwfEnumConfig', (_IN, c_int, 'idxDevice'), (_OUT, POINTER(c_int), 'pcConfig'))
dwf_enum_config_info = _dwf_function('FDwfEnumConfigInfo', (_IN, c_int, 'idxDevice'), (_IN, DwfDeci, 'info'), (_OUT, POINTER(c_int), 'pv'))
dwf_enum_config_info_str = _dwf_function('FDwfEnumConfigInfo', (_IN, c_int, 'idxDevice'), (_IN, DwfDeci, 'info'), (_IN, c_char_p, 'pv'))

# Open/Close

dwf_device_open = _dwf_function('FDwfDeviceOpen', (_IN, c_int, 'idxDevice'), (_OUT, POINTER(HDWF), 'phdwf'))
if _version >= (3, 17, 1):
    dwf_device_open_ex = _dwf_function('FDwfDeviceOpenEx', (_IN, c_char_p, 'szOpt'), (_OUT, POINTER(HDWF), 'phdwf'))
dwf_device_config_open = _dwf_function('FDwfDeviceConfigOpen', (_IN, c_int, 'idxDev'), (_IN, c_int, 'idxCfg'), (_OUT, POINTER(HDWF), 'phdwf'))
dwf_device_close = _dwf_function('FDwfDeviceClose', (_IN, HDWF, 'hdwf'))
dwf_device_close_all = _dwf_function('FDwfDeviceCloseAll')
dwf_device_auto_configure_set = _dwf_function('FDwfDeviceAutoConfigureSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fAutoConfigure'))
dwf_device_auto_configure_get = _dwf_function('FDwfDeviceAutoConfigureGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfAutoConfigure'))
dwf_device_reset = _dwf_function('FDwfDeviceReset', (_IN, HDWF, 'hdwf'))
dwf_device_enable_set = _dwf_function('FDwfDeviceEnableSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fEnable'))
dwf_device_trigger_info = _dwf_function('FDwfDeviceTriggerInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfstrigsrc'))
dwf_device_trigger_set = _dwf_function('FDwfDeviceTriggerSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxPin'), (_IN, DwfTrigSrc, 'trigsrc'))
dwf_device_trigger_get = _dwf_function('FDwfDeviceTriggerGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxPin'), (_OUT, POINTER(DwfTrigSrc), 'ptrigsrc'))
dwf_device_trigger_pc = _dwf_function('FDwfDeviceTriggerPC', (_IN, HDWF, 'hdwf'))
dwf_device_trigger_slope_info = _dwf_function('FDwfDeviceTriggerSlopeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfsslope'))
if _version >= (3, 9, 1):
    dwf_device_param_set = _dwf_function('FDwfDeviceParamSet', (_IN, HDWF, 'hdwf'), (_IN, DwfParam, 'param'), (_IN, c_int, 'value'))
    dwf_device_param_get = _dwf_function('FDwfDeviceParamGet', (_IN, HDWF, 'hdwf'), (_IN, DwfParam, 'param'), (_OUT, POINTER(c_int), 'pvalue'))

### ANALOG _IN INSTRUMENT FUNCTIONS

# Control and status

dwf_analog_in_reset = _dwf_function('FDwfAnalogInReset', (_IN, HDWF, 'hdwf'))
dwf_analog_in_configure = _dwf_function('FDwfAnalogInConfigure', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fReconfigure'), (_IN, c_int, 'fStart'))
dwf_analog_in_trigger_force = _dwf_function('FDwfAnalogInTriggerForce', (_IN, HDWF, 'hdwf'), )
dwf_analog_in_status = _dwf_function('FDwfAnalogInStatus', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fReadData'), (_OUT, POINTER(DwfState), 'psts'))
dwf_analog_in_status_samples_left = _dwf_function('FDwfAnalogInStatusSamplesLeft', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcSamplesLeft'))
dwf_analog_in_status_samples_valid = _dwf_function('FDwfAnalogInStatusSamplesValid', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcSamplesValid'))
dwf_analog_in_status_index_write = _dwf_function('FDwfAnalogInStatusIndexWrite', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pidxWrite'))
dwf_analog_in_status_auto_triggered = _dwf_function('FDwfAnalogInStatusAutoTriggered', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfAuto'))
dwf_analog_in_status_data = _dwf_function('FDwfAnalogInStatusData', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, POINTER(c_double), 'rgdVoltData'), (_IN, c_int, 'cdData'))
dwf_analog_in_status_data2 = _dwf_function('FDwfAnalogInStatusData2', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, POINTER(c_double), 'rgdVoltData'), (_IN, c_int, 'idxData'), (_IN, c_int, 'cdData'))
dwf_analog_in_status_data16 = _dwf_function('FDwfAnalogInStatusData16', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, POINTER(c_short), 'rgu16Data'), (_IN, c_int, 'idxData'), (_IN, c_int, 'cdData'))
dwf_analog_in_status_noise = _dwf_function('FDwfAnalogInStatusNoise', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, POINTER(c_double), 'rgdMin'), (_IN, POINTER(c_double), 'rgdMax'), (_IN, c_int, 'cdData'))
dwf_analog_in_status_noise2 = _dwf_function('FDwfAnalogInStatusNoise2', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, POINTER(c_double), 'rgdMin'), (_IN, POINTER(c_double), 'rgdMax'), (_IN, c_int, 'idxData'), (_IN, c_int, 'cdData'))
dwf_analog_in_status_sample = _dwf_function('FDwfAnalogInStatusSample', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'pdVoltSample'))
if _version >= (3, 16, 3):
    dwf_analog_in_status_time = _dwf_function('FDwfAnalogInStatusTime', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'psecUtc'), (_OUT, POINTER(c_uint), 'ptick'), (_OUT, POINTER(c_uint), 'pticksPerSecond'))

dwf_analog_in_status_record = _dwf_function('FDwfAnalogInStatusRecord', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcdDataAvailable'), (_OUT, POINTER(c_int), 'pcdDataLost'), (_OUT, POINTER(c_int), 'pcdDataCorrupt'))
dwf_analog_in_record_length_set = _dwf_function('FDwfAnalogInRecordLengthSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'sLength'))
dwf_analog_in_record_length_get = _dwf_function('FDwfAnalogInRecordLengthGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psLength'))

if _version >= (3, 18, 30):
    dwf_analog_in_counter_info = _dwf_function('FDwfAnalogInCounterInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pcntMax'), (_OUT, POINTER(c_double), 'psecMax'))
    dwf_analog_in_counter_set = _dwf_function('FDwfAnalogInCounterSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'sec'))
    dwf_analog_in_counter_get = _dwf_function('FDwfAnalogInCounterGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psec'))
    dwf_analog_in_counter_status = _dwf_function('FDwfAnalogInCounterStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pcnt'), (_OUT, POINTER(c_double), 'pfreq'), (_OUT, POINTER(c_int), 'ptick'))

# Acquisition configuration

dwf_analog_in_frequency_info = _dwf_function('FDwfAnalogInFrequencyInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'phzMin'), (_OUT, POINTER(c_double), 'phzMax'))
dwf_analog_in_frequency_set = _dwf_function('FDwfAnalogInFrequencySet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hzFrequency'))
dwf_analog_in_frequency_get = _dwf_function('FDwfAnalogInFrequencyGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'phzFrequency'))

dwf_analog_in_bits_info = _dwf_function('FDwfAnalogInBitsInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnBits'))

dwf_analog_in_buffer_size_info = _dwf_function('FDwfAnalogInBufferSizeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnSizeMin'), (_OUT, POINTER(c_int), 'pnSizeMax'))
dwf_analog_in_buffer_size_set = _dwf_function('FDwfAnalogInBufferSizeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'nSize'))
dwf_analog_in_buffer_size_get = _dwf_function('FDwfAnalogInBufferSizeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnSize'))

if _version >= (3, 21, 0):
    dwf_analog_in_buffers_info = _dwf_function('FDwfAnalogInBuffersInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pMax'))
    dwf_analog_in_buffers_set = _dwf_function('FDwfAnalogInBuffersSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'n'))
    dwf_analog_in_buffers_get = _dwf_function('FDwfAnalogInBuffersGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pn'))
    dwf_analog_in_buffers_status = _dwf_function('FDwfAnalogInBuffersStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pn'))

dwf_analog_in_noise_size_info = _dwf_function('FDwfAnalogInNoiseSizeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnSizeMax'))
dwf_analog_in_noise_size_set = _dwf_function('FDwfAnalogInNoiseSizeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'nSize'))
dwf_analog_in_noise_size_get = _dwf_function('FDwfAnalogInNoiseSizeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnSize'))

dwf_analog_in_acquisition_mode_info = _dwf_function('FDwfAnalogInAcquisitionModeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfsacqmode'))
dwf_analog_in_acquisition_mode_set = _dwf_function('FDwfAnalogInAcquisitionModeSet', (_IN, HDWF, 'hdwf'), (_IN, DwfAcqMode, 'acqmode'))
dwf_analog_in_acquisition_mode_get = _dwf_function('FDwfAnalogInAcquisitionModeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfAcqMode), 'pacqmode'))

# Channel configuration

dwf_analog_in_channel_count = _dwf_function('FDwfAnalogInChannelCount', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcChannel'))
if _version >= (3, 21, 0):
    dwf_analog_in_channel_counts = _dwf_function('FDwfAnalogInChannelCounts', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcReal'), (_OUT, POINTER(c_int), 'pcFilter'), (_OUT, POINTER(c_int), 'pcTotal'))
dwf_analog_in_channel_enable_set = _dwf_function('FDwfAnalogInChannelEnableSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'fEnable'))
dwf_analog_in_channel_enable_get = _dwf_function('FDwfAnalogInChannelEnableGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfEnable'))
dwf_analog_in_channel_filter_info = _dwf_function('FDwfAnalogInChannelFilterInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfsfilter'))
dwf_analog_in_channel_filter_set = _dwf_function('FDwfAnalogInChannelFilterSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfFilter, 'filter'))
dwf_analog_in_channel_filter_get = _dwf_function('FDwfAnalogInChannelFilterGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfFilter), 'pfilter'))
dwf_analog_in_channel_range_info = _dwf_function('FDwfAnalogInChannelRangeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvoltsMin'), (_OUT, POINTER(c_double), 'pvoltsMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_analog_in_channel_range_steps = _dwf_function('FDwfAnalogInChannelRangeSteps', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_double), 'rgVoltsStep'), (_OUT, POINTER(c_int), 'pnSteps'))
dwf_analog_in_channel_range_set = _dwf_function('FDwfAnalogInChannelRangeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'voltsRange'))
dwf_analog_in_channel_range_get = _dwf_function('FDwfAnalogInChannelRangeGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'pvoltsRange'))
dwf_analog_in_channel_offset_info = _dwf_function('FDwfAnalogInChannelOffsetInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvoltsMin'), (_OUT, POINTER(c_double), 'pvoltsMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_analog_in_channel_offset_set = _dwf_function('FDwfAnalogInChannelOffsetSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'voltOffset'))
dwf_analog_in_channel_offset_get = _dwf_function('FDwfAnalogInChannelOffsetGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'pvoltOffset'))
dwf_analog_in_channel_attenuation_set = _dwf_function('FDwfAnalogInChannelAttenuationSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'xAttenuation'))
dwf_analog_in_channel_attenuation_get = _dwf_function('FDwfAnalogInChannelAttenuationGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'pxAttenuation'))
if _version >= (3, 14, 3):
    dwf_analog_in_channel_bandwidth_set = _dwf_function('FDwfAnalogInChannelBandwidthSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'hz'))
    dwf_analog_in_channel_bandwidth_get = _dwf_function('FDwfAnalogInChannelBandwidthGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'phz'))
    dwf_analog_in_channel_impedance_set = _dwf_function('FDwfAnalogInChannelImpedanceSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'ohms'))
    dwf_analog_in_channel_impedance_get = _dwf_function('FDwfAnalogInChannelImpedanceGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'pOhms'))
if _version >= (3, 18, 30):
    dwf_analog_in_channel_coupling_info = _dwf_function('FDwfAnalogInChannelCouplingInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfscoupling'))
    dwf_analog_in_channel_coupling_set = _dwf_function('FDwfAnalogInChannelCouplingSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogCoupling, 'coupling'))
    dwf_analog_in_channel_coupling_get = _dwf_function('FDwfAnalogInChannelCouplingGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfAnalogCoupling), 'pcoupling'))

# FIR and IIR filters

if _version >= (3, 21, 0):
    dwf_analog_in_channel_fiir_info = _dwf_function('FDwfAnalogInChannelFiirInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'cFIR'), (_OUT, POINTER(c_int), 'cIIR'))
    dwf_analog_in_channel_fiir_set = _dwf_function('FDwfAnalogInChannelFiirSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfFiirInput, 'input'), (_IN, DwfFiirMode, 'fiir'), (_IN, DwfFiirType, 'pass'), (_IN, c_int, 'ord'), (_IN, c_double, 'hz1'), (_IN, c_double, 'hz2'), (_IN, c_double, 'ep'))
    dwf_analog_in_channel_window_set = _dwf_function('FDwfAnalogInChannelWindowSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfWindow, 'win'), (_IN, c_int, 'size'), (_IN, c_double, 'beta'))
    dwf_analog_in_channel_custom_window_set = _dwf_function('FDwfAnalogInChannelCustomWindowSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, POINTER(c_double), 'rg'), (_IN, c_int, 'size'), (_IN, c_int, 'normalize'))

# Trigger configuration

dwf_analog_in_trigger_source_set = _dwf_function('FDwfAnalogInTriggerSourceSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTrigSrc, 'trigsrc'))
dwf_analog_in_trigger_source_get = _dwf_function('FDwfAnalogInTriggerSourceGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTrigSrc), 'ptrigsrc'))

dwf_analog_in_trigger_position_info = _dwf_function('FDwfAnalogInTriggerPositionInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_analog_in_trigger_position_set = _dwf_function('FDwfAnalogInTriggerPositionSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secPosition'))
dwf_analog_in_trigger_position_get = _dwf_function('FDwfAnalogInTriggerPositionGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecPosition'))
dwf_analog_in_trigger_position_status = _dwf_function('FDwfAnalogInTriggerPositionStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecPosition'))

dwf_analog_in_trigger_auto_timeout_info = _dwf_function('FDwfAnalogInTriggerAutoTimeoutInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_analog_in_trigger_auto_timeout_set = _dwf_function('FDwfAnalogInTriggerAutoTimeoutSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secTimeout'))
dwf_analog_in_trigger_auto_timeout_get = _dwf_function('FDwfAnalogInTriggerAutoTimeoutGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecTimeout'))

dwf_analog_in_trigger_hold_off_info = _dwf_function('FDwfAnalogInTriggerHoldOffInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'), (_OUT, POINTER(c_double), 'pnStep'))
dwf_analog_in_trigger_hold_off_set = _dwf_function('FDwfAnalogInTriggerHoldOffSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secHoldOff'))
dwf_analog_in_trigger_hold_off_get = _dwf_function('FDwfAnalogInTriggerHoldOffGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecHoldOff'))

dwf_analog_in_trigger_type_info = _dwf_function('FDwfAnalogInTriggerTypeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfstrigtype'))
dwf_analog_in_trigger_type_set = _dwf_function('FDwfAnalogInTriggerTypeSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTrigType, 'trigtype'))
dwf_analog_in_trigger_type_get = _dwf_function('FDwfAnalogInTriggerTypeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTrigType), 'ptrigtype'))

dwf_analog_in_trigger_channel_info = _dwf_function('FDwfAnalogInTriggerChannelInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pidxMin'), (_OUT, POINTER(c_int), 'pidxMax'))
dwf_analog_in_trigger_channel_set = _dwf_function('FDwfAnalogInTriggerChannelSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
dwf_analog_in_trigger_channel_get = _dwf_function('FDwfAnalogInTriggerChannelGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pidxChannel'))

dwf_analog_in_trigger_filter_info = _dwf_function('FDwfAnalogInTriggerFilterInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfsfilter'))
dwf_analog_in_trigger_filter_set = _dwf_function('FDwfAnalogInTriggerFilterSet', (_IN, HDWF, 'hdwf'), (_IN, DwfFilter, 'filter'))
dwf_analog_in_trigger_filter_get = _dwf_function('FDwfAnalogInTriggerFilterGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfFilter), 'pfilter'))

dwf_analog_in_trigger_level_info = _dwf_function('FDwfAnalogInTriggerLevelInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvoltsMin'), (_OUT, POINTER(c_double), 'pvoltsMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_analog_in_trigger_level_set = _dwf_function('FDwfAnalogInTriggerLevelSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'voltsLevel'))
dwf_analog_in_trigger_level_get = _dwf_function('FDwfAnalogInTriggerLevelGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvoltsLevel'))

dwf_analog_in_trigger_hysteresis_info = _dwf_function('FDwfAnalogInTriggerHysteresisInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvoltsMin'), (_OUT, POINTER(c_double), 'pvoltsMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_analog_in_trigger_hysteresis_set = _dwf_function('FDwfAnalogInTriggerHysteresisSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'voltsLevel'))
dwf_analog_in_trigger_hysteresis_get = _dwf_function('FDwfAnalogInTriggerHysteresisGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvoltsHysteresis'))

dwf_analog_in_trigger_condition_info = _dwf_function('FDwfAnalogInTriggerConditionInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfstrigcond'))
dwf_analog_in_trigger_condition_set = _dwf_function('FDwfAnalogInTriggerConditionSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTriggerSlope, 'trigcond'))
dwf_analog_in_trigger_condition_get = _dwf_function('FDwfAnalogInTriggerConditionGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTriggerSlope), 'ptrigcond'))

dwf_analog_in_trigger_length_info = _dwf_function('FDwfAnalogInTriggerLengthInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_analog_in_trigger_length_set = _dwf_function('FDwfAnalogInTriggerLengthSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secLength'))
dwf_analog_in_trigger_length_get = _dwf_function('FDwfAnalogInTriggerLengthGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecLength'))

dwf_analog_in_trigger_length_condition_info = _dwf_function('FDwfAnalogInTriggerLengthConditionInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfstriglen'))
dwf_analog_in_trigger_length_condition_set = _dwf_function('FDwfAnalogInTriggerLengthConditionSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTrigLen, 'triglen'))
dwf_analog_in_trigger_length_condition_get = _dwf_function('FDwfAnalogInTriggerLengthConditionGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTrigLen), 'ptriglen'))

dwf_analog_in_sampling_source_set = _dwf_function('FDwfAnalogInSamplingSourceSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTrigSrc, 'trigsrc'))
dwf_analog_in_sampling_source_get = _dwf_function('FDwfAnalogInSamplingSourceGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTrigSrc), 'ptrigsrc'))

dwf_analog_in_sampling_slope_set = _dwf_function('FDwfAnalogInSamplingSlopeSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTriggerSlope, 'slope'))
dwf_analog_in_sampling_slope_get = _dwf_function('FDwfAnalogInSamplingSlopeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTriggerSlope), 'pslope'))

dwf_analog_in_sampling_delay_set = _dwf_function('FDwfAnalogInSamplingDelaySet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'sec'))
dwf_analog_in_sampling_delay_get = _dwf_function('FDwfAnalogInSamplingDelayGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psec'))

### ANALOG _OUT INSTRUMENT FUNCTIONS

# Configuration

dwf_analog_out_count = _dwf_function('FDwfAnalogOutCount', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcChannel'))

dwf_analog_out_master_set = _dwf_function('FDwfAnalogOutMasterSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxMaster'))
dwf_analog_out_master_get = _dwf_function('FDwfAnalogOutMasterGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pidxMaster'))

dwf_analog_out_trigger_source_set = _dwf_function('FDwfAnalogOutTriggerSourceSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfTrigSrc, 'trigsrc'))
dwf_analog_out_trigger_source_get = _dwf_function('FDwfAnalogOutTriggerSourceGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfTrigSrc), 'ptrigsrc'))

dwf_analog_out_trigger_slope_set = _dwf_function('FDwfAnalogOutTriggerSlopeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfTriggerSlope, 'slope'))
dwf_analog_out_trigger_slope_get = _dwf_function('FDwfAnalogOutTriggerSlopeGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfTriggerSlope), 'pslope'))

dwf_analog_out_run_info = _dwf_function('FDwfAnalogOutRunInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'))
dwf_analog_out_run_set = _dwf_function('FDwfAnalogOutRunSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'secRun'))
dwf_analog_out_run_get = _dwf_function('FDwfAnalogOutRunGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'psecRun'))
dwf_analog_out_run_status = _dwf_function('FDwfAnalogOutRunStatus', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'psecRun'))

dwf_analog_out_wait_info = _dwf_function('FDwfAnalogOutWaitInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'))
dwf_analog_out_wait_set = _dwf_function('FDwfAnalogOutWaitSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'secWait'))
dwf_analog_out_wait_get = _dwf_function('FDwfAnalogOutWaitGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'psecWait'))

dwf_analog_out_repeat_info = _dwf_function('FDwfAnalogOutRepeatInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pnMin'), (_OUT, POINTER(c_int), 'pnMax'))
dwf_analog_out_repeat_set = _dwf_function('FDwfAnalogOutRepeatSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'cRepeat'))
dwf_analog_out_repeat_get = _dwf_function('FDwfAnalogOutRepeatGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pcRepeat'))
dwf_analog_out_repeat_status = _dwf_function('FDwfAnalogOutRepeatStatus', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pcRepeat'))

dwf_analog_out_repeat_trigger_set = _dwf_function('FDwfAnalogOutRepeatTriggerSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'fRepeatTrigger'))
dwf_analog_out_repeat_trigger_get = _dwf_function('FDwfAnalogOutRepeatTriggerGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfRepeatTrigger'))

# EExplorer channel 3&4 current/voltage limitation

dwf_analog_out_limitation_info = _dwf_function('FDwfAnalogOutLimitationInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'pMin'), (_OUT, POINTER(c_double), 'pMax'))
dwf_analog_out_limitation_set = _dwf_function('FDwfAnalogOutLimitationSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_double, 'limit'))
dwf_analog_out_limitation_get = _dwf_function('FDwfAnalogOutLimitationGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'plimit'))

dwf_analog_out_mode_set = _dwf_function('FDwfAnalogOutModeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutMode, 'mode'))
dwf_analog_out_mode_get = _dwf_function('FDwfAnalogOutModeGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfAnalogOutMode), 'pmode'))

dwf_analog_out_idle_info = _dwf_function('FDwfAnalogOutIdleInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfsidle'))
dwf_analog_out_idle_set = _dwf_function('FDwfAnalogOutIdleSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutIdle, 'idle'))
dwf_analog_out_idle_get = _dwf_function('FDwfAnalogOutIdleGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfAnalogOutIdle), 'pidle'))

dwf_analog_out_node_info = _dwf_function('FDwfAnalogOutNodeInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfsnode'))
dwf_analog_out_node_enable_set = _dwf_function('FDwfAnalogOutNodeEnableSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, c_int, 'fMode'))
dwf_analog_out_node_enable_get = _dwf_function('FDwfAnalogOutNodeEnableGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_int), 'pfMode'))

dwf_analog_out_node_function_info = _dwf_function('FDwfAnalogOutNodeFunctionInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_uint), 'pfsfunc'))
dwf_analog_out_node_function_set = _dwf_function('FDwfAnalogOutNodeFunctionSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, DwfFunc, 'func'))
dwf_analog_out_node_function_get = _dwf_function('FDwfAnalogOutNodeFunctionGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(DwfFunc), 'pfunc'))

dwf_analog_out_node_frequency_info = _dwf_function('FDwfAnalogOutNodeFrequencyInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'phzMin'), (_OUT, POINTER(c_double), 'phzMax'))
dwf_analog_out_node_frequency_set = _dwf_function('FDwfAnalogOutNodeFrequencySet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, c_double, 'hzFrequency'))
dwf_analog_out_node_frequency_get = _dwf_function('FDwfAnalogOutNodeFrequencyGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'phzFrequency'))

# Carrier Amplitude or Modulation Index

dwf_analog_out_node_amplitude_info = _dwf_function('FDwfAnalogOutNodeAmplitudeInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'pMin'), (_OUT, POINTER(c_double), 'pMax'))
dwf_analog_out_node_amplitude_set = _dwf_function('FDwfAnalogOutNodeAmplitudeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, c_double, 'vAmplitude'))
dwf_analog_out_node_amplitude_get = _dwf_function('FDwfAnalogOutNodeAmplitudeGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'pvAmplitude'))

dwf_analog_out_node_offset_info = _dwf_function('FDwfAnalogOutNodeOffsetInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'pMin'), (_OUT, POINTER(c_double), 'pMax'))
dwf_analog_out_node_offset_set = _dwf_function('FDwfAnalogOutNodeOffsetSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, c_double, 'vOffset'))
dwf_analog_out_node_offset_get = _dwf_function('FDwfAnalogOutNodeOffsetGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'pvOffset'))

dwf_analog_out_node_symmetry_info = _dwf_function('FDwfAnalogOutNodeSymmetryInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'ppercentageMin'), (_OUT, POINTER(c_double), 'ppercentageMax'))
dwf_analog_out_node_symmetry_set = _dwf_function('FDwfAnalogOutNodeSymmetrySet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, c_double, 'percentageSymmetry'))
dwf_analog_out_node_symmetry_get = _dwf_function('FDwfAnalogOutNodeSymmetryGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'ppercentageSymmetry'))

dwf_analog_out_node_phase_info = _dwf_function('FDwfAnalogOutNodePhaseInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'pdegreeMin'), (_OUT, POINTER(c_double), 'pdegreeMax'))
dwf_analog_out_node_phase_set = _dwf_function('FDwfAnalogOutNodePhaseSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, c_double, 'degreePhase'))
dwf_analog_out_node_phase_get = _dwf_function('FDwfAnalogOutNodePhaseGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_double), 'pdegreePhase'))

dwf_analog_out_node_data_info = _dwf_function('FDwfAnalogOutNodeDataInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_int), 'pnSamplesMin'), (_OUT, POINTER(c_int), 'pnSamplesMax'))
dwf_analog_out_node_data_set = _dwf_function('FDwfAnalogOutNodeDataSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, POINTER(c_double), 'rgdData'), (_IN, c_int, 'cdData'))

dwf_analog_out_custom_am_fm_enable_set = _dwf_function('FDwfAnalogOutCustomAMFMEnableSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'fEnable'))
dwf_analog_out_custom_am_fm_enable_get = _dwf_function('FDwfAnalogOutCustomAMFMEnableGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfEnable'))

# Control

dwf_analog_out_reset = _dwf_function('FDwfAnalogOutReset', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
dwf_analog_out_configure = _dwf_function('FDwfAnalogOutConfigure', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'fStart'))
dwf_analog_out_status = _dwf_function('FDwfAnalogOutStatus', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfState), 'psts'))
dwf_analog_out_node_play_status = _dwf_function('FDwfAnalogOutNodePlayStatus', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_OUT, POINTER(c_int), 'cdDataFree'), (_OUT, POINTER(c_int), 'cdDataLost'), (_OUT, POINTER(c_int), 'cdDataCorrupted'))
dwf_analog_out_node_play_data = _dwf_function('FDwfAnalogOutNodePlayData', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfAnalogOutNode, 'node'), (_IN, POINTER(c_double), 'rgdData'), (_IN, c_int, 'cdData'))

### ANALOG IO INSTRUMENT FUNCTIONS

# Control

dwf_analog_io_reset = _dwf_function('FDwfAnalogIOReset', (_IN, HDWF, 'hdwf'), )
dwf_analog_io_configure = _dwf_function('FDwfAnalogIOConfigure', (_IN, HDWF, 'hdwf'), )
dwf_analog_io_status = _dwf_function('FDwfAnalogIOStatus', (_IN, HDWF, 'hdwf'), )

# Configure

dwf_analog_io_enable_info = _dwf_function('FDwfAnalogIOEnableInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfSet'), (_OUT, POINTER(c_int), 'pfStatus'))
dwf_analog_io_enable_set = _dwf_function('FDwfAnalogIOEnableSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fMasterEnable'))
dwf_analog_io_enable_get = _dwf_function('FDwfAnalogIOEnableGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfMasterEnable'))
dwf_analog_io_enable_status = _dwf_function('FDwfAnalogIOEnableStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfMasterEnable'))
dwf_analog_io_channel_count = _dwf_function('FDwfAnalogIOChannelCount', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnChannel'))
dwf_analog_io_channel_name = _dwf_function('FDwfAnalogIOChannelName', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_char_p, 'szName'), (_IN, c_char_p, 'szLabel'))
dwf_analog_io_channel_info = _dwf_function('FDwfAnalogIOChannelInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pnNodes'))
dwf_analog_io_channel_node_name = _dwf_function('FDwfAnalogIOChannelNodeName', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxNode'), (_IN, c_char_p, 'szNodeName'), (_IN, c_char_p, 'szNodeUnits'))
dwf_analog_io_channel_node_info = _dwf_function('FDwfAnalogIOChannelNodeInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxNode'), (_OUT, POINTER(DwfAnalogIO), 'panalogio'))
dwf_analog_io_channel_node_set_info = _dwf_function('FDwfAnalogIOChannelNodeSetInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxNode'), (_OUT, POINTER(c_double), 'pmin'), (_OUT, POINTER(c_double), 'pmax'), (_OUT, POINTER(c_int), 'pnSteps'))
dwf_analog_io_channel_node_set = _dwf_function('FDwfAnalogIOChannelNodeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxNode'), (_IN, c_double, 'value'))
dwf_analog_io_channel_node_get = _dwf_function('FDwfAnalogIOChannelNodeGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxNode'), (_OUT, POINTER(c_double), 'pvalue'))
dwf_analog_io_channel_node_status_info = _dwf_function('FDwfAnalogIOChannelNodeStatusInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxNode'), (_OUT, POINTER(c_double), 'pmin'), (_OUT, POINTER(c_double), 'pmax'), (_OUT, POINTER(c_int), 'pnSteps'))
dwf_analog_io_channel_node_status = _dwf_function('FDwfAnalogIOChannelNodeStatus', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'idxNode'), (_OUT, POINTER(c_double), 'pvalue'))

### DIGITAL IO INSTRUMENT FUNCTIONS

# Control

dwf_digital_io_reset = _dwf_function('FDwfDigitalIOReset', (_IN, HDWF, 'hdwf'), )
dwf_digital_io_configure = _dwf_function('FDwfDigitalIOConfigure', (_IN, HDWF, 'hdwf'), )
dwf_digital_io_status = _dwf_function('FDwfDigitalIOStatus', (_IN, HDWF, 'hdwf'), )

# Configure

dwf_digital_io_output_enable_info = _dwf_function('FDwfDigitalIOOutputEnableInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsOutputEnableMask'))
dwf_digital_io_output_enable_set = _dwf_function('FDwfDigitalIOOutputEnableSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'fsOutputEnable'))
dwf_digital_io_output_enable_get = _dwf_function('FDwfDigitalIOOutputEnableGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsOutputEnable'))
dwf_digital_io_output_info = _dwf_function('FDwfDigitalIOOutputInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsOutputMask'))
dwf_digital_io_output_set = _dwf_function('FDwfDigitalIOOutputSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'fsOutput'))
dwf_digital_io_output_get = _dwf_function('FDwfDigitalIOOutputGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsOutput'))
if _version >= (3, 21, 0):
    dwf_digital_io_pull_info = _dwf_function('FDwfDigitalIOPullInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsUp'), (_OUT, POINTER(c_uint), 'pfsDown'))
    dwf_digital_io_pull_set = _dwf_function('FDwfDigitalIOPullSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'pfsUp'), (_IN, c_uint, 'pfsDown'))
    dwf_digital_io_pull_get = _dwf_function('FDwfDigitalIOPullGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsUp'), (_OUT, POINTER(c_uint), 'pfsDown'))
    dwf_digital_io_drive_info = _dwf_function('FDwfDigitalIODriveInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'channel'), (_OUT, POINTER(c_double), 'ampMin'), (_OUT, POINTER(c_double), 'ampMax'), (_OUT, POINTER(c_double), 'ampSteps'), (_OUT, POINTER(c_double), 'pslewSteps'))
    dwf_digital_io_drive_set = _dwf_function('FDwfDigitalIODriveSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'channel'), (_IN, c_double, 'amp'), (_IN, c_int, 'slew'))
    dwf_digital_io_drive_get = _dwf_function('FDwfDigitalIODriveGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'channel'), (_OUT, POINTER(c_double), 'pamp'), (_OUT, POINTER(c_int), 'pslew'))
dwf_digital_io_input_info = _dwf_function('FDwfDigitalIOInputInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsInputMask'))
dwf_digital_io_input_status = _dwf_function('FDwfDigitalIOInputStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsInput'))
dwf_digital_io_output_enable_info64 = _dwf_function('FDwfDigitalIOOutputEnableInfo64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsOutputEnableMask'))
dwf_digital_io_output_enable_set64 = _dwf_function('FDwfDigitalIOOutputEnableSet64', (_IN, HDWF, 'hdwf'), (_IN, c_ulonglong, 'fsOutputEnable'))
dwf_digital_io_output_enable_get64 = _dwf_function('FDwfDigitalIOOutputEnableGet64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsOutputEnable'))
dwf_digital_io_output_info64 = _dwf_function('FDwfDigitalIOOutputInfo64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsOutputMask'))
dwf_digital_io_output_set64 = _dwf_function('FDwfDigitalIOOutputSet64', (_IN, HDWF, 'hdwf'), (_IN, c_ulonglong, 'fsOutput'))
dwf_digital_io_output_get64 = _dwf_function('FDwfDigitalIOOutputGet64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsOutput'))
dwf_digital_io_input_info64 = _dwf_function('FDwfDigitalIOInputInfo64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsInputMask'))
dwf_digital_io_input_status64 = _dwf_function('FDwfDigitalIOInputStatus64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsInput'))

### DIGITAL _IN INSTRUMENT FUNCTIONS

# Control and status

dwf_digital_in_reset = _dwf_function('FDwfDigitalInReset', (_IN, HDWF, 'hdwf'), )
dwf_digital_in_configure = _dwf_function('FDwfDigitalInConfigure', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fReconfigure'), (_IN, c_int, 'fStart'))
dwf_digital_in_status = _dwf_function('FDwfDigitalInStatus', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fReadData'), (_OUT, POINTER(DwfState), 'psts'))
dwf_digital_in_status_samples_left = _dwf_function('FDwfDigitalInStatusSamplesLeft', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcSamplesLeft'))
dwf_digital_in_status_samples_valid = _dwf_function('FDwfDigitalInStatusSamplesValid', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcSamplesValid'))
dwf_digital_in_status_index_write = _dwf_function('FDwfDigitalInStatusIndexWrite', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pidxWrite'))
dwf_digital_in_status_auto_triggered = _dwf_function('FDwfDigitalInStatusAutoTriggered', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfAuto'))
dwf_digital_in_status_data = _dwf_function('FDwfDigitalInStatusData', (_IN, HDWF, 'hdwf'), (_IN, c_void_p, 'rgData'), (_IN, c_int, 'countOfDataBytes'))
dwf_digital_in_status_data2 = _dwf_function('FDwfDigitalInStatusData2', (_IN, HDWF, 'hdwf'), (_IN, c_void_p, 'rgData'), (_IN, c_int, 'idxSample'), (_IN, c_int, 'countOfDataBytes'))
if _version >= (3, 21, 0):
    dwf_digital_in_status_data3 = _dwf_function('FDwfDigitalInStatusData3', (_IN, HDWF, 'hdwf'), (_IN, c_void_p, 'rgData'), (_IN, c_int, 'idxSample'), (_IN, c_int, 'countOfDataBytes'), (_IN, c_int, 'bitShift'))
dwf_digital_in_status_noise2 = _dwf_function('FDwfDigitalInStatusNoise2', (_IN, HDWF, 'hdwf'), (_IN, c_void_p, 'rgData'), (_IN, c_int, 'idxSample'), (_IN, c_int, 'countOfDataBytes'))
if _version >= (3, 21, 0):
    dwf_digital_in_status_noise3 = _dwf_function('FDwfDigitalInStatusNoise3', (_IN, HDWF, 'hdwf'), (_IN, c_void_p, 'rgData'), (_IN, c_int, 'idxSample'), (_IN, c_int, 'countOfDataBytes'), (_IN, c_int, 'bitShift'))
dwf_digital_in_status_record = _dwf_function('FDwfDigitalInStatusRecord', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcdDataAvailable'), (_OUT, POINTER(c_int), 'pcdDataLost'), (_OUT, POINTER(c_int), 'pcdDataCorrupt'))
if _version >= (3, 21, 0):
    dwf_digital_in_status_compress = _dwf_function('FDwfDigitalInStatusCompress', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcdDataAvailable'), (_OUT, POINTER(c_int), 'pcdDataLost'), (_OUT, POINTER(c_int), 'pcdDataCorrupt'))
    dwf_digital_in_status_compressed = _dwf_function('FDwfDigitalInStatusCompressed', (_IN, HDWF, 'hdwf'), (_IN, c_void_p, 'rgData'), (_IN, c_int, 'countOfBytes'))
    dwf_digital_in_status_compressed2 = _dwf_function('FDwfDigitalInStatusCompressed2', (_IN, HDWF, 'hdwf'), (_IN, c_void_p, 'rgData'), (_IN, c_int, 'idxSample'), (_IN, c_int, 'countOfBytes'))
if _version >= (3, 16, 3):
    dwf_digital_in_status_time = _dwf_function('FDwfDigitalInStatusTime', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'psecUtc'), (_OUT, POINTER(c_uint), 'ptick'), (_OUT, POINTER(c_uint), 'pticksPerSecond'))

if _version >= (3, 18, 30):
    dwf_digital_in_counter_info = _dwf_function('FDwfDigitalInCounterInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pcntMax'), (_OUT, POINTER(c_double), 'psecMax'))
    dwf_digital_in_counter_set = _dwf_function('FDwfDigitalInCounterSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'sec'))
    dwf_digital_in_counter_get = _dwf_function('FDwfDigitalInCounterGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psec'))
    dwf_digital_in_counter_status = _dwf_function('FDwfDigitalInCounterStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pcnt'), (_OUT, POINTER(c_double), 'pfreq'), (_OUT, POINTER(c_int), 'ptick'))

# Acquisition configuration

dwf_digital_in_internal_clock_info = _dwf_function('FDwfDigitalInInternalClockInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'phzFreq'))

dwf_digital_in_clock_source_info = _dwf_function('FDwfDigitalInClockSourceInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfsDwfDigitalInClockSource'))
dwf_digital_in_clock_source_set = _dwf_function('FDwfDigitalInClockSourceSet', (_IN, HDWF, 'hdwf'), (_IN, DwfDigitalInClockSource, 'v'))
dwf_digital_in_clock_source_get = _dwf_function('FDwfDigitalInClockSourceGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfDigitalInClockSource), 'pv'))

dwf_digital_in_divider_info = _dwf_function('FDwfDigitalInDividerInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pdivMax'))
dwf_digital_in_divider_set = _dwf_function('FDwfDigitalInDividerSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'div'))
dwf_digital_in_divider_get = _dwf_function('FDwfDigitalInDividerGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pdiv'))

dwf_digital_in_bits_info = _dwf_function('FDwfDigitalInBitsInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnBits'))
dwf_digital_in_sample_format_set = _dwf_function('FDwfDigitalInSampleFormatSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'nBits'))
dwf_digital_in_sample_format_get = _dwf_function('FDwfDigitalInSampleFormatGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnBits'))

dwf_digital_in_input_order_set = _dwf_function('FDwfDigitalInInputOrderSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fDioFirst'))

dwf_digital_in_buffer_size_info = _dwf_function('FDwfDigitalInBufferSizeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnSizeMax'))
dwf_digital_in_buffer_size_set = _dwf_function('FDwfDigitalInBufferSizeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'nSize'))
dwf_digital_in_buffer_size_get = _dwf_function('FDwfDigitalInBufferSizeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pnSize'))

if _version >= (3, 21, 0):
    dwf_digital_in_buffers_info = _dwf_function('FDwfDigitalInBuffersInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pMax'))
    dwf_digital_in_buffers_set = _dwf_function('FDwfDigitalInBuffersSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'n'))
    dwf_digital_in_buffers_get = _dwf_function('FDwfDigitalInBuffersGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pn'))
    dwf_digital_in_buffers_status = _dwf_function('FDwfDigitalInBuffersStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pn'))

dwf_digital_in_sample_mode_info = _dwf_function('FDwfDigitalInSampleModeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfsDwfDigitalInSampleMode'))
dwf_digital_in_sample_mode_set = _dwf_function('FDwfDigitalInSampleModeSet', (_IN, HDWF, 'hdwf'), (_IN, DwfDigitalInSampleMode, 'v'))
dwf_digital_in_sample_mode_get = _dwf_function('FDwfDigitalInSampleModeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfDigitalInSampleMode), 'pv'))

dwf_digital_in_sample_sensible_set = _dwf_function('FDwfDigitalInSampleSensibleSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'fs'))
dwf_digital_in_sample_sensible_get = _dwf_function('FDwfDigitalInSampleSensibleGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfs'))

dwf_digital_in_acquisition_mode_info = _dwf_function('FDwfDigitalInAcquisitionModeInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfsacqmode'))
dwf_digital_in_acquisition_mode_set = _dwf_function('FDwfDigitalInAcquisitionModeSet', (_IN, HDWF, 'hdwf'), (_IN, DwfAcqMode, 'acqmode'))
dwf_digital_in_acquisition_mode_get = _dwf_function('FDwfDigitalInAcquisitionModeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfAcqMode), 'pacqmode'))

# Trigger configuration

dwf_digital_in_trigger_source_set = _dwf_function('FDwfDigitalInTriggerSourceSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTrigSrc, 'trigsrc'))
dwf_digital_in_trigger_source_get = _dwf_function('FDwfDigitalInTriggerSourceGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTrigSrc), 'ptrigsrc'))

dwf_digital_in_trigger_slope_set = _dwf_function('FDwfDigitalInTriggerSlopeSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTriggerSlope, 'slope'))
dwf_digital_in_trigger_slope_get = _dwf_function('FDwfDigitalInTriggerSlopeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTriggerSlope), 'pslope'))

dwf_digital_in_trigger_position_info = _dwf_function('FDwfDigitalInTriggerPositionInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pnSamplesAfterTriggerMax'))
dwf_digital_in_trigger_position_set = _dwf_function('FDwfDigitalInTriggerPositionSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'cSamplesAfterTrigger'))
dwf_digital_in_trigger_position_get = _dwf_function('FDwfDigitalInTriggerPositionGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pcSamplesAfterTrigger'))

dwf_digital_in_trigger_prefill_set = _dwf_function('FDwfDigitalInTriggerPrefillSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'cSamplesBeforeTrigger'))
dwf_digital_in_trigger_prefill_get = _dwf_function('FDwfDigitalInTriggerPrefillGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pcSamplesBeforeTrigger'))

dwf_digital_in_trigger_auto_timeout_info = _dwf_function('FDwfDigitalInTriggerAutoTimeoutInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'), (_OUT, POINTER(c_double), 'pnSteps'))
dwf_digital_in_trigger_auto_timeout_set = _dwf_function('FDwfDigitalInTriggerAutoTimeoutSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secTimeout'))
dwf_digital_in_trigger_auto_timeout_get = _dwf_function('FDwfDigitalInTriggerAutoTimeoutGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecTimeout'))

dwf_digital_in_trigger_info = _dwf_function('FDwfDigitalInTriggerInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsLevelLow'), (_OUT, POINTER(c_uint), 'pfsLevelHigh'), (_OUT, POINTER(c_uint), 'pfsEdgeRise'), (_OUT, POINTER(c_uint), 'pfsEdgeFall'))
dwf_digital_in_trigger_set = _dwf_function('FDwfDigitalInTriggerSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'fsLevelLow'), (_IN, c_uint, 'fsLevelHigh'), (_IN, c_uint, 'fsEdgeRise'), (_IN, c_uint, 'fsEdgeFall'))
dwf_digital_in_trigger_get = _dwf_function('FDwfDigitalInTriggerGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsLevelLow'), (_OUT, POINTER(c_uint), 'pfsLevelHigh'), (_OUT, POINTER(c_uint), 'pfsEdgeRise'), (_OUT, POINTER(c_uint), 'pfsEdgeFall'))

if _version >= (3, 21, 0):
    dwf_digital_in_trigger_info64 = _dwf_function('FDwfDigitalInTriggerInfo64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsLevelLow'), (_OUT, POINTER(c_ulonglong), 'pfsLevelHigh'), (_OUT, POINTER(c_ulonglong), 'pfsEdgeRise'), (_OUT, POINTER(c_ulonglong), 'pfsEdgeFall'))
    dwf_digital_in_trigger_set64 = _dwf_function('FDwfDigitalInTriggerSet64', (_IN, HDWF, 'hdwf'), (_IN, c_ulonglong, 'fsLevelLow'), (_IN, c_ulonglong, 'fsLevelHigh'), (_IN, c_ulonglong, 'fsEdgeRise'), (_IN, c_ulonglong, 'fsEdgeFall'))
    dwf_digital_in_trigger_get64 = _dwf_function('FDwfDigitalInTriggerGet64', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_ulonglong), 'pfsLevelLow'), (_OUT, POINTER(c_ulonglong), 'pfsLevelHigh'), (_OUT, POINTER(c_ulonglong), 'pfsEdgeRise'), (_OUT, POINTER(c_ulonglong), 'pfsEdgeFall'))

dwf_digital_in_trigger_reset_set = _dwf_function('FDwfDigitalInTriggerResetSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'fsLevelLow'), (_IN, c_uint, 'fsLevelHigh'), (_IN, c_uint, 'fsEdgeRise'), (_IN, c_uint, 'fsEdgeFall'))
if _version >= (3, 21, 0):
    dwf_digital_in_trigger_reset_set64 = _dwf_function('FDwfDigitalInTriggerResetSet64', (_IN, HDWF, 'hdwf'), (_IN, c_ulonglong, 'fsLevelLow'), (_IN, c_ulonglong, 'fsLevelHigh'), (_IN, c_ulonglong, 'fsEdgeRise'), (_IN, c_ulonglong, 'fsEdgeFall'))
dwf_digital_in_trigger_count_set = _dwf_function('FDwfDigitalInTriggerCountSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cCount'), (_IN, c_int, 'fRestart'))
dwf_digital_in_trigger_length_set = _dwf_function('FDwfDigitalInTriggerLengthSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secMin'), (_IN, c_double, 'secMax'), (_IN, c_int, 'idxSync'))
dwf_digital_in_trigger_match_set = _dwf_function('FDwfDigitalInTriggerMatchSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'iPin'), (_IN, c_uint, 'fsMask'), (_IN, c_uint, 'fsValue'), (_IN, c_int, 'cBitStuffing'))

### DIGITAL _OUT INSTRUMENT FUNCTIONS

# Control

dwf_digital_out_reset = _dwf_function('FDwfDigitalOutReset', (_IN, HDWF, 'hdwf'), )
dwf_digital_out_configure = _dwf_function('FDwfDigitalOutConfigure', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fStart'))
dwf_digital_out_status = _dwf_function('FDwfDigitalOutStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfState), 'psts'))
if _version >= (3, 18, 30):
    dwf_digital_out_status_output = _dwf_function('FDwfDigitalOutStatusOutput', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pfsValue'), (_OUT, POINTER(c_uint), 'pfsEnable'))

# Configuration

dwf_digital_out_internal_clock_info = _dwf_function('FDwfDigitalOutInternalClockInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'phzFreq'))

dwf_digital_out_trigger_source_set = _dwf_function('FDwfDigitalOutTriggerSourceSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTrigSrc, 'trigsrc'))
dwf_digital_out_trigger_source_get = _dwf_function('FDwfDigitalOutTriggerSourceGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTrigSrc), 'ptrigsrc'))

dwf_digital_out_run_info = _dwf_function('FDwfDigitalOutRunInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'))
dwf_digital_out_run_set = _dwf_function('FDwfDigitalOutRunSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secRun'))
dwf_digital_out_run_get = _dwf_function('FDwfDigitalOutRunGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecRun'))
dwf_digital_out_run_status = _dwf_function('FDwfDigitalOutRunStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecRun'))

dwf_digital_out_wait_info = _dwf_function('FDwfDigitalOutWaitInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecMin'), (_OUT, POINTER(c_double), 'psecMax'))
dwf_digital_out_wait_set = _dwf_function('FDwfDigitalOutWaitSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'secWait'))
dwf_digital_out_wait_get = _dwf_function('FDwfDigitalOutWaitGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'psecWait'))

dwf_digital_out_repeat_info = _dwf_function('FDwfDigitalOutRepeatInfo', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pnMin'), (_OUT, POINTER(c_uint), 'pnMax'))
dwf_digital_out_repeat_set = _dwf_function('FDwfDigitalOutRepeatSet', (_IN, HDWF, 'hdwf'), (_IN, c_uint, 'cRepeat'))
dwf_digital_out_repeat_get = _dwf_function('FDwfDigitalOutRepeatGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pcRepeat'))
dwf_digital_out_repeat_status = _dwf_function('FDwfDigitalOutRepeatStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_uint), 'pcRepeat'))

dwf_digital_out_trigger_slope_set = _dwf_function('FDwfDigitalOutTriggerSlopeSet', (_IN, HDWF, 'hdwf'), (_IN, DwfTriggerSlope, 'slope'))
dwf_digital_out_trigger_slope_get = _dwf_function('FDwfDigitalOutTriggerSlopeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfTriggerSlope), 'pslope'))

dwf_digital_out_repeat_trigger_set = _dwf_function('FDwfDigitalOutRepeatTriggerSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fRepeatTrigger'))
dwf_digital_out_repeat_trigger_get = _dwf_function('FDwfDigitalOutRepeatTriggerGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfRepeatTrigger'))

dwf_digital_out_count = _dwf_function('FDwfDigitalOutCount', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pcChannel'))
dwf_digital_out_enable_set = _dwf_function('FDwfDigitalOutEnableSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'fEnable'))
dwf_digital_out_enable_get = _dwf_function('FDwfDigitalOutEnableGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfEnable'))

dwf_digital_out_output_info = _dwf_function('FDwfDigitalOutOutputInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfsDwfDigitalOutOutput'))
dwf_digital_out_output_set = _dwf_function('FDwfDigitalOutOutputSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfDigitalOutOutput, 'v'))
dwf_digital_out_output_get = _dwf_function('FDwfDigitalOutOutputGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfDigitalOutOutput), 'pv'))

dwf_digital_out_type_info = _dwf_function('FDwfDigitalOutTypeInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfsDwfDigitalOutType'))
dwf_digital_out_type_set = _dwf_function('FDwfDigitalOutTypeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfDigitalOutType, 'v'))
dwf_digital_out_type_get = _dwf_function('FDwfDigitalOutTypeGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfDigitalOutType), 'pv'))

dwf_digital_out_idle_info = _dwf_function('FDwfDigitalOutIdleInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfsDwfDigitalOutIdle'))
dwf_digital_out_idle_set = _dwf_function('FDwfDigitalOutIdleSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, DwfDigitalOutIdle, 'v'))
dwf_digital_out_idle_get = _dwf_function('FDwfDigitalOutIdleGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(DwfDigitalOutIdle), 'pv'))

dwf_digital_out_divider_info = _dwf_function('FDwfDigitalOutDividerInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'vMin'), (_OUT, POINTER(c_uint), 'vMax'))
dwf_digital_out_divider_init_set = _dwf_function('FDwfDigitalOutDividerInitSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_uint, 'v'))
dwf_digital_out_divider_init_get = _dwf_function('FDwfDigitalOutDividerInitGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'pv'))
dwf_digital_out_divider_set = _dwf_function('FDwfDigitalOutDividerSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_uint, 'v'))
dwf_digital_out_divider_get = _dwf_function('FDwfDigitalOutDividerGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'pv'))

dwf_digital_out_counter_info = _dwf_function('FDwfDigitalOutCounterInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'vMin'), (_OUT, POINTER(c_uint), 'vMax'))
dwf_digital_out_counter_init_set = _dwf_function('FDwfDigitalOutCounterInitSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'fHigh'), (_IN, c_uint, 'v'))
dwf_digital_out_counter_init_get = _dwf_function('FDwfDigitalOutCounterInitGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pfHigh'), (_OUT, POINTER(c_uint), 'pv'))
dwf_digital_out_counter_set = _dwf_function('FDwfDigitalOutCounterSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_uint, 'vLow'), (_IN, c_uint, 'vHigh'))
dwf_digital_out_counter_get = _dwf_function('FDwfDigitalOutCounterGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'pvLow'), (_OUT, POINTER(c_uint), 'pvHigh'))

# ADP3X50

if _version >= (3, 18, 30):
    dwf_digital_out_repetition_info = _dwf_function('FDwfDigitalOutRepetitionInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'pnMax'))
    dwf_digital_out_repetition_set = _dwf_function('FDwfDigitalOutRepetitionSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_uint, 'cRepeat'))
    dwf_digital_out_repetition_get = _dwf_function('FDwfDigitalOutRepetitionGet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'pcRepeat'))

dwf_digital_out_data_info = _dwf_function('FDwfDigitalOutDataInfo', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_uint), 'pcountOfBitsMax'))
dwf_digital_out_data_set = _dwf_function('FDwfDigitalOutDataSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_void_p, 'rgBits'), (_IN, c_uint, 'countOfBits'))

if _version >= (3, 14, 3):
    dwf_digital_out_play_data_set = _dwf_function('FDwfDigitalOutPlayDataSet', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_ubyte), 'rgBits'), (_IN, c_uint, 'bitPerSample'), (_IN, c_uint, 'countOfSamples'))
    dwf_digital_out_play_rate_set = _dwf_function('FDwfDigitalOutPlayRateSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hzRate'))
if _version >= (3, 18, 30):
    dwf_digital_out_play_update_set = _dwf_function('FDwfDigitalOutPlayUpdateSet', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_ubyte), 'rgBits'), (_IN, c_uint, 'indexOfSample'), (_IN, c_uint, 'countOfSamples'))

# UART

dwf_digital_uart_reset = _dwf_function('FDwfDigitalUartReset', (_IN, HDWF, 'hdwf'), )
dwf_digital_uart_rate_set = _dwf_function('FDwfDigitalUartRateSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hz'))
dwf_digital_uart_bits_set = _dwf_function('FDwfDigitalUartBitsSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBits'))
dwf_digital_uart_parity_set = _dwf_function('FDwfDigitalUartParitySet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'parity'))
if _version >= (3, 17, 1):
    dwf_digital_uart_polarity_set = _dwf_function('FDwfDigitalUartPolaritySet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'polarity'))
dwf_digital_uart_stop_set = _dwf_function('FDwfDigitalUartStopSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'cBit'))
dwf_digital_uart_tx_set = _dwf_function('FDwfDigitalUartTxSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
dwf_digital_uart_rx_set = _dwf_function('FDwfDigitalUartRxSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))

dwf_digital_uart_tx = _dwf_function('FDwfDigitalUartTx', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_char), 'szTx'), (_IN, c_int, 'cTx'))
dwf_digital_uart_rx = _dwf_function('FDwfDigitalUartRx', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_char), 'szRx'), (_IN, c_int, 'cRx'), (_OUT, POINTER(c_int), 'pcRx'), (_OUT, POINTER(c_int), 'pParity'))

# SPI

dwf_digital_spi_reset = _dwf_function('FDwfDigitalSpiReset', (_IN, HDWF, 'hdwf'), )
dwf_digital_spi_frequency_set = _dwf_function('FDwfDigitalSpiFrequencySet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hz'))
dwf_digital_spi_clock_set = _dwf_function('FDwfDigitalSpiClockSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
dwf_digital_spi_data_set = _dwf_function('FDwfDigitalSpiDataSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxDQ'), (_IN, c_int, 'idxChannel'))
if _version >= (3, 14, 3):
    dwf_digital_spi_idle_set = _dwf_function('FDwfDigitalSpiIdleSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxDQ'), (_IN, DwfDigitalOutIdle, 'idle'))
dwf_digital_spi_mode_set = _dwf_function('FDwfDigitalSpiModeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'iMode'))
dwf_digital_spi_order_set = _dwf_function('FDwfDigitalSpiOrderSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fMSBFirst'))
if _version >= (3, 21, 0):
    dwf_digital_spi_delay_set = _dwf_function('FDwfDigitalSpiDelaySet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cStart'), (_IN, c_int, 'cCmd'), (_IN, c_int, 'cWord'), (_IN, c_int, 'cStop'))
    dwf_digital_spi_select_set = _dwf_function('FDwfDigitalSpiSelectSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxSelect'), (_IN, c_int, 'fIdle'))

dwf_digital_spi_select = _dwf_function('FDwfDigitalSpiSelect', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_IN, c_int, 'level'))
dwf_digital_spi_write_read = _dwf_function('FDwfDigitalSpiWriteRead', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ubyte), 'rgTX'), (_IN, c_int, 'cTX'), (_OUT, POINTER(c_ubyte), 'rgRX'), (_IN, c_int, 'cRX'))
dwf_digital_spi_write_read16 = _dwf_function('FDwfDigitalSpiWriteRead16', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ushort), 'rgTX'), (_IN, c_int, 'cTX'), (_OUT, POINTER(c_ushort), 'rgRX'), (_IN, c_int, 'cRX'))
dwf_digital_spi_write_read32 = _dwf_function('FDwfDigitalSpiWriteRead32', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_uint), 'rgTX'), (_IN, c_int, 'cTX'), (_OUT, POINTER(c_uint), 'rgRX'), (_IN, c_int, 'cRX'))
dwf_digital_spi_read = _dwf_function('FDwfDigitalSpiRead', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_ubyte), 'rgRX'), (_IN, c_int, 'cRX'))
dwf_digital_spi_read_one = _dwf_function('FDwfDigitalSpiReadOne', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_uint), 'pRX'))
dwf_digital_spi_read16 = _dwf_function('FDwfDigitalSpiRead16', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_ushort), 'rgRX'), (_IN, c_int, 'cRX'))
dwf_digital_spi_read32 = _dwf_function('FDwfDigitalSpiRead32', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_uint), 'rgRX'), (_IN, c_int, 'cRX'))
dwf_digital_spi_write = _dwf_function('FDwfDigitalSpiWrite', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ubyte), 'rgTX'), (_IN, c_int, 'cTX'))
dwf_digital_spi_write_one = _dwf_function('FDwfDigitalSpiWriteOne', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBits'), (_IN, c_uint, 'vTX'))
dwf_digital_spi_write16 = _dwf_function('FDwfDigitalSpiWrite16', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ushort), 'rgTX'), (_IN, c_int, 'cTX'))
dwf_digital_spi_write32 = _dwf_function('FDwfDigitalSpiWrite32', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_uint), 'rgTX'), (_IN, c_int, 'cTX'))

if _version >= (3, 21, 0):
    dwf_digital_spi_cmd_write_read = _dwf_function('FDwfDigitalSpiCmdWriteRead', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ubyte), 'rgTX'), (_IN, c_int, 'cTX'), (_OUT, POINTER(c_ubyte), 'rgRX'), (_IN, c_int, 'cRX'))
    dwf_digital_spi_cmd_write_read16 = _dwf_function('FDwfDigitalSpiCmdWriteRead16', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ushort), 'rgTX'), (_IN, c_int, 'cTX'), (_OUT, POINTER(c_ushort), 'rgRX'), (_IN, c_int, 'cRX'))
    dwf_digital_spi_cmd_write_read32 = _dwf_function('FDwfDigitalSpiCmdWriteRead32', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_uint), 'rgTX'), (_IN, c_int, 'cTX'), (_OUT, POINTER(c_uint), 'rgRX'), (_IN, c_int, 'cRX'))
    dwf_digital_spi_cmd_read = _dwf_function('FDwfDigitalSpiCmdRead', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_ubyte), 'rgRX'), (_IN, c_int, 'cRX'))
    dwf_digital_spi_cmd_read_one = _dwf_function('FDwfDigitalSpiCmdReadOne', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_uint), 'pRX'))
    dwf_digital_spi_cmd_read16 = _dwf_function('FDwfDigitalSpiCmdRead16', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_ushort), 'rgRX'), (_IN, c_int, 'cRX'))
    dwf_digital_spi_cmd_read32 = _dwf_function('FDwfDigitalSpiCmdRead32', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_OUT, POINTER(c_uint), 'rgRX'), (_IN, c_int, 'cRX'))
    dwf_digital_spi_cmd_write = _dwf_function('FDwfDigitalSpiCmdWrite', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ubyte), 'rgTX'), (_IN, c_int, 'cTX'))
    dwf_digital_spi_cmd_write_one = _dwf_function('FDwfDigitalSpiCmdWriteOne', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, c_uint, 'vTX'))
    dwf_digital_spi_cmd_write16 = _dwf_function('FDwfDigitalSpiCmdWrite16', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_ushort), 'rgTX'), (_IN, c_int, 'cTX'))
    dwf_digital_spi_cmd_write32 = _dwf_function('FDwfDigitalSpiCmdWrite32', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cBitCmd'), (_IN, c_uint, 'cmd'), (_IN, c_int, 'cDummy'), (_IN, c_int, 'cDQ'), (_IN, c_int, 'cBitPerWord'), (_IN, POINTER(c_uint), 'rgTX'), (_IN, c_int, 'cTX'))

# I2C

dwf_digital_i2c_reset = _dwf_function('FDwfDigitalI2cReset', (_IN, HDWF, 'hdwf'), )
dwf_digital_i2c_clear = _dwf_function('FDwfDigitalI2cClear', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pfFree'))
if _version >= (3, 10, 9):
    dwf_digital_i2c_stretch_set = _dwf_function('FDwfDigitalI2cStretchSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fEnable'))
dwf_digital_i2c_rate_set = _dwf_function('FDwfDigitalI2cRateSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hz'))
dwf_digital_i2c_read_nak_set = _dwf_function('FDwfDigitalI2cReadNakSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fNakLastReadByte'))
dwf_digital_i2c_scl_set = _dwf_function('FDwfDigitalI2cSclSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
dwf_digital_i2c_sda_set = _dwf_function('FDwfDigitalI2cSdaSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
if _version >= (3, 17, 1):
    dwf_digital_i2c_timeout_set = _dwf_function('FDwfDigitalI2cTimeoutSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'sec'))

dwf_digital_i2c_write_read = _dwf_function('FDwfDigitalI2cWriteRead', (_IN, HDWF, 'hdwf'), (_IN, c_ubyte, 'adr8bits'), (_IN, POINTER(c_ubyte), 'rgbTx'), (_IN, c_int, 'cTx'), (_IN, POINTER(c_ubyte), 'rgRx'), (_IN, c_int, 'cRx'), (_OUT, POINTER(c_int), 'pNak'))
dwf_digital_i2c_read = _dwf_function('FDwfDigitalI2cRead', (_IN, HDWF, 'hdwf'), (_IN, c_ubyte, 'adr8bits'), (_IN, POINTER(c_ubyte), 'rgbRx'), (_IN, c_int, 'cRx'), (_OUT, POINTER(c_int), 'pNak'))
dwf_digital_i2c_write = _dwf_function('FDwfDigitalI2cWrite', (_IN, HDWF, 'hdwf'), (_IN, c_ubyte, 'adr8bits'), (_IN, POINTER(c_ubyte), 'rgbTx'), (_IN, c_int, 'cTx'), (_OUT, POINTER(c_int), 'pNak'))
dwf_digital_i2c_write_one = _dwf_function('FDwfDigitalI2cWriteOne', (_IN, HDWF, 'hdwf'), (_IN, c_ubyte, 'adr8bits'), (_IN, c_ubyte, 'bTx'), (_OUT, POINTER(c_int), 'pNak'))

if _version >= (3, 18, 1):
    dwf_digital_i2c_spy_start = _dwf_function('FDwfDigitalI2cSpyStart', (_IN, HDWF, 'hdwf'), )
    dwf_digital_i2c_spy_status = _dwf_function('FDwfDigitalI2cSpyStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'fStart'), (_OUT, POINTER(c_int), 'fStop'), (_IN, POINTER(c_ubyte), 'rgData'), (_OUT, POINTER(c_int), 'cData'), (_OUT, POINTER(c_int), 'iNak'))

# CAN

dwf_digital_can_reset = _dwf_function('FDwfDigitalCanReset', (_IN, HDWF, 'hdwf'), )
dwf_digital_can_rate_set = _dwf_function('FDwfDigitalCanRateSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hz'))
dwf_digital_can_polarity_set = _dwf_function('FDwfDigitalCanPolaritySet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fHigh'))
dwf_digital_can_tx_set = _dwf_function('FDwfDigitalCanTxSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
dwf_digital_can_rx_set = _dwf_function('FDwfDigitalCanRxSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))

dwf_digital_can_tx = _dwf_function('FDwfDigitalCanTx', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'vID'), (_IN, c_int, 'fExtended'), (_IN, c_int, 'fRemote'), (_IN, c_int, 'cDLC'), (_IN, POINTER(c_ubyte), 'rgTX'))
dwf_digital_can_rx = _dwf_function('FDwfDigitalCanRx', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'pvID'), (_OUT, POINTER(c_int), 'pfExtended'), (_OUT, POINTER(c_int), 'pfRemote'), (_OUT, POINTER(c_int), 'pcDLC'), (_IN, POINTER(c_ubyte), 'rgRX'), (_IN, c_int, 'cRX'), (_OUT, POINTER(c_int), 'pvStatus'))

# SWD

if _version >= (3, 21, 0):
    dwf_digital_swd_reset = _dwf_function('FDwfDigitalSwdReset', (_IN, HDWF, 'hdwf'), )
    dwf_digital_swd_rate_set = _dwf_function('FDwfDigitalSwdRateSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hz'))
    dwf_digital_swd_ck_set = _dwf_function('FDwfDigitalSwdCkSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
    dwf_digital_swd_io_set = _dwf_function('FDwfDigitalSwdIoSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'))
    dwf_digital_swd_turn_set = _dwf_function('FDwfDigitalSwdTurnSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cTurn'))
    dwf_digital_swd_trail_set = _dwf_function('FDwfDigitalSwdTrailSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cTrail'))
    dwf_digital_swd_park_set = _dwf_function('FDwfDigitalSwdParkSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fDrive'))
    dwf_digital_swd_nak_set = _dwf_function('FDwfDigitalSwdNakSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fContinue'))
    dwf_digital_swd_io_idle_set = _dwf_function('FDwfDigitalSwdIoIdleSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fHigh'))
    dwf_digital_swd_clear = _dwf_function('FDwfDigitalSwdClear', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cReset'), (_IN, c_int, 'cTrail'))
    dwf_digital_swd_write = _dwf_function('FDwfDigitalSwdWrite', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'APnDP'), (_IN, c_int, 'A32'), (_OUT, POINTER(c_int), 'pAck'), (_IN, c_uint, 'Write'))
    dwf_digital_swd_read = _dwf_function('FDwfDigitalSwdRead', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'APnDP'), (_IN, c_int, 'A32'), (_OUT, POINTER(c_int), 'pAck'), (_OUT, POINTER(c_uint), 'pRead'), (_OUT, POINTER(c_int), 'pCrc'))

# Impedance

if _version >= (3, 9, 1):
    dwf_analog_impedance_reset = _dwf_function('FDwfAnalogImpedanceReset', (_IN, HDWF, 'hdwf'), )
    dwf_analog_impedance_mode_set = _dwf_function('FDwfAnalogImpedanceModeSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'mode'))
    dwf_analog_impedance_mode_get = _dwf_function('FDwfAnalogImpedanceModeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'mode'))
    dwf_analog_impedance_reference_set = _dwf_function('FDwfAnalogImpedanceReferenceSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'ohms'))
    dwf_analog_impedance_reference_get = _dwf_function('FDwfAnalogImpedanceReferenceGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pohms'))
    dwf_analog_impedance_frequency_set = _dwf_function('FDwfAnalogImpedanceFrequencySet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'hz'))
    dwf_analog_impedance_frequency_get = _dwf_function('FDwfAnalogImpedanceFrequencyGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'phz'))
    dwf_analog_impedance_amplitude_set = _dwf_function('FDwfAnalogImpedanceAmplitudeSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'volts'))
    dwf_analog_impedance_amplitude_get = _dwf_function('FDwfAnalogImpedanceAmplitudeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvolts'))
    dwf_analog_impedance_offset_set = _dwf_function('FDwfAnalogImpedanceOffsetSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'volts'))
    dwf_analog_impedance_offset_get = _dwf_function('FDwfAnalogImpedanceOffsetGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pvolts'))
    dwf_analog_impedance_probe_set = _dwf_function('FDwfAnalogImpedanceProbeSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'ohmRes'), (_IN, c_double, 'faradCap'))
    dwf_analog_impedance_probe_get = _dwf_function('FDwfAnalogImpedanceProbeGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pohmRes'), (_OUT, POINTER(c_double), 'pfaradCap'))
    dwf_analog_impedance_period_set = _dwf_function('FDwfAnalogImpedancePeriodSet', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cMinPeriods'))
    dwf_analog_impedance_period_get = _dwf_function('FDwfAnalogImpedancePeriodGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_int), 'cMinPeriods'))
    dwf_analog_impedance_comp_reset = _dwf_function('FDwfAnalogImpedanceCompReset', (_IN, HDWF, 'hdwf'), )
    dwf_analog_impedance_comp_set = _dwf_function('FDwfAnalogImpedanceCompSet', (_IN, HDWF, 'hdwf'), (_IN, c_double, 'ohmOpenResistance'), (_IN, c_double, 'ohmOpenReactance'), (_IN, c_double, 'ohmShortResistance'), (_IN, c_double, 'ohmShortReactance'))
    dwf_analog_impedance_comp_get = _dwf_function('FDwfAnalogImpedanceCompGet', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(c_double), 'pohmOpenResistance'), (_OUT, POINTER(c_double), 'pohmOpenReactance'), (_OUT, POINTER(c_double), 'pohmShortResistance'), (_OUT, POINTER(c_double), 'pohmShortReactance'))
    dwf_analog_impedance_configure = _dwf_function('FDwfAnalogImpedanceConfigure', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'fStart'))
    dwf_analog_impedance_status = _dwf_function('FDwfAnalogImpedanceStatus', (_IN, HDWF, 'hdwf'), (_OUT, POINTER(DwfState), 'psts'))
    dwf_analog_impedance_status_input = _dwf_function('FDwfAnalogImpedanceStatusInput', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_double), 'pgain'), (_OUT, POINTER(c_double), 'pradian'))
    dwf_analog_impedance_status_measure = _dwf_function('FDwfAnalogImpedanceStatusMeasure', (_IN, HDWF, 'hdwf'), (_IN, DwfAnalogImpedance, 'measure'), (_OUT, POINTER(c_double), 'pvalue'))
if _version >= (3, 17, 1):
    dwf_analog_impedance_status_warning = _dwf_function('FDwfAnalogImpedanceStatusWarning', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'idxChannel'), (_OUT, POINTER(c_int), 'pWarning'))

if _version >= (3, 18, 30):
    dwf_spectrum_window = _dwf_function('FDwfSpectrumWindow', (_IN, HDWF, 'hdwf'), (_IN, c_int, 'cdWin'), (_IN, DwfWindow, 'iWindow'), (_IN, c_double, 'vBeta'), (_OUT, POINTER(c_double), 'vNEBW'))
    dwf_spectrum_fft = _dwf_function('FDwfSpectrumFFT', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_double), 'rgdData'), (_IN, c_int, 'cdData'), (_IN, POINTER(c_double), 'rgdBin'), (_IN, POINTER(c_double), 'rgdPhase'), (_IN, c_int, 'cdBin'))
    dwf_spectrum_transform = _dwf_function('FDwfSpectrumTransform', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_double), 'rgdData'), (_IN, c_int, 'cdData'), (_IN, POINTER(c_double), 'rgdBin'), (_IN, POINTER(c_double), 'rgdPhase'), (_IN, c_int, 'cdBin'), (_IN, c_double, 'iFirst'), (_IN, c_double, 'iLast'))
if _version >= (3, 21, 0):
    dwf_spectrum_goertzel = _dwf_function('FDwfSpectrumGoertzel', (_IN, HDWF, 'hdwf'), (_IN, POINTER(c_double), 'rgdData'), (_IN, c_int, 'cdData'), (_IN, c_double, 'pos'), (_IN, POINTER(c_double), 'pMag'), (_IN, c_double, 'pRad'))
