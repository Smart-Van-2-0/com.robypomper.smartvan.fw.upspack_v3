# FW UPS Pack V3 - Values Mapping

The properties exposed on the DBus vary depending on
the [type of device](supported_devices.md). A description of the
DBus object to be exposed is defined for each type of device. The DBus object
definitions are specified in the
[_dbus_descs.py](/fw_upspack_v3/ups/_dbus_descs.py) file.

During the `main_loop`, this script refresh the device's data and parse any
property found, if the property value is update the script sends the property
update to the DBus. To parse the property it uses the info contained into
the`PROPS_CODE` table. Sometime, it can trigger an exception because the updated
property is not present into the DBus object definitions. In this case add the
property to the DBus object definitions or fix the `PROPS_CODES` table.

## DBus properties

Exposed properties can be of two types: direct or calculated. Direct properties
are exported as they come from the device. Calculated properties are the result
of an elaboration.

### Direct

Direct properties are defined into the `PROPS_CODES` table into
the [mappings.py](/fw_upspack_v3/ups/mappings.py) file.

For each property are defined following fields:

* `KEY`: property name on device side
* `name`: property name on DBus
* `desc`: human-readable description of the property
* `parser`: the method to use to parse the value read from the device

| Prop.'s KEY | Prop.'s Name on DBus | Description                          | Parser method      |
|-------------|----------------------|--------------------------------------|--------------------|
| `SmartUPS`  | `firmware_version`   | UPS's firmware version               | `props_parser_str` |
| `Vin`       | `state_operation`    | UPS's charging state (True=Charging) | `props_parser_vin` |
| `BATCAP`    | `battery_capacity`   | UPS's battery capacity in percentage | `props_parser_int` |
| `Vout`      | `voltage_out_millis` | UPS's output voltage in mV           | `props_parser_int` |

Parser methods are defined into [_parsers.py](/fw_upspack_v3/ups/_parsers.py)
file. Depending on which DBus property's they are mapped for, they can return
different value's types.<br/>
Custom types are defined into
the [_definitions.py](/fw_upspack_v3/ups/_definitions.py) file.

### Calculated

Calculated properties are special values that can be elaborated starting from
other properties (also other calculated properties). When a property is updated,
the script checks if there is some calculated property that depends on it. If
any, then the script calculate the dependant property.

For each calculated property are defined following fields:

* `KEY`: calculated property name on DBus
* `name`: calculated property name (not used)
* `desc`: human-readable description of the property
* `depends_on`: the list of properties on which the current property depends
* `calculator`: the method to use to elaborate the property

| Prop.'s Name on DBus | Description                  | Depends on           | Calculator method  |
|----------------------|------------------------------|----------------------|--------------------|
| `voltage_out`        | UPS' output voltage in volts | `voltage_out_millis` | `calc_voltage_out` |

All methods used to elaborate the properties, receives the properties cache as
param. So they can use that list to get all properties read from the device (
also other calculated properties).

## Properties by DBus Object description

This is the table containing all properties handled by this script. For each
property, the table define if it will be exported by the column's device type.

| Prop.'s Name on DBus | Type   | UPS Smart v3_2P | 
|----------------------|--------|-----------------|
| `firmware_version`   | string | Yes             |
| `state_operation`    | bool   | Yes             |
| `battery_capacity`   | int    | Yes             |
| `voltage_out_millis` | int    | Yes             |
| `voltage_out`        | double | Yes             |
