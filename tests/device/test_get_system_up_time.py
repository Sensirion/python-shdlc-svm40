# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if get_system_up_time() returns the expected value.
    """
    uptime = device.get_system_up_time()
    assert type(uptime) is int
    assert uptime >= 0
