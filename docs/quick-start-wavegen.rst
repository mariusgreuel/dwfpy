.. include:: common.rst

Using the Waveform Generator
============================

If your device has an arbitrary waveform generator, you can access it via the property :py:meth:`analog_output <dwfpy.device.Device.analog_output>`.
Individual channels can be accessed via a zero-based index, or a label, such as 'ch1'.

There are various high-level functions that you can use to control the waveform generator:

**Channel Setup**

- :py:meth:`analog_output[ch].setup() <dwfpy.analog_output.AnalogOutput.Channel.setup>` - Sets up a new carrier waveform.
- :py:meth:`analog_output[ch].setup_am() <dwfpy.analog_output.AnalogOutput.Channel.setup_am>` - Applies an AM modulation to a waveform.
- :py:meth:`analog_output[ch].setup_fm() <dwfpy.analog_output.AnalogOutput.Channel.setup_fm>` - Applies an FM modulation to a waveform (sweep).

Setting up a new Waveform
-------------------------

You can use the :py:meth:`setup() <dwfpy.analog_output.AnalogOutput.Channel.setup>` function to create a new waveform.
You can specify the generator function, frequency, amplitude, offset, symmetry, and phase.
By default, the carrier node is enabled via the parameter ``enabled=True``.
To start the channel immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       wavegen = device.analog_output
       wavegen[0].setup(function='sine', frequency=1e3, amplitude=1.0, start=True)

For a complete example, see
`examples/analog_out_sine.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/analog_out_sine.py>`_.

Setting up an Amplitude Modulation
----------------------------------

You can use the :py:meth:`setup_am() <dwfpy.analog_output.AnalogOutput.Channel.setup_am>` function to modulate the amplitude.
You can specify the generator function, frequency, amplitude, offset, symmetry, and phase, similar to the ``setup()`` function.
By default, the AM node is enabled via the parameter ``enabled=True``.
To start the channel immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       wavegen = device.analog_output
       wavegen[0].setup(function='sine', frequency=1e3, amplitude=1.0)
       wavegen[0].setup_am(function='triangle', frequency=10, amplitude=50, start=True)

Setting up a Frequency Modulation
---------------------------------

You can use the :py:meth:`setup_fm() <dwfpy.analog_output.AnalogOutput.Channel.setup_fm>` function to modulate the frequency.
You can specify the generator function, frequency, amplitude, offset, symmetry, and phase, similar to the ``setup()`` function.
By default, the FM node is enabled via the parameter ``enabled=True``.
To start the channel immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       wavegen = device.analog_output
       wavegen[0].setup(function='sine', frequency=1e3, amplitude=1.0)
       wavegen[0].setup_fm(function='sine', frequency=10, amplitude=10, start=True)

Generating a Custom Waveform
----------------------------

You can use the :py:meth:`setup() <dwfpy.analog_output.AnalogOutput.Channel.setup>` function to create a custom waveform.
Use the function 'custom' and the parameter ``data_samples`` to pass the samples to be generated.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       wavegen = device.analog_output

       # Create 256 samples of a sine waveform from 0 to 2*pi/4 (90 degrees).
       waveform = [math.sin(i * 2 * math.pi / 256 / 4) for i in range(0, 256)]
       wavegen[0].setup("custom", frequency=1e3, amplitude=1, data_samples=waveform, start=True)

For a complete example, see
`examples/analog_out_custom.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/analog_out_custom.py>`_.
