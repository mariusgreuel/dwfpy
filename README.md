# Python Bindings for Digilent WaveForms API

The **dwfpy** package allows you to access **Digilent WaveForms** devices via Python.

Supported devices include all [WaveForms][WaveForms] devices, such as the **Analog Discovery 2** or the **Digital Discovery**.

The source code for the **dwfpy** package can be found at GitHub at <https://github.com/mariusgreuel/dwfpy>.

## Features

- Pythonic abstraction of Digilent Waveforms devices.
- Low-level API with complete access to the DWF API.
- High-level API that supports one-line configuration statements.

One of the design goals is to provide users with a simple high-level API that allows one to perform common tasks quickly,
while hiding some of the complexity of the WaveForms API.

For instance, to output a sine-wave on a **Analog Discovery 2**, you can simply write:

```python
import dwfpy as dwf

with dwf.AnalogDiscovery2() as device:
    print('Generating a 1kHz sine wave on WaveGen channel 1...')
    device.analog_output['ch1'].setup('sine', frequency=1e3, amplitude=1, start=True)
    input('Press Enter key to exit.')
```

## Installing dwfpy

You can install the [dwfpy package](https://pypi.org/project/dwfpy/) from PyPI using pip:

```console
pip install dwfpy
```

In order to use the **dwfpy** package, you need **Python 3.6** or higher.

As **dwfpy** builds on top of the WaveForms API, you need to install the [WaveForms software][WaveForms-Software],
which includes the required runtime components to access the WaveForms devices.

## Documentation

You can find the **dwfpy** user's guide at <https://dwfpy.readthedocs.io/>.

Detailed information about the Digilent Waveforms API is available
from the [Digilent WaveForms SDK Reference Manual][WaveForms-SDK-Reference-Manual].

## Examples

You can find examples using **dwfpy** in the dwfpy GitHub repository at
<https://github.com/mariusgreuel/dwfpy/tree/main/examples>.

## Getting help

For issues with **dwfpy**, please visit the
[dwfpy issue tracker](https://github.com/mariusgreuel/dwfpy/issues).

[WaveForms]: https://digilent.com/shop/software/digilent-waveforms/
[WaveForms-Software]: https://digilent.com/reference/software/waveforms/waveforms-3/start
[WaveForms-SDK-Reference-Manual]: https://digilent.com/reference/_media/waveforms_sdk_reference_manual.pdf
