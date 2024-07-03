# FW UPS Pack V3 - Supported devices

Once the device is initialized, the script reads its data. Each PDU contains the
`$ SmartUPS` property which is the **product VERSION of the connected device**.
The **device information is then retrieved from the PID mapping** in the
[mappings.py](/fw_upspack_v3/ups/mappings.py) file, this file is based on
the [Devices by VERSION](#devices-by-version) tables.<br/>
Then, those info are used to initialize the DBus object with the correspondent
DBus iface and description. Both, the iface and the object description are
defined into the `PID` mapping.

* `model`: human-readable name of the exact model
* `type`: devices code to group similar devices
  from [_definitions.py](/fw_upspack_v3/ups/_definitions.py) as `DEV_TYPE_*`
* `dbus_iface`: a string defining the DBus iface<br/>
  from [_definitions.py](/fw_upspack_v3/ups/_definitions.py) as `DEV_IFACE_*`
* `dbus_desc`: a string defining the DBus object's description<br/>
  [dbus_definitions.py](/fw_upspack_v3/ups/_dbus_descs.py) as `DEV_DBUS_DESC_*`

## Device types

Here, you can find the list of all devices types available. Any product ID
from [Devices by PID](#devices-by-version) section is mapped into a device type
using the `PID` table from the [mappings.py](/fw_upspack_v3/ups/mappings.py)
file. More details on DBus definitions and their properties can be found on
the [Values Mapping](values_mapping.md#properties-by-dbus-object-description)
page.

| Type's Constant          | Type's Name     | DBus's Iface   | DBus's Description       |
|--------------------------|-----------------|----------------|--------------------------|
| `DEV_TYPE_UPSSmart_V32P` | UPS Smart v3_2P | com.upspack_v3 | `DEV_DBUS_DESC_UPSSmart` |

## Devices by VERSION

At the current version, any 'UPS Pack V3' devices with the `V3.2P` firmware
installed is supported. To support more versions, please update the `PID` table
into the [mappings.py](/fw_upspack_v3/ups/mappings.py) file.
