.. include:: common.rst

Using the Pattern Generator
===========================

If your device has a pattern generator, you can access it via the property :py:meth:`digital_output <dwfpy.device.Device.digital_output>`.
Individual channels can be accessed via a zero-based index, or a label, such as 'ch1'.

There are various functions that you can use to configure pins:

- :py:meth:`digital_output[ch].setup_constant() <dwfpy.digital_output.DigitalOutput.Channel.setup_constant>` - Sets up the channel as a constant output.
- :py:meth:`digital_output[ch].setup_clock() <dwfpy.digital_output.DigitalOutput.Channel.setup_clock>` - Sets up the channel as a clock output.
- :py:meth:`digital_output[ch].setup_pulse() <dwfpy.digital_output.DigitalOutput.Channel.setup_pulse>` - Sets up the channel as a pulse output.
- :py:meth:`digital_output[ch].setup_random() <dwfpy.digital_output.DigitalOutput.Channel.setup_random>` - Sets up the channel as a random output.
- :py:meth:`digital_output[ch].setup_custom() <dwfpy.digital_output.DigitalOutput.Channel.setup_constant>` - Sets up the channel with a custom output.

All setup function allow you to speficy the output mode ('push-pull', 'open-drain', 'open-source', or 'three-state') and the idle state ('init', 'low', 'high', or 'z').

Setting up a Constant Output
----------------------------

You can use the :py:meth:`setup_constant() <dwfpy.digital_output.DigitalOutput.Channel.setup_constant>` function
to drive a channel with a constant output value.
To start the channel immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       pattern = device.digital_output
       # Output a high level on pin DIO-0.
       pattern[0].setup_constant(value=True, start=True)

Setting up a Clock Signal
-------------------------

You can use the :py:meth:`setup_clock() <dwfpy.digital_output.DigitalOutput.Channel.setup_clock>` function
to output a clock or PWM signal.
You can specify the frequency, duty_cycle, phase, delay, and repetition count.
By default, the channel is enabled via the parameter ``enabled=True``.
To start the channel immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       pattern = device.digital_output
       # Output a 1kHz clock on pin DIO-0.
       pattern[0].setup_clock(frequency=1e3, start=True)

For a complete example, see
`examples/digital_out_clock.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/digital_out_clock.py>`_.

Setting up a Random Signal
--------------------------

You can use the :py:meth:`setup_random() <dwfpy.digital_output.DigitalOutput.Channel.setup_random>` function to output a clock or PWM signal.
You can specify the rate, delay, and repetition count.
By default, the channel is enabled via the parameter ``enabled=True``.
To start the channel immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       pattern = device.digital_output
       # Output a random pattern at a 1kHz rate on pin DIO-0.
       pattern[0].setup_random(rate=1e3, start=True)

For a complete example, see
`examples/digital_out_pins.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/digital_out_pins.py>`_.
