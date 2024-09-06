#!/usr/bin/python3

from fw_upspack_v3.ups.mappings import *
from fw_upspack_v3.base.device_serial import DeviceSerial


class Device(DeviceSerial):
    """
    Device class for UPS Pack devices communicating via Serial port
    """

    DELIMITER = "$ SmartUPS"
    FIELD_PID = "SmartUPS"
    FIELD_TYPE = "--"

    def __init__(self, device: str = '/dev/ttyAMA0', speed: int = 9600, auto_refresh=True):
        super().__init__(device, speed, self.DELIMITER, self.FIELD_PID, self.FIELD_TYPE, auto_refresh)

        self.cached_version = None

    def _parse_pdu(self, frames):
        """ $ SmartUPS V3.2P,Vin NG,BATCAP 64,Vout 5250 $ """
        for frame in frames:
            frame = frame.decode('utf-8').replace('$', '')
            all_data = frame.strip().split(',')
            for data in all_data:
                sub_data = data.split(' ')
                key = sub_data[0]
                value = sub_data[1]
                self._data[key] = value

    @property
    def device_version(self) -> "str | None":
        """ Returns the device PID """
        if self.cached_version is None:
            self.cached_version = self._data['SmartUPS']

        return self.cached_version

    @property
    def device_type(self) -> str:
        """ Returns the device type """
        if self.cached_type is None:
            if self.device_pid is not None:
                try:
                    self.cached_type = PID[self.device_pid]['type']
                except KeyError as err:
                    raise SystemError("Unknown PID '{}' read from device".format(self.device_pid)) from err

        return self.cached_type if self.cached_type is not None else DEV_TYPE_UNKNOWN


if __name__ == '__main__':
    v = Device()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))
