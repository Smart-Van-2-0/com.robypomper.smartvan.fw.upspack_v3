#!/usr/bin/python3

import random

from .device import VEDevice
from .mappings import *

class VEDeviceSimulator(VEDevice):

    def __init__(self, device: str = '/dev/ttyUSB0', speed: int = 19200):
        super().__init__(device, speed, False)
        self._data = {
            'FW': '',
            'SER#': '',
            'V': "12000.0",
            'I': '0.0',
            'VPV': '0',
            'PPV': '0',
            'CS': '0',
            'MPPT': '0',
            'OR': '0',
            'ERR': '0',
            'LOAD': "OFF",
            'IL': '0',
            'H19': '0',
            'H20': '0',
            'H21': '0',
            'H22': '0',
            'H23': '0',
            'HSDS': '0',
            'PID': '0xA060'
        }

    def refresh(self, reset_data=False) -> bool:
        self._data = {
            'FW': '161',
            'SER#': 'HQ221234567',
            'V': max(min(self.regenerateValue(self._data['V'], 200), 15000), 10000),
            'I': max(min(self.regenerateValue(self._data['I'], 200), 4000), 0),
            'VPV': max(min(self.regenerateValue(self._data['VPV'], 200), 15000), 0),
            'PPV': max(min(self.regenerateValue(self._data['PPV'], 5), 200), 0),
            'CS': '0',
            'MPPT': '0',
            'OR': '0x00000001',
            'ERR': '0',
            'LOAD': "ON" if random.randint(0, 1) else "OFF",
            'IL': max(min(self.regenerateValue(self._data['IL'], 200), 4000), 0),
            'H19': '230',
            'H20': '0',
            'H21': '0',
            'H22': '0',
            'H23': '0',
            'HSDS': '25',
            'PID': '0xA060'
        }
        return True

    @staticmethod
    def regenerateValue(str_value, range_value):
        prev_value = props_parser_float(str_value)
        inc = random.randint(0, range_value) - (range_value / 2)
        return prev_value + inc


if __name__ == '__main__':
    v = VEDeviceSimulator()
    print("{}/{}# [{}CONNECTED]: {}".format(v.device_model, v.device_serial,
                                            "" if v.is_connected else "NOT ", v.latest_data["V"]))
