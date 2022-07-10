.. include:: common.rst

Using the Digital I/O
=====================

If your device has Digital I/O, you can access it via the property :py:meth:`digital_io <dwfpy.device.Device.digital_io>`.
Individual channels can be accessed via a zero-based index, or a label, such as 'dio0', 'dio1', etc.

Reading from Inputs
-------------------

By default, pins are configured as inputs.

.. note::
   You need to call the :py:meth:`digital_io.read_status() <dwfpy.digital_io.DigitalIo.read_status>` function
   before reading from ``input_state`` to read all input states from the device.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       io = device.digital_io
       # Configure DIO-0 as input
       io[0].setup(enabled=False, configure=True)
       # Read all I/O pins
       io.read_status()
       dio0 = io[1].input_state
       print(f'DIO-0={dio0}')

Writing to Outputs
------------------

You can use the :py:meth:`setup() <dwfpy.digital_io.DigitalIo.Channel>` function
to setup a Digital I/O pin.
To configure the Digital I/O pins, pass the parameter ``configure=True``.

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       io = device.digital_io
       # Configure DIO-0 as output, and set the state to high
       io[0].setup(enabled=True, state=True)
       # Configure DIO-1 as output, and set the state to low
       io[1].setup(enabled=True, state=False, configure=True)
       # Output a one on DIO-1
       io[1].output_state = True

For a complete example, see
`examples/digital_in_acquisition.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/digital_in_acquisition.py>`_.

