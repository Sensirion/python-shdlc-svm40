# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcFirmwareImage

import logging
log = logging.getLogger(__name__)


class Svm40FirmwareImage(ShdlcFirmwareImage):
    """
    SVM40 firmware image.

    This class represents a firmware image for the SVM40 device. It is used to
    load and verify Intel-Hex files for performing firmware updates over SHDLC.
    """

    def __init__(self, hexfile):
        """
        Constructor which loads and parses the firmware from a hex file.

        :param str/file hexfile:
            The filename or file-like object containing the firmware in
            Intel-Hex format (\\*.hex).
        :raise ~sensirion_shdlc_driver.errors.ShdlcFirmwareImageSignatureError:
            If the signature of the image is invalid.
        """
        super(Svm40FirmwareImage, self).__init__(
            hexfile, bl_start_addr=0x8000000, app_start_addr=0x8001000,
            signature=b'\x3C\x42\x4C\x2E\x53\x49\x47\x3E',
            bl_version_offset=0x0200)
