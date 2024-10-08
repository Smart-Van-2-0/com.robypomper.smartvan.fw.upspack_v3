#!/usr/bin/python3

import random

from fw_upspack_v3.ups.device import Device
from fw_upspack_v3.base.commons import regenerateValueMaxMin


class DeviceSimulator(Device):

    def __init__(self, device, speed):
        super().__init__(device, speed, auto_refresh=False)
        self._data = {
            'SmartUPS': 'V3.2P',
            'Vin': 'GOOD',
            'BATCAP': "100",
            'Vout': '5250'
        }
        self._is_connected = True

    def refresh(self, reset_data=False) -> bool:
        self._data = {
            'SmartUPS': 'V3.2P',
            'Vin': 'GOOD' if random.randint(0, 1) else "NG",
            'BATCAP': str(int(regenerateValueMaxMin(self._data['BATCAP'], 1, 0, 100))),
            'Vout': str(int(regenerateValueMaxMin(self._data['Vout'], 10, 5100, 5400))),
        }
        return True


if __name__ == '__main__':
    v = DeviceSimulator()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))
