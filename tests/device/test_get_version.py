# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver.types import Version
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if get_version() returns the expected value.
    """
    version = device.get_version()
    assert type(version) is Version
    assert version.firmware.major >= 0
    assert version.firmware.minor >= 0
    assert version.firmware.debug in [True, False]
    assert version.hardware.major >= 1
    assert version.hardware.minor >= 0
    assert version.protocol.major == 1
    assert version.protocol.minor == 0
