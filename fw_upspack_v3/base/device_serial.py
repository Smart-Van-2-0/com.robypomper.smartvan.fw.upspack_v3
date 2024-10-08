#!/usr/bin/python3

import logging
import os
import serial

from fw_upspack_v3.base.device import DeviceAbs
from fw_upspack_v3.base.commons import dev_type_to_code

logger = logging.getLogger()


class DeviceSerial(DeviceAbs):
    """
    Serial device base classes.
    """

    def __init__(self, device: str = '/dev/ttyAMA0', speed: int = 9600, pdu_delimiter="$", device_pid_index="PID", device_type_index="Type", auto_refresh=True):
        super().__init__()

        self.device = device
        self.speed = speed
        self.pdu_delimiter_bytes = pdu_delimiter \
            if pdu_delimiter is None or type(pdu_delimiter) == bytes \
            else pdu_delimiter.encode()
        self._device_pid_index = device_pid_index
        self._device_type_index = device_type_index
        self._data = {}

        self._is_connected = False
        if os.path.exists(device):
            with serial.Serial(self.device, self.speed, timeout=1) as _s:
                self._is_connected = True
        self._is_reading = False

        self.cached_pid = None
        self.cached_type = None
        self.cached_type_code = None

        if auto_refresh:
            self.refresh()

    def refresh(self, reset_data=False) -> bool:
        """
        Reads and parse data from the serial port.

        return: True if it read data successfully
        """
        if self._is_reading:
            while self._is_reading or self.must_terminate:
                pass
            if self.must_terminate:
                return False
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
        """
        Parse the entire PDU and populate the `self._data` array.
        :param frames: a list of all lines included into read pdu, if pdu is only
                       one line, then the list will contain only one element
        """
        raise NotImplementedError()

    def _get_data(self) -> list[bytes]:
        """ Returns a PDU array, one entry per line."""
        data = []
        try:
            with serial.Serial(self.device, self.speed, timeout=1) as s:
                self._is_connected = True
                # Wait for start of frame
                while not self.must_terminate:
                    frame = s.readline()
                    if frame.startswith(self.pdu_delimiter_bytes):
                        break

                # slurp all frames
                frame = b''
                while not frame.startswith(self.pdu_delimiter_bytes) and not self.must_terminate:
                    frame = s.readline()
                    data.append(frame)

                if len(data) == 0:
                    logger.debug("Error querying device, no data received")
                    self._is_connected = False
                    return []
                if not self._find_pid(data):
                    logger.debug("Error querying device, no PID received")
                    self._is_connected = False
                    return []

                if self.must_terminate:
                    self._is_connected = False

        except serial.serialutil.SerialException as err:
            logger.warning("Error querying device ({})".format(err))
            self._is_connected = False

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
    def device_pid(self) -> "str | None":
        """
        Returns the device PID, it can be used as index for the PID dict.
        In the SIM7600 case is the device's model (AT+CGMM).
        """

        if self.cached_pid is None:
            try:
                self.cached_pid = self._data[self._device_pid_index]
            except KeyError as err:
                logger.debug("Field '{}' not found on read data".format(self._device_pid_index))
                raise SystemError("Unknown PID from device") from err

        return self.cached_pid

    def _find_pid(self, data):
        for frame in data:
            if self._device_pid_index.encode() in frame:
                return True
        return False

    @property
    def device_type(self) -> "str | None":
        """
        Returns the device PID, it can be used as index for the PID dict.
        In the SIM7600 case is the device's model (AT+CGMM).
        """

        if self.cached_type is None:
            try:
                self.cached_type = self._data[self._device_type_index]
            except KeyError as err:
                logger.debug("Field '{}' not found on read data".format(self._device_type_index))
                raise SystemError("Unknown Type from device") from err

        return self.cached_type

    @property
    def device_type_code(self) -> str:
        """ Returns the device type as a code string"""

        if self.cached_type_code is None and self.device_type is not None:
            self.cached_type_code = dev_type_to_code(self.device_type)

        return self.cached_type_code

    @property
    def latest_data(self) -> dict:
        return self._data
