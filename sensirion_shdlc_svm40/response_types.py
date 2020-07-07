# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

import logging
log = logging.getLogger(__name__)


class AirQuality(object):
    """
    Represents a measurement response for the air quality.

    With the :py:attr:`ticks` you can access the raw data as received from the
    device. For the converted value the :py:attr:`voc_index` attribute is
    available.
    """
    def __init__(self, ticks):
        """
        Creates an instance from the received raw data.

        :param int ticks:
            The read ticks as received from the device.
        """
        super(AirQuality, self).__init__()

        #: The ticks (int) as received from the device.
        self.ticks = ticks

        #: The converted VOC index.
        self.voc_index = ticks / 10.

    def __str__(self):
        return 'VOC index = {:.1f}'.format(self.voc_index)


class Humidity(object):
    """
    Represents a measurement response for the humidity.

    With the :py:attr:`ticks` you can access the raw data as received from the
    device. For the converted value the :py:attr:`percent_rh` attribute is
    available.
    """
    def __init__(self, ticks):
        """
        Creates an instance from the received raw data.

        :param int ticks:
            The read ticks as received from the device.
        """
        super(Humidity, self).__init__()

        #: The ticks (int) as received from the device.
        self.ticks = ticks

        #: The converted humidity in %RH.
        self.percent_rh = ticks / 100.

    def __str__(self):
        return '{:0.1f} %RH'.format(self.percent_rh)


class Temperature(object):
    """
    Represents a measurement response for the temperature.

    With the :py:attr:`ticks` you can access the raw data as received from the
    device. For the converted values you can choose between
    :py:attr:`degrees_celsius` and :py:attr:`degrees_fahrenheit`.
    """
    def __init__(self, ticks):
        """
        Creates an instance from the received raw data.

        :param int ticks:
            The read ticks as received from the device.
        """
        super(Temperature, self).__init__()

        #: The ticks (int) as received from the device.
        self.ticks = ticks

        #: The converted temperature in °C.
        self.degrees_celsius = ticks / 200.

        #: The converted temperature in °F.
        self.degrees_fahrenheit = self.degrees_celsius * 9. / 5. + 32.

    def __str__(self):
        return '{:0.1f} °C'.format(self.degrees_celsius)
