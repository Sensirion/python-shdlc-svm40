# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if get_serial_number() returns the expected value.
    """
    serial_number = device.get_serial_number()
    assert type(serial_number) is str
    assert len(serial_number) == 24
