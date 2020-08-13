# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_svm40.response_types import AirQuality, Humidity, \
    Temperature
from sensirion_shdlc_svm40.device_errors import \
    Svm40CommandNotAllowedInCurrentState
import pytest
import time


@pytest.mark.needs_device
def test(device):
    """
    Test if read_measured_values() returns the expected values.
    """
    device.start_measurement()
    time.sleep(1.)

    # check the read values
    air_quality, humidity, temperature = device.read_measured_values()
    assert type(air_quality) is AirQuality
    assert type(air_quality.voc_index) is float
    assert type(humidity) is Humidity
    assert type(humidity.ticks) is int
    assert type(humidity.percent_rh) is float
    assert type(temperature) is Temperature
    assert type(temperature.ticks) is int
    assert type(temperature.degrees_celsius) is float
    assert type(temperature.degrees_fahrenheit) is float
    # use default formatting for printing output:
    print("{}, {}, {}".format(air_quality, humidity, temperature))

    # stop the measurement and check for proper exception if called again
    device.stop_measurement()
    with pytest.raises(Svm40CommandNotAllowedInCurrentState):
        device.read_measured_values()


@pytest.mark.needs_device
def test_initial_state(device):
    """
    Test if read_measured_values() returns the expected
    exception if called without starting the measurement first.
    """
    with pytest.raises(Svm40CommandNotAllowedInCurrentState):
        device.read_measured_values()
