# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if get_voc_state() and set_voc_state() work as expected.
    """
    device.start_measurement()
    state = device.get_voc_state()
    assert type(state) == list
    assert len(state) == 8

    device.stop_measurement()
    device.set_voc_state(state)
