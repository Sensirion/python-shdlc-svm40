# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("parameters", [
    (-30., 250, 72, 720, 500),  # max allowed values
    (30., 1, 1, 0, 10),         # min allowed values
    (0., 100, 12, 180, 50),     # default values
])
def test_nv(device, parameters):
    """
    Test if store_nv_data() works as expected.
    """
    device.set_compensation_temperature_offset(parameters[0])
    device.set_voc_tuning_parameters(
        parameters[1], parameters[2], parameters[3], parameters[4])
    device.store_nv_data()
    assert device.get_compensation_temperature_offset() == parameters[0]
    voc_index_offset, learning_time_hours, gating_max_duration_minutes, \
        std_initial = device.get_voc_tuning_parameters()
    assert voc_index_offset == parameters[1]
    assert learning_time_hours == parameters[2]
    assert gating_max_duration_minutes == parameters[3]
    assert std_initial == parameters[4]

    # reset device and check that the value was stored in the nv-memory
    device.device_reset()
    assert device.get_compensation_temperature_offset() == parameters[0]
    voc_index_offset, learning_time_hours, gating_max_duration_minutes, \
        std_initial = device.get_voc_tuning_parameters()
    assert voc_index_offset == parameters[1]
    assert learning_time_hours == parameters[2]
    assert gating_max_duration_minutes == parameters[3]
    assert std_initial == parameters[4]
