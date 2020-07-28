# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcDevice, ShdlcFirmwareUpdate
from .device_errors import SVM40_DEVICE_ERROR_LIST
from .firmware_image import Svm40FirmwareImage
from .commands import \
    Svm40CmdStartContinuousMeasurement, \
    Svm40CmdStopMeasurement, \
    Svm40CmdReadMeasuredValuesAsIntegers, \
    Svm40CmdReadMeasuredValuesAsIntegersWithRawParameters, \
    Svm40CmdGetTOffset, Svm40CmdSetTOffset, Svm40CmdStoreNvData
from .response_types import AirQuality, Humidity, Temperature

import logging
log = logging.getLogger(__name__)


class Svm40ShdlcDevice(ShdlcDevice):
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

    def get_compensation_temperature_offset(self):
        """
        Gets the customer temperature offset which is used for the
        compensation.

        :return: Customer temperature offset in degrees celsius.
        :rtype: float
        """
        return self.execute(Svm40CmdGetTOffset())

    def set_compensation_temperature_offset(self, t_offset):
        """
        Sets the customer temperature offset which is used for the
        compensation.

        .. note:: Execute the command
            :py:meth:`~sensirion_shdlc_svm40.device.store_nv_data` command
            after writing the parameter to store it in the non-volatile memory
            of the device otherwise the parameter will be reset upton a device
            reset.

        :param float t_offset:
            Customer temperature offset in degrees celsius.
        """
        self.execute(Svm40CmdSetTOffset(t_offset))

    def store_nv_data(self):
        """
        Stores all customer engine parameters to the non-volatile memory.
        """
        self.execute(Svm40CmdStoreNvData())

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
