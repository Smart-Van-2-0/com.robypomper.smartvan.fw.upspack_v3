# FW Victron - Changelog

[README](README.md) | [CHANGELOG](CHANGELOG.md) | [TODOs](TODOs.md) | [LICENCE](LICENCE.md)


## Version 1.0.1

* Refactored cmdLine args replacing `_` char with `-`
* Added VEDevice simulator available with the cmdLine arg `--simulate`
* Improved DBus support introducing DBus object interface support
* Fixed VEDeviceSimulator data generation
* Add signal INT and TERM handler into `run.py`


## Version 1.0.0

* VE.Direct support via `VEDevice` class
  * Implemented `ve_device.py` starting from [`karioja/vedirect`](https://github.com/karioja/vedirect)::`vedirect/vedirect.py`
  * Implemented `ve_parsers.py` starting from [`birdie1/victron`](https://github.com/birdie1/victron)::`lib/helper.py` file
  * Implemented `ve_definitions.py` starting from [`birdie1/victron`](https://github.com/birdie1/victron)::`lib/mapper.py` file
* DBus support via `dbus_daemon.py` and `DBusObject` class
  * Implemented `dbus_daemon.py` as a provider for a singleton DBus instance
  * Implemented `dbus_definitions.py` based on [VE.Direct-Protocol-3.33.pdf](https://www.victronenergy.com/upload/documents/VE.Direct-Protocol-3.33.pdf)
  * Implemented `dbus_obj.py` as a DBus service including VE.Direct properties
* Implemented `mappings.py` that links PID to device model and VE.Direct's properties to DBus properties
* Implemented `run.py` as main script  
