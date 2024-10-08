#!/usr/bin/python3

from fw_upspack_v3.base.commons import *
from fw_upspack_v3.ups._definitions import *
from fw_upspack_v3.ups._dbus_descs import *
from fw_upspack_v3.ups._parsers import *


# Given an VERSION, this object returns all his info and meta-data
PID = {
    "V3.2P": {"model": "UPS Smart", "type": DEV_TYPE_UPSSmart_V32P,
              "dbus_iface": DEV_IFACE_UPSSmart, "dbus_desc": DEV_DBUS_DESC_UPSSmart},
}

PROPS_CODES = {
    "SmartUPS": {"name": "firmware_version", "desc": "UPS's firmware version",
                 "parser": props_parser_str},
    "Vin": {"name": "state_operation", "desc": "UPS's charging state (True=Charging)",
            "parser": props_parser_vin},
    "BATCAP": {"name": "battery_capacity", "desc": "UPS's battery capacity in percentage",
               "parser": props_parser_int},
    "Vout": {"name": "voltage_out_millis", "desc": "UPS's output voltage in mV",
             "parser": props_parser_int},
}


CALC_PROPS_CODES = {
    "voltage_out": {"depends_on": "voltage_out_millis",
                "calculator": calc_voltage_out},
}
