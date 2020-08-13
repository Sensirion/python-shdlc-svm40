# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if get_product_type() returns the expected value.
    """
    product_type = device.get_product_type()
    assert type(product_type) is str
    assert product_type == "00140000"
