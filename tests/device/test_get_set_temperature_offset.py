# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("t_offset", [
    (-1.),
    (1.),
    (0.),
])
def test(device, t_offset):
    """
    Test if get_compensation_temperature_offset() and
    set_compensation_temperature_offset() works as expected.
    """
    initial_value = device.get_compensation_temperature_offset()
    device.set_compensation_temperature_offset(t_offset)
    assert device.get_compensation_temperature_offset() == t_offset

    # reset device and check that the value was not stored in the nv-memory
    device.device_reset()
    assert device.get_compensation_temperature_offset() == initial_value


@pytest.mark.needs_device
@pytest.mark.parametrize("t_offset", [
    (-1.),
    (1.),
    (0.),
])
def test_nv(device, t_offset):
    """
    Test if store_nv_data() works as expected.
    """
    device.set_compensation_temperature_offset(t_offset)
    device.store_nv_data()
    assert device.get_compensation_temperature_offset() == t_offset

    # reset device and check that the value was stored in the nv-memory
    device.device_reset()
    assert device.get_compensation_temperature_offset() == t_offset
