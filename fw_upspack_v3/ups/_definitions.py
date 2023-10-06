#!/usr/bin/python3

# Default device type for unknown devices
DEV_TYPE_UNKNOWN = "Unknown Device Type"

# List of supported devices' types
DEV_TYPE_BMV = "BMV"
DEV_TYPE_BlueSolar_MPPT = "BlueSolar MPPT"
DEV_TYPE_BlueSolar_MPPT_VECan = "BlueSolar MPPT VE.Can"
DEV_TYPE_SmartSolar_MPPT = "SmartSolar MPPT"
DEV_TYPE_SmartSolar_MPPT_VECan = "SmartSolar MPPT VE.Can"
DEV_TYPE_Phoenix_Inverter = "Phoenix Inverter"
DEV_TYPE_Phoenix_Smart_IP43_Charger = "Phoenix Smart IP43 Charger"
DEV_TYPE_SmartShunt = "SmartShunt"

# WARN and AR has same codes, but different meanings
# WARN is just a warning while AR (alarm reason) is the reason why the inverter went into security shutdown
WARN_AR = {
    1: "Low Voltage",
    2: "High Voltage",
    4: "Low SOC",
    8: "Low Starter Voltage",
    16: "High Starter Voltage",
    32: "Low Temperature",
    64: "High Temperature",
    128: "Mid Voltage",
    256: "Overload",
    512: "DC-ripple",
    1024: "Low V AC out",
    2048: "High V AC out",
    4096: "Short Circuit",
    8192: "BMS Lockout"
}

MODE = {
    "1": "Charger",
    "2": "Inverter",
    "4": "Off",
    "5": "Eco",
    "253": "Hibernate",
}

CS = {
    "0": "OFF",
    "1": "Low power",
    "2": "Fault",
    "3": "Bulk",
    "4": "Absorption",
    "5": "Float",
    "6": "Storage",
    "7": "Equalize (manual)",
    "9": "Inverting",
    "11": "Power supply",
    "245": "Starting-up",
    "246": "Repeated absorption",
    "247": "Auto equalize / Recondition",
    "248": "BatterySafe",
    "252": "External Control"
}

ERROR = {
    "0": "No error",
    "2": "Battery voltage too high",
    "17": "Charger temperature too high",
    "18": "Charger over current",
    "19": "Charger current reversed",
    "20": "Bulk time limit exceeded",
    "21": "Current sensor issue (sensor bias/sensor broken)",
    "26": "Terminals overheated",
    "28": "Converter issue (dual converter models only)",
    "33": "Input voltage too high (solar panel)",
    "34": "Input current too high (solar panel)",
    "38": "Input shutdown (due to excessive battery voltage)",
    "39": "Input shutdown (due to current flow during off mode)",
    "65": "Lost communication with one of devices",
    "66": "Synchronised charging device configuration issue",
    "67": "BMS connection lost",
    "68": "Network misconfigured",
    "116": "Factory calibration data lost",
    "117": "Invalid/incompatible firmware",
    "119": "User settings invalid"
}

MPPT = {
    "0": "OFF",
    "1": "Voltage or current limited",
    "2": "MPP Tracker active"
}

CAP_BLE = {
    "0x00000001": "BLE supports switching off",
    "0x00000002": "BLE switching off is permanent"
}

OR = {
    "0x00000000": "Not Off/No Reason",
    "0x00000001": "No input power",
    "0x00000002": "Switched off (power switch)",
    "0x00000004": "Switched off (device mode register)",
    "0x00000008": "Remote input",
    "0x00000010": "Protection active",
    "0x00000020": "Paygo",
    "0x00000040": "BMS",
    "0x00000080": "Engine shutdown detection",
    "0x00000100": "Analysing input voltage"
}

MON = {
    "-9": "Solar charger",
    "-8": "Wind turbine",
    "-7": "Shaft generator",
    "-6": "Alternator",
    "-5": "Fuel cell",
    "-4": "Water generator",
    "-3": "DC/DC charger",
    "-2": "AC charger",
    "-1": "Generic source",
    "0": "Battery monitor (BMV)",
    "1": "Generic load",
    "2": "Electric drive",
    "3": "Fridge",
    "4": "Water pump",
    "5": "Bilge pump",
    "6": "DC system",
    "7": "Inverter",
    "8": "Water heater"
}
