# Python Bindings for Digilent WaveForms API

![build](https://github.com/mariusgreuel/dwfpy/actions/workflows/build.yml/badge.svg)
![docs](https://readthedocs.org/projects/dwfpy/badge/?version=latest)

**DwfPy** is a Python package that allows you to access **Digilent WaveForms** devices via Python. It provides a low-level API with complete access to the Digilent WaveForms API, and also a simple but powerful high-level API, which allows you to configure WaveForms devices with a single statement.

For instance, to output a 1kHz sine-wave on an **Analog Discovery**, you can simply write:

```python
import dwfpy as dwf

with dwf.Device() as device:
    print('Generating a 1kHz sine wave on WaveGen channel 1...')
    device.analog_output['ch1'].setup('sine', frequency=1e3, amplitude=1, start=True)
    input('Press Enter key to exit.')
```

## Features

- Pythonic abstraction of Digilent Waveforms API.
- Low-level API with complete access to the Digilent Waveforms API.
- Powerful high-level API that supports one-line configuration statements.
- Supports all sub-modules, such as oscilloscope, arbitrary waveform generator, logic analyzer, pattern generator, digital I/O, and power supplies.
- Works with all WaveForms devices, such as the **Analog Discovery 2**, the **Analog Discovery 3**, or the **Digital Discovery**.

## Installing DwfPy

You can install the [DwfPy package](https://pypi.org/project/dwfpy/) from PyPI using pip:

```console
pip install dwfpy
```

In order to use the **DwfPy** package, you need **Python 3.8** or higher.

As **DwfPy** builds on top of the WaveForms API, you need to install the [WaveForms software][WaveForms-Software], which includes the required runtime components to access the WaveForms devices.

The source code for the **DwfPy** package can be found at GitHub at <https://github.com/mariusgreuel/dwfpy>.

## Examples

You can find Python examples using **DwfPy** in the dwfpy GitHub repository at <https://github.com/mariusgreuel/dwfpy/tree/main/examples>.

## Documentation

You can find the **DwfPy** user's guide at <https://dwfpy.readthedocs.io/>.

Detailed information about the Digilent Waveforms API is available from the [Digilent WaveForms SDK Reference Manual][WaveForms-SDK-Reference-Manual].

## Getting help

For issues with **DwfPy**, please visit the
[dwfpy issue tracker](https://github.com/mariusgreuel/dwfpy/issues).

[WaveForms]: https://digilent.com/shop/software/digilent-waveforms/
[WaveForms-Software]: https://digilent.com/reference/software/waveforms/waveforms-3/start
[WaveForms-SDK-Reference-Manual]: https://digilent.com/reference/_media/waveforms_sdk_reference_manual.pdf
