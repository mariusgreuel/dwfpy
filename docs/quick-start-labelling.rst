.. include:: common.rst

Labelling Channels
==================

Instead of indexing channels via a zero-based integer index, the channels can be accessed via a label.
By default, analog channels are labelled *ch1*, *ch2*, etc.
Digital channels are labelled *dio0*, *dio1*, etc.

You can rename the channel labels to you needs.
For instance, if you have a clock signal on DIO pin 0 that you want to access via the label *clock*, you could write:

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       # Rename pin DIO-0 from 'dio0' to 'clock'
       device.digital_output[0].label = 'clock'

       # DIO-0 can now be referenced via the label 'clock'
       device.digital_output['clock'].setup_clock(frequency=1e3)
