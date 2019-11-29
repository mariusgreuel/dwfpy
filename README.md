# Digilent WaveForms for Python

The `dwfpy` Python package can be used to access **Digilent WaveForms** devices, such as the **Analog Discovery 2** or the **Digital Discovery**.

The goal of this package is to provide users with a simple, yet powerful way of controlling Digilent WaveForms devices.

## Features

- Pythonic abstraction of Digilent Waveforms devices.
- Low-level API with complete access to the DWF API.
- High-level API that supports one-line configuration statements.

## Example

For instance, to configure the Arbitrary Waveform Generator of an Analog Discovery 2, you can write:

```python
import dwfpy as dwf

with dwf.AnalogDiscovery2() as device:
    print('Generating a 1kHz sine wave on WaveGen channel 1...')
    device.analog_output['ch1'].setup('sine', frequency=1e3, amplitude=1, start=True)
    input('Press Enter key to exit.')
```

## Installing dwfpy

You can install the [dwfpy](https://pypi.org/project/dwfpy/) package from [PyPI](https://pypi.org/) via pip:

```console
pip install dwfpy
```

In order to use the `dwfpy` package, you need **Python 3.6** or higher.

The source code for the `dwfpy` package can be found at GitHub at <https://github.com/mariusgreuel/dwfpy>.

## Getting help

As of now, there is no users manual for `dwfpy`. You are encouraged to study the source code, and use your editors code completion features to browse the dwfpy functions and properties.

Detailed information about the Digilent Waveforms devices is available from the [Digilent WaveForms SDK Reference Manual][WaveForms-SDK-Reference-Manual].

[WaveForms-SDK-Reference-Manual]: https://digilent.com/reference/_media/waveforms_sdk_reference_manual.pdf
