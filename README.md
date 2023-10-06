# FW UPS Pack V3

Simple Python module that read data from "UPS Pack V3" and share them on
the local DBus.
This repository is part of the [Smart Van Project](https://smartvan.johnosproject.org/).

**FW Name:** FW Victron<br />
**FW Group:** com.robypomper.smartvan.fw.victron<br />
**FW Version:** 1.0.2-DEV

[README](README.md) | [CHANGELOG](CHANGELOG.md) | [TODOs](TODOs.md) | [LICENCE](LICENCE.md)

Once ran, this script **reads data from the serial specified port then notify
the DBus with updated values**. The DBus service and his properties depends on
the PID get from the device. More info on [Supported devices and value
mapping](#supported-devices-and-value-mapping).


## Run

This is a Python script, so `python` is required to run it.

Once Python was installed on youir machine, you can install the script's
requirements globally or create a dedicated `venv`.

```commandline
# Init venv (Optional)
$ python -m venv venev
$ source venv/bin/activate

# Install script's requirements
$ pip install -r requirements.txt
```

Now, you are ready to run the script with the command:

```commandline
$ python run.py

or specify DBus params

$ python run.py  --dbus-name com.custom.bus --dbus-obj-path /custom/path --dbus-iface com.custom.IFace
```

Defaults DBus params are:
* DBus Name: `com.victron`
* DBus Obj Path: DEV_TYPE_* (eg: `smartsolar_mppt`)
* DBus Interface: DEV_IFACE_* (eg: `com.victron.SmartSolarMPPT`)

### Script's arguments

The `run.py` script accept following arguments:
 
* `-h`, `--help`: show this help message and exit
* `-v`, `--version`: show version and exit
* `--port PORT`: serial port
* `--speed SPEED`: serial port speed
* `--simulate`: Simulate a VEDevice with id `0xA060`
* `--dbus-name DBUS_NAME`: DBus name
* `--dbus-obj-path DBUS_OBJ_PATH`: DBus object path (if None, the device type will be used, if empty nothing will be used)
* `--dbus-iface DBUS_IFACE`: DBus interface (if None, the device interface will be used, if empty nothing will be used)
* `--dev`: enable development mode, increase logged messages info
* `--debug`: Set log level to debug
* `--quiet`: Set log level to errorexecuted and


## Develop

The main goal for this script is to link the VE.Direct protocol to the DBus.
So, in addition to the main script, all other files are related to the VE Direct
or to the DBus protocols.


## Supported devices and value mapping

This script should be able to handle any Victron device that support the VE.Direct
protocol via Serial cable.

On VE.Direct side, this script can read and handle all properties defined into
the [VE.Direct-Protocol-3.33.pdf](https://www.victronenergy.com/upload/documents/VE.Direct-Protocol-3.33.pdf)
from Victron. The full list of implemented properties, but also the known PIDs
list can be found into the [`mappings.py`](fw_victron/mappings.py) file.

On the DBus side, only the "SmartSolar MPPT" and "SmartSolar MPPT VE.Can"
devices are defined. Other device types missing their DBus object definition at
[`dbus_definitions.py`](fw_victron/dbus_definitions.py).<br/>
When this script is **connected to an unsupported device type, then it raise an
exception and exit**.
