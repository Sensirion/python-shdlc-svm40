# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcDeviceBase, ShdlcFirmwareUpdate
from .device_errors import SVM40_DEVICE_ERROR_LIST
from .firmware_image import Svm40FirmwareImage
from .commands import \
    Svm40CmdGetProductType, \
    Svm40CmdGetProductName, \
    Svm40CmdGetSerialNumber, \
    Svm40CmdGetVersion, \
    Svm40CmdDeviceReset, \
    Svm40CmdGetSystemUpTime, \
    Svm40CmdStartContinuousMeasurement, \
    Svm40CmdStopMeasurement, \
    Svm40CmdReadMeasuredValuesAsIntegers, \
    Svm40CmdReadMeasuredValuesAsIntegersWithRawParameters, \
    Svm40CmdGetTemperatureOffsetForRhtMeasurements, \
    Svm40CmdGetVocTuningParameters, \
    Svm40CmdStoreNvData, \
    Svm40CmdSetTemperatureOffsetForRhtMeasurements, \
    Svm40CmdSetVocTuningParameters, \
    Svm40CmdGetVocState, \
    Svm40CmdSetVocState
from .response_types import AirQuality, Humidity, Temperature
from sensirion_shdlc_driver.types import FirmwareVersion, HardwareVersion, \
    ProtocolVersion, Version
from struct import pack, unpack


import logging
log = logging.getLogger(__name__)


