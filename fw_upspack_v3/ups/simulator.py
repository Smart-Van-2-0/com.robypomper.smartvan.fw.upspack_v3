#!/usr/bin/python3

from fw_upspack_v3.ups.device import Device
from fw_upspack_v3.ups.mappings import *
from fw_upspack_v3.commons import regenerateValue


class DeviceSimulator(Device):

    def __init__(self, device: str = '/dev/ttyAMA0', speed: int = 9600):
        super().__init__(device, speed, False)
        self._data = {
            'SmartUPS': 'V3.2P',
            'Vin': 'GOOD',
            'BATCAP': "100",
            'Vout': '5250'
        }

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
