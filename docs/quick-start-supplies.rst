.. include:: common.rst

Using the Power Supplies
========================

Depending on the device you have, there may be one or more power supplies that can be accessed via the channels and nodes of the **Analog IO** module,
which are documented in the |WaveForms-SDK-Reference-Manual|.

.. note::
   In order to output a voltage, most power supplies have to be enabled both individually and via the **master enable switch**.

For instance, to output 3.3V on the positive power supply of an **Analog Discovery 2**, you can write:

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       # Set the voltage of the positive power supply to 3.3V.
       device.analog_io[0][1].value = 3.3

       # Enable the positive power supply.
       device.analog_io[0][0].value = True

       # Enable the master-enable switch.
       device.analog_io.master_enable = True

Instead of the generic **Device** class, you can also use the specialized device classes,
which simplifies the access to the power supplies.

For instance, to output 3.3V on the positive power supply of an **Analog Discovery 2**, you can write:

.. code-block::

   import dwfpy as dwf

   with dwf.AnalogDiscovery2() as device:
       # Set the positive power supply to 3.3V and enable it.
       device.supplies.positive.setup(voltage=3.3)
       device.supplies.master_enable = True