class Svm40ShdlcDevice(ShdlcDeviceBase):
    """
    SVM40 device.

    This is a low-level driver which just provides all SHDLC commands as Python
    methods. Typically, calling a method sends one SHDLC request to the device
    and interprets its response. There is no higher level functionality
    available, please look for other drivers if you need a higher level
    interface.

    There is no (or very few) caching functionality in this driver. For example
    if you call :func:`get_serial_number` 100 times, it will send the command
    100 times over the SHDLC interface to the device. This makes the driver
    (nearly) stateless.
    """

    def __init__(self, connection, slave_address):
        """
        Create an SVM40 device instance on an SHDLC connection.

        .. note:: This constructor does not communicate with the device, so
                  it's possible to instantiate an object even if the device is
                  not connected or powered yet.

        :param ~sensirion_shdlc_driver.connection.ShdlcConnection connection:
            The connection used for the communication.
        :param byte slave_address:
            The address of the device. The default address of the SVM40 is 0.
        """
        super(Svm40ShdlcDevice, self).__init__(connection, slave_address)
        self._register_device_errors(SVM40_DEVICE_ERROR_LIST)

    def get_product_type(self, as_int=False):
        """
        Get the product type. The product type (sometimes also called "device
        type") can be used to detect what kind of SHDLC product is connected.

        :param bool as_int: If ``True``, the product type is returned as an
                            integer, otherwise as a string of hexadecimal
                            digits (default).
        :return: The product type as an integer or string of hexadecimal
                 digits.
        :rtype: string/int
        """
        product_type = self.execute(Svm40CmdGetProductType())
        if as_int:
            product_type = int(product_type, 16)
        return product_type

    def get_product_name(self):
        """
        Get the product name of the device.

        :return: The product name as an ASCII string.
        :rtype: string
        """
        return self.execute(Svm40CmdGetProductName())

    def get_serial_number(self):
        """
        Get the serial number of the device.

        :return: The serial number as an ASCII string.
        :rtype: string
        """
        return self.execute(Svm40CmdGetSerialNumber())

    def get_version(self):
        """
        Get the version of the device firmware, hardware and SHDLC protocol.

        :return: The device version as a Version object.
        :rtype: Version
        """
        firmware_major, firmware_minor, firmware_debug, \
            hardware_major, hardware_minor, protocol_major, protocol_minor = \
            self.execute(Svm40CmdGetVersion())
        return Version(
            firmware=FirmwareVersion(
                major=firmware_major,
                minor=firmware_minor,
                debug=firmware_debug
            ),
            hardware=HardwareVersion(
                major=hardware_major,
                minor=hardware_minor
            ),
            protocol=ProtocolVersion(
                major=protocol_major,
                minor=protocol_minor
            )
        )

    def get_system_up_time(self):
        """
        Get the system up time of the device.

        :return: The time since the last power-on or device reset [s].
        :rtype: int
        """
        return self.execute(Svm40CmdGetSystemUpTime())

    def device_reset(self):
        """
        Execute a device reset (reboot firmware, similar to power cycle).
        """
        self.execute(Svm40CmdDeviceReset())

    def get_compensation_temperature_offset(self):
        """
        Gets the temperature offset for RHT measurements.

        :return: Temperature offset in degrees celsius.
        :rtype: float
        """
        data = self.execute(Svm40CmdGetTemperatureOffsetForRhtMeasurements())
        # Firmware versions prior to 2.0 will return a float value (4 bytes)
        # and for firmware version >= 2.0 an int16 value (2 bytes) is returned.
        t_offset = None
        if len(data) == 2:
            t_offset = float(unpack('>h', data)[0]) / 200.
        elif len(data) == 4:
            t_offset = float(unpack('>f', data)[0])
        return t_offset

    def set_compensation_temperature_offset(self, t_offset,
                                            send_as_integer=False):
        """
        Sets the temperature offset for RHT measurements.

        .. note:: Execute the command
            :py:meth:`~sensirion_shdlc_svm40.device.store_nv_data` command
            after writing the parameter to store it in the non-volatile memory
            of the device otherwise the parameter will be reset upton a device
            reset.

        :param float t_offset: Temperature offset in degrees celsius.
        :param bool send_as_integer:
            Set to `True` to use the integer format. This option was added for
            firmware version >= 2.0 which will accepted either a float value
            (4 bytes) or an int16 value (2 bytes). Firmware versions prior to
            2.0 will only accept the float format. Float temperature values are
            in degrees celsius with no scaling. Integer temperature
            values are in degrees celsius with a scaling of 200.
        """
        if send_as_integer:
            data = pack('>h', int(round(t_offset * 200)))  # scaled int16
        else:
            data = pack('>f', t_offset)  # float
        self.execute(Svm40CmdSetTemperatureOffsetForRhtMeasurements(data))

    def get_voc_tuning_parameters(self):
        """
        Gets the currently set parameters for customizing the VOC algorithm.

        :return:
            - voc_index_offset (int) -
              VOC index representing typical (average) conditions. The default
              value is 100.
            - learning_time_hours (int) -
              Time constant of long-term estimator in hours. Past events will
              be forgotten after about twice the learning time. The default
              value is 12 hours.
            - gating_max_duration_minutes (int) -
              Maximum duration of gating in minutes (freeze of estimator during
              high VOC index signal). Zero disables the gating. The default
              value is 180 minutes.
            - std_initial (int) -
              Initial estimate for standard deviation. Lower value boosts
              events during initial learning period, but may result in larger
              device-to-device variations. The default value is 50.
        :rtype: tuple
        """
        return self.execute(Svm40CmdGetVocTuningParameters())

    def set_voc_tuning_parameters(self, voc_index_offset, learning_time_hours,
                                  gating_max_duration_minutes, std_initial):
        """
        Sets parameters to customize the VOC algorithm. This command is only
        available in idle mode.

        .. note:: Execute the store command after writing the parameter to
                  store it in the non-volatile memory of the device otherwise
                  the parameter will be reset upton a device reset.

        :param int voc_index_offset:
            VOC index representing typical (average) conditions. The default
            value is 100.
        :param int learning_time_hours:
            Time constant of long-term estimator in hours. Past events will be
            forgotten after about twice the learning time. The default value is
            12 hours.
        :param int gating_max_duration_minutes:
            Maximum duration of gating in minutes (freeze of estimator during
            high VOC index signal). Set to zero to disable the gating. The
            default value is 180 minutes.
        :param int std_initial:
            Initial estimate for standard deviation. Lower value boosts events
            during initial learning period, but may result in larger
            device-to-device variations. The default value is 50.
        """
        self.execute(Svm40CmdSetVocTuningParameters(
            voc_index_offset, learning_time_hours, gating_max_duration_minutes,
            std_initial))

    def store_nv_data(self):
        """
        Stores all customer engine parameters to the non-volatile memory.
        """
        self.execute(Svm40CmdStoreNvData())

    def get_voc_state(self):
        """
        Gets the current VOC algorithm state. Retrieved values can be used to
        set the VOC algorithm state to resume operation after a short
        interruption, skipping initial learning phase. This command is only
        available during measurement mode.

        .. note:: This feature can only be used after at least 3 hours of
                  continuous operation.

        :return: Current VOC algorithm state.
        :rtype: list(int)
        """
        return self.execute(Svm40CmdGetVocState())

    def set_voc_state(self, state):
        """
        Set previously retrieved VOC algorithm state to resume operation after
        a short interruption, skipping initial learning phase. This command is
        only available in idle mode.

        .. note:: This feature should not be used after interruptions of more
                  than 10 minutes.

        :param list(int) state: Current VOC algorithm state.
        """
        self.execute(Svm40CmdSetVocState(state))

    def start_measurement(self):
        """
        Starts continuous measurement in polling mode.

        .. note:: This command is only available in idle mode.
        """
        self.execute(Svm40CmdStartContinuousMeasurement())

    def stop_measurement(self):
        """
        Leaves the measurement mode and returns to the idle mode.

        .. note:: This command is only available in measurement mode.
        """
        self.execute(Svm40CmdStopMeasurement())

    def read_measured_values(self):
        """
        Returns the new measurement results.

        .. note:: This command is only available in measurement mode. The
                  firmware updates the measurement values every second. Polling
                  data with a faster sampling rate will return the same values.
                  The first measurement is available 1 second after the start
                  measurement command is issued. Any readout prior to this will
                  return zero initialized values.

        :return:
            The measured air quality, humidity and temperature.

            - air_quality (:py:class:`~sensirion_shdlc_svm40.response_types.AirQuality`) -
              Air quality response object.
            - humidity (:py:class:`~sensirion_shdlc_svm40.response_types.Humidity`) -
              Humidity response object.
            - temperature (:py:class:`~sensirion_shdlc_svm40.response_types.Temperature`) -
              Temperature response object.
        :rtype:
            tuple
        """  # noqa: E501
        voc, rh, t = self.execute(Svm40CmdReadMeasuredValuesAsIntegers())
        return AirQuality(voc), Humidity(rh), Temperature(t)

    def read_measured_values_raw(self):
        """
        Returns the new measurement results with raw values added.

        .. note:: This command is only available in measurement mode. The
                  firmware updates the measurement values every second. Polling
                  data with a faster sampling rate will return the same values.
                  The first measurement is available 1 second after the start
                  measurement command is issued. Any readout prior to this will
                  return zero initialized values.

        :return:
            The measured air quality, humidity and temperature including the
            raw values without engine compensation.

            - air_quality (:py:class:`~sensirion_shdlc_svm40.response_types.AirQuality`) -
              Air quality response object.
            - humidity (:py:class:`~sensirion_shdlc_svm40.response_types.Humidity`) -
              Humidity response object.
            - temperature (:py:class:`~sensirion_shdlc_svm40.response_types.Temperature`) -
              Temperature response object.
            - raw_voc_ticks (int) -
              Raw VOC output ticks as read from the SGP sensor.
            - raw_humidity (:py:class:`~sensirion_shdlc_svm40.response_types.Humidity`) -
              Humidity response object.
            - raw_temperature (:py:class:`~sensirion_shdlc_svm40.response_types.Temperature`) -
              Temperature response object.
        :rtype:
            tuple
        """  # noqa: E501
        voc, rh, t, raw_voc, raw_rh, raw_t = self.execute(
            Svm40CmdReadMeasuredValuesAsIntegersWithRawParameters())
        return AirQuality(voc), Humidity(rh), Temperature(t), \
            raw_voc, Humidity(raw_rh), Temperature(raw_t)

    def update_firmware(self, image, emergency=False, status_callback=None,
                        progress_callback=None):
        """
        Update the firmware on the device.

        This method allows you to download a new firmware (provided as a
        \\*.hex file) to the device. A device reset is performed after the
        firmware update.

        .. note:: This can take several minutes, don't abort it! If aborted,
                  the device stays in the bootloader and you need to restart
                  the update with ``emergency=True`` to recover.

        :param image:
            The image to flash, either as a
            :py::class:`~sensirion_shdlc_svm40.firmware_image.Svm40FirmwareImage`
            object, a file-like object, or the filename (``str``) to the
            \\*.hex file.
        :param bool emergency:
            Must be set to ``True`` if the device is already in bootloader
            mode, ``False`` otherwise.
        :param callable status_callback:
            Optional callback for status report, taking a string as parameter.
        :param callable progress_callback:
            Optional callback for progress report, taking a float as parameter
            (progress in percent).
        :raises ~sensirion_shdlc_driver.errors.ShdlcFirmwareImageIncompatibilityError:
            If the image is not compatible with the connected device.
        :raises Exception:
            On other errors.
        """  # noqa: E501
        if not isinstance(image, Svm40FirmwareImage):
            image = Svm40FirmwareImage(image)
        update = ShdlcFirmwareUpdate(self, image,
                                     status_callback=status_callback,
                                     progress_callback=progress_callback)
        update.execute(emergency=emergency)
