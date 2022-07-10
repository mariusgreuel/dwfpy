.. include:: common.rst

Working with Devices
====================

Creating a Device Instance
--------------------------

To find and create an instance of a Digilent Waveforms device,
you simply create an instance of the :py:class:`Device <dwfpy.device.Device>` class.
You should use the Python `with statement <https://docs.python.org/3/whatsnew/2.6.html#pep-343-the-with-statement>`_
to ensure that your device is closed automatically on exit, or when an exception occurs:

.. code-block::

   import dwfpy as dwf

   with dwf.Device() as device:
       print(f'Found device: {device.name} ({device.serial_number})')

Using a Specific Device Instance
--------------------------------

If you know the kind of device you have connected to your PC,
you can use a specialized class, such as :py:class:`AnalogDiscovery2 <dwfpy.device.AnalogDiscovery2>` or :py:class:`DigitalDiscovery <dwfpy.device.DigitalDiscovery>`,
which provides additional functions that are specific to that device:

.. code-block::

   import dwfpy as dwf

   with dwf.AnalogDiscovery2() as device:
       print(f'Found an Analog Discovery 2: {device.user_name} ({device.serial_number})')

You can find the available device classes in the :py:class:`device <dwfpy.device>` module.

Filtering Devices
-----------------

If you have multiple devices installed, you can pass additional filter parameters,
while creating the device instance. For example, you can pass a **serial number** to pick a specific device:

.. code-block::

   import dwfpy as dwf

   with dwf.Device(serial_number='123456ABCDEF') as device:
       print(f'Found a device with matching serial number: {device.user_name} ({device.serial_number})')

You can find additional filter parameters in the class constructor method :py:class:`Device <dwfpy.device.Device>`.

Enumerating Devices
-------------------

If you want to enumerate all present devices and get the devices properties,
you can use the :py:meth:`Device.enumerate() <dwfpy.device.Device.enumerate>` function to enumerate devices:

.. code-block::

   import dwfpy as dwf

   for device in dwf.Device.enumerate():
       print(f'Found device: {device.name} {device.serial_number}')

For a complete example, see
`examples/device_enumeration.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/device_enumeration.py>`_
and
`examples/device_info.py <https://github.com/mariusgreuel/dwfpy/blob/main/examples/device_info.py>`_
