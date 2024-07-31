#!/usr/bin/python3

def props_parser_vin(raw_value: str) -> bool:
    try:
        if raw_value.upper() == "GOOD":
            return True
        elif raw_value.upper() == "NG":
            return False
        else:
            raise ValueError("Can't cast '{}' into {}, invalid value".format(raw_value, "float"))
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "float"))


def calc_voltage_out(property_cache) -> float:
    voltage_out_millis = property_cache['voltage_out_millis']['value']
    return voltage_out_millis / 1000
