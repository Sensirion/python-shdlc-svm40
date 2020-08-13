# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if get_product_name() returns the expected value.
    """
    product_name = device.get_product_name()
    assert type(product_name) is str
