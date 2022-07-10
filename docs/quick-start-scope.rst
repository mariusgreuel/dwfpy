.. include:: common.rst

Using the Oscilloscope
======================

If your device has an oscilloscope, you can access it via the property :py:meth:`analog_input <dwfpy.device.Device.analog_input>`.
Individual channels can be accessed via a zero-based index, or a label, such as 'ch1'.

There are various high-level functions that you can use to control the oscilloscope:

**Channel Setup**

- :py:meth:`analog_input[ch].setup() <dwfpy.analog_input.AnalogInput.Channel.setup>` - Sets up the channel for data acquisition.

**Data Acquisition**

- :py:meth:`analog_input[ch].get_sample() <dwfpy.analog_input.AnalogInput.Channel.get_sample>` - Gets the last ADC conversion sample.
- :py:meth:`analog_input.single() <dwfpy.analog_input.AnalogInput.single>` - Starts a single data acquisition.
- :py:meth:`analog_input.record() <dwfpy.analog_input.AnalogInput.record>` - Starts a data recording.

**Triggering**

- :py:meth:`analog_input.setup_edge_trigger() <dwfpy.analog_input.AnalogInput.setup_edge_trigger>` - Trigger upon a certain voltage level in the positive or negative slope of the waveform.
- :py:meth:`analog_input.setup_pulse_trigger() <dwfpy.analog_input.AnalogInput.setup_pulse_trigger>` - Trigger upon a positive or negative pulse width when measured at a certain voltage level.
- :py:meth:`analog_input.setup_transition_trigger() <dwfpy.analog_input.AnalogInput.setup_transition_trigger>` - Sets up a transition trigger.
- :py:meth:`analog_input.setup_window_trigger() <dwfpy.analog_input.AnalogInput.setup_window_trigger>` - Trigger upon a signal entering or exiting a window at certain voltage thresholds.

Setting Up Channels
-------------------

You can use the :py:meth:`analog_input[ch].setup() <dwfpy.analog_input.AnalogInput.Channel.setup>` function
on a respective analog input channel to setup a channel.
You can specify the channel voltage range, offset voltage, and more.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       scope = device.analog_input
       scope[0].setup(range=5.0, offset=2.0)

Getting the Current ADC Sample
------------------------------

You can use the :py:meth:`analog_input[ch].get_sample() <dwfpy.analog_input.AnalogInput.Channel.get_sample>` function
on a respective analog input channel to get the current ADC reading.

.. note::
   You need to call the :py:meth:`analog_input.read_status() <dwfpy.analog_input.AnalogInput.read_status>` function
   before calling ``get_sample()`` to read a sample from the device.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       scope = device.analog_input
       scope[0].setup(range=50.0)
       scope.configure()
       scope.read_status()
       print(f'CH1: {scope[0].get_sample()}V')

For a complete example, see
`examples/analog_in_sample.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/analog_in_sample.py>`_.

Single Data Acquisition
-----------------------

You can use the :py:meth:`single() <dwfpy.analog_input.AnalogInput.single>` function
on the analog input unit to perform a single-shot data acquisition.
To configure the oscilloscope, pass the parameter ``configure=True``.
To start the acquisition immediately and wait for the acquisition to finish, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       scope = device.analog_input
       scope[0].setup(range=5.0)
       scope.single(sample_rate=1e6, buffer_size=4096, configure=True, start=True)
       samples = scope[0].get_data()
       print(samples)

For a complete example, see
`examples/analog_in_single.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/analog_in_single.py>`_.

Recording Samples
-----------------

You can use the :py:meth:`record() <dwfpy.analog_input.AnalogInput.record>` function on the analog input unit to perform data recording.
To configure the oscilloscope, pass the parameter ``configure=True``.
To start the acquisition immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       scope = device.analog_input
       scope[0].setup(range=5.0)
       recorder = scope.record(sample_rate=1e6, sample_count=1e6, configure=True, start=True)
       samples = recorder.channels[0].data_samples
       print(samples)

For a complete example, see
`examples/analog_in_record.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/analog_in_record.py>`_.

Setting Up an Edge Trigger
--------------------------

You can use the :py:meth:`setup_edge_trigger() <dwfpy.analog_input.AnalogInput.setup_edge_trigger>` function
to trigger the oscilloscope on a positive or negative slope of the waveform.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       scope[0].setup(range=5.0)
       scope.setup_edge_trigger(mode='normal', channel=0, slope='rising', level=0.5, hysteresis=0.01)
       scope.single(sample_rate=1e6, buffer_size=4096, configure=True, start=True)
       samples = scope[0].get_data()

For a complete example, see
`examples/analog_in_single.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/analog_in_single.py>`_.
