#!/usr/bin/python3

import serial

from .mappings import *


class VEDirectException(Exception):
    pass


class InvalidChecksumException(VEDirectException):
    pass


def check_frame_checksum(frames: list[bytes]):
    """ Checks the PDU for validity.
    The "checksum" generates a char so that the sum
    of all characters equals 0 mod 256"""
    checksum = 0
    for frame in frames:
        for char in frame:
            checksum = (checksum + char) % 256
    return checksum == 0


class VEDevice:

    def __init__(self, device: str = '/dev/ttyUSB0', speed: int = 19200, auto_refresh=True):
        self.device = device
        self.speed = speed
        self._data = {}

        self._is_connected = False
        self._is_reading = False

        self.cached_pid = None
        self.cached_model = None
        self.cached_type = None
        self.cached_serial = None

        if auto_refresh:
            self.refresh()

    def refresh(self, reset_data=False) -> bool:
        """
        Reads and parse data from the serial port.

        return: True if it read data successfully
        """
        if self._is_reading:
            while self._is_reading:
                pass
            return self._is_connected

        self._is_reading = True
        if reset_data:
            self._data = {}
        frames = self._get_data()
        self._parse_pdu(frames)
        self._is_reading = False

        return self._is_connected

    @property
    def is_connected(self) -> bool:
        """ Returns True if at last refresh attempt the serial device was available. """
        return self._is_connected

    @property
    def is_reading(self) -> bool:
        """ Returns the local device (eg: '/dev/ttyUSB0') used to connect to the serial device """
        return self._is_reading

    def _parse_pdu(self, frames):
        for frame in frames:
            if frame.startswith(b'Checksum'):
                # This entry is useless
                continue
            key, value = frame.strip().decode('utf-8').split('\t')
            self._data[key] = value

    def _get_data(self) -> list[bytes]:
        """ Returns a PDU array, one entry per line."""
        data = []
        try:
            with serial.Serial(self.device, self.speed, timeout=4) as s:
                self._is_connected = True
                # Wait for start of frame
                while True:
                    frame = s.readline()
                    if frame.startswith(b'PID'):
                        break

                # slurp all frames
                frame = b''
                while not frame.startswith(b'PID'):
                    frame = s.readline()
                    data.append(frame)
        except serial.serialutil.SerialException:
            self._is_connected = False

        # The checksum is for the whole DTU
        if not check_frame_checksum(data):
            # raise InvalidChecksumException()
            return []

        return data

    @property
    def conn_device(self) -> str:
        """ Returns the local device (eg: '/dev/ttyUSB0') used to connect to the serial device """
        return self.device

    @property
    def conn_speed(self) -> int:
        """ Returns the speed used to communicate with the serial device """
        return self.speed

    @property
    def device_serial(self) -> str | None:
        """ Returns the device PID """
        if self.cached_serial is None:
            self.cached_serial = self._data['SER#']

        return self.cached_serial

    @property
    def device_pid(self) -> str | None:
        """ Returns the device PID """
        if self.cached_pid is None:
            self.cached_pid = self._data['PID']

        return self.cached_pid

    @property
    def device_model(self) -> str | None:
        """ Returns the device model """
        if self.cached_model is None:
            if self.device_pid is not None:
                self.cached_model = PID[self.device_pid]['model']

        return self.cached_model

    @property
    def device_type(self) -> str:
        """ Returns the device type """
        if self.cached_type is None:
            model = self.device_model
            if model is not None:
                self.cached_type = PID[self.device_pid]['type']

        return self.cached_type if self.cached_type is not None else DEV_TYPE_UNKNOWN

    @property
    def device_type_code(self) -> str:
        """ Returns the device type as a code string"""
        return dev_type_to_code(self.device_type)

    @property
    def latest_data(self) -> dict:
        return self._data


if __name__ == '__main__':
    v = VEDevice()
    print("{}/{}# [{}CONNECTED]: {}".format(v.device_model, v.device_serial,
                                            "" if v.is_connected else "NOT ", v.latest_data["V"]))
