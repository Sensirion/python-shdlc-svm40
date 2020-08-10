# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

##############################################################################
##############################################################################
#                 _____         _    _ _______ _____ ____  _   _
#                / ____|   /\  | |  | |__   __|_   _/ __ \| \ | |
#               | |       /  \ | |  | |  | |    | || |  | |  \| |
#               | |      / /\ \| |  | |  | |    | || |  | | . ` |
#               | |____ / ____ \ |__| |  | |   _| || |__| | |\  |
#                \_____/_/    \_\____/   |_|  |_____\____/|_| \_|
#
#     THIS FILE IS AUTOMATICALLY GENERATED AND MUST NOT BE EDITED MANUALLY!
#
# Generator:    sensirion-shdlc-interface-generator 0.6.1
# Product:      SVM40
# Version:      0.2.0
#
##############################################################################
##############################################################################

# flake8: noqa

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver.command import ShdlcCommand
from struct import pack, unpack

import logging
log = logging.getLogger(__name__)


class Svm40CmdReadMeasuredValuesBase(ShdlcCommand):
    """
    SHDLC command 0x03: "Read Measured Values".
    """

    def __init__(self, *args, **kwargs):
        super(Svm40CmdReadMeasuredValuesBase, self).__init__(
            0x03, *args, **kwargs)


class Svm40CmdReadMeasuredValuesAsIntegers(Svm40CmdReadMeasuredValuesBase):

    def __init__(self):
        """
        Read Measured Values As Integers Command

        Returns the new measurement results as integers.

        .. note:: This command is only available in measurement mode. The
                  firmware updates the measurement values every second. Polling
                  data with a faster sampling rate will return the same values.
                  The first measurement is available 1 second after the start
                  measurement command is issued. Any readout prior to this will
                  return zero initialized values.
        """
        super(Svm40CmdReadMeasuredValuesAsIntegers, self).__init__(
            data=b"".join([bytes(bytearray([0x0A]))]),
            max_response_time=0.1,
            post_processing_time=0.0,
            min_response_length=6,
            max_response_length=6
        )

    @staticmethod
    def interpret_response(data):
        """
        :return:
            - voc_index (int) -
              VOC engine output in ppb with a scaling value of 10.
            - humidity (int) -
              Compensated ambient humidity in % RH with a scaling factor of
              100.
            - temperature (int) -
              Compensated ambient temperatur in degrees celsius with a scaling
              of 200.
        :rtype: tuple
        """
        voc_index = int(unpack(">h", data[0:2])[0])  # int16
        humidity = int(unpack(">h", data[2:4])[0])  # int16
        temperature = int(unpack(">h", data[4:6])[0])  # int16
        return voc_index,\
            humidity,\
            temperature


class Svm40CmdReadMeasuredValuesAsIntegersWithRawParameters(Svm40CmdReadMeasuredValuesBase):

    def __init__(self):
        """
        Read Measured Values As Integers With Raw Parameters Command

        Returns the new measurement results as integers with raw values added.

        .. note:: This command is only available in measurement mode. The
                  firmware updates the measurement values every second. Polling
                  data with a faster sampling rate will return the same values.
                  The first measurement is available 1 second after the start
                  measurement command is issued. Any readout prior to this will
                  return zero initialized values.
        """
        super(Svm40CmdReadMeasuredValuesAsIntegersWithRawParameters, self).__init__(
            data=b"".join([bytes(bytearray([0x0B]))]),
            max_response_time=0.1,
            post_processing_time=0.0,
            min_response_length=12,
            max_response_length=12
        )

    @staticmethod
    def interpret_response(data):
        """
        :return:
            - voc_index (int) -
              VOC engine output in ppb with a scaling value of 10.
            - humidity (int) -
              Compensated ambient humidity in % RH with a scaling factor of
              100.
            - temperature (int) -
              Compensated ambient temperatur in degrees celsius with a scaling
              of 200.
            - raw_voc_ticks (int) -
              Raw VOC output ticks as read from the SGP sensor.
            - raw_humidity (int) -
              Uncompensated raw humidity in % RH as read from the SHT40 with a
              scaling factor of 100.
            - raw_temperature (int) -
              Uncompensated raw temperatur in degrees celsius as read from the
              SHT40 with a scaling of 200.
        :rtype: tuple
        """
        voc_index = int(unpack(">h", data[0:2])[0])  # int16
        humidity = int(unpack(">h", data[2:4])[0])  # int16
        temperature = int(unpack(">h", data[4:6])[0])  # int16
        raw_voc_ticks = int(unpack(">H", data[6:8])[0])  # uint16
        raw_humidity = int(unpack(">h", data[8:10])[0])  # int16
        raw_temperature = int(unpack(">h", data[10:12])[0])  # int16
        return voc_index,\
            humidity,\
            temperature,\
            raw_voc_ticks,\
            raw_humidity,\
            raw_temperature
