.. include:: common.rst

dwfpy Design
============

The design of the **dwfpy** package consists of three layers: Python bindings, low-level API, and high-level API.

Bindings
--------

The **dwfpy** bindings give you raw access to the C API of the DWF DLL.
In order to provide a natural look-and-feel while working in Python, the following API changes have been made:

- The naming of the DWF API has been adapted to match Python naming conventions.
- The DWF function API has been declared using the ctypes `CFUNCTYPE` prototypes, which allow you to pass Python types such as `int`, instead of ctypes types such as `c_int`.
- Error handling is performed automatically, i.e. the C functions return value is checked and an exception is thrown when appropriate.
- Function return values are directly returned as a scalar or tuple.

For instance, the DWF C API to get the minimum and maximum offset voltage of an analog-out channel is:

.. code-block:: c

   int FDwfAnalogOutNodeOffsetInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pMin, double *pMax);

When working with the **dwfpy** bindings, it can be used as follows:

.. code-block::

   import dwfpy as dwf
   import dwfpy.bindings as dwfb

   with dwf.Device() as device:
       min_offset, max_offset = dwfb.dwf_analog_out_node_offset_info(device.handle, 0, dwfb.ANALOG_OUT_NODE_CARRIER)

Typically, you do not work with the **dwfpy** bindings. Instead, use the low-level or high-level API.

Low-Level API
-------------

The **dwfpy** low-level API is designed to map the bindings to a more structured API.

- Functional units of the device have been grouped into objects.
- Channels and nodes are abstracted as collections, using a dict-like API.

For instance, the DWF C API to set the offset voltage of the analog_out channel 1 (arbitary waveform generator) is:

.. code-block:: c

   int FDwfAnalogOutNodeOffsetSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double vOffset);

When working with the **dwfpy** low-level API, it can be used as follows:

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       device.analog_output.channels[0].nodes[dwf.AnalogOutputNode.CARRIER].offset = 1.23

High-Level API
--------------

The dwfpy high-level API is designed to perform multiple common actions with a single line of Python code.

For instance, to start channel 1 of the arbitary waveform generator to output a sine-wave,
using a frequency of 1kHz and an amplitude of 1Vpp, you would write:

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       device.analog_output['ch1'].setup(function='sine', frequency=1e3, amplitude=1, start=True)
