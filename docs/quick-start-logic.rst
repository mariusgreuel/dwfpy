.. include:: common.rst

Using the Logic Analyzer
========================

If your device has a logic analyzer, you can access it via the property :py:meth:`digital_input <dwfpy.device.Device.digital_input>`.
Individual channels can be accessed via a zero-based index, or a label, such as 'ch1'.

There are various high-level functions that you can use to control the logic analyzer:

**Acquisition**

- :py:meth:`digital_input.single() <dwfpy.digital_input.DigitalInput.single>` - Starts a single data acquisition.
- :py:meth:`digital_input.record() <dwfpy.digital_input.DigitalInput.record>` - Starts a data recording.

**Triggering**

- :py:meth:`digital_input.setup_trigger() <dwfpy.digital_input.DigitalInput.setup_trigger>` - Sets up the trigger condition.
- :py:meth:`digital_input.setup_edge_trigger() <dwfpy.digital_input.DigitalInput.setup_edge_trigger>` - Sets up an edge trigger.
- :py:meth:`digital_input.setup_level_trigger() <dwfpy.digital_input.DigitalInput.setup_level_trigger>` - Sets up a level trigger.
- :py:meth:`digital_input.setup_glitch_trigger() <dwfpy.digital_input.DigitalInput.setup_glitch_trigger>` - Sets up a glitch trigger.
- :py:meth:`digital_input.setup_timeout_trigger() <dwfpy.digital_input.DigitalInput.setup_timeout_trigger>` - Sets up a timeout trigger.
- :py:meth:`digital_input.setup_more_trigger() <dwfpy.digital_input.DigitalInput.setup_more_trigger>` - Sets up a more trigger.
- :py:meth:`digital_input.setup_length_trigger() <dwfpy.digital_input.DigitalInput.setup_length_trigger>` - Sets up a length trigger.
- :py:meth:`digital_input.setup_counter_trigger() <dwfpy.digital_input.DigitalInput.setup_counter_trigger>` - Sets up a counter trigger.

**Channel specific Triggering**

- :py:meth:`digital_input[ch].setup_trigger() <dwfpy.digital_input.DigitalInput.Channel.setup_trigger>` - Sets up the trigger condition for this channel.
- :py:meth:`digital_input[ch].setup_reset_trigger() <dwfpy.digital_input.DigitalInput.Channel.setup_reset_trigger>` - Sets up the trigger reset condition for this channel.

Single Data Acquisition
-----------------------

You can use the :py:meth:`single() <dwfpy.digital_input.DigitalInput.single>` function
on the digital input unit to perform a single-shot data acquisition.
To configure the logic analyzer, pass the parameter ``configure=True``.
To start the acquisition immediately and wait for the acquisition to finish, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       logic = device.digital_input
       samples = logic.single(sample_rate=1e6, buffer_size=4096, configure=True, start=True)
       print(samples)

For a complete example, see
`examples/digital_in_acquisition.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/digital_in_acquisition.py>`_.

Recording Samples
-----------------

You can use the :py:meth:`record() <dwfpy.digital_input.DigitalInput.record>` function
on the digital input unit to perform data recording.
To configure the logic analyzer, pass the parameter ``configure=True``.
To start the acquisition immediately, pass the parameter ``start=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       logic = device.digital_input
       recorder = logic.record(sample_rate=1e6, sample_count=1e6, configure=True, start=True)
       samples = recorder.data_samples
       print(samples)

For a complete example, see
`examples/digital_in_record.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/digital_in_record.py>`_.

For an examples that uses data compression, see
`examples/digital_in_record_compress.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/digital_in_record_compress.py>`_.
