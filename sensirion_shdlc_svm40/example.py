# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_svm40 import Svm40ShdlcDevice
import time

import logging
log = logging.getLogger(__name__)


def main():
    # Connect to the device with default settings:
    #  - baudrate:      115200
    #  - slave address: 0
    with ShdlcSerialPort(port='COM1', baudrate=115200) as port:
        device = Svm40ShdlcDevice(ShdlcConnection(port), slave_address=0)
        print("Resetting device... ")
        device.device_reset()

        # Print some device information
        print("Version: {}".format(device.get_version()))
        print("Product Name: {}".format(device.get_product_name()))
        print("Serial Number: {}".format(device.get_serial_number()))

        # Measure
        device.start_measurement()
        print("Measurement started... ")
        while True:
            time.sleep(10.)
            air_quality, humidity, temperature = device.read_measured_values()
            # use default formatting for printing output:
            print("{}, {}, {}".format(air_quality, humidity, temperature))
            # custom printing of attributes:
            print(". VOC index = {} (received int16 = {}) ".format(
                air_quality.voc_index, air_quality.ticks))
            print(". Humidity = {:0.2f} %RH (received int16 = {})".format(
                humidity.percent_rh, humidity.ticks))
            print(". Temperature = {:0.2f} °C (received int16 = {})".format(
                temperature.degrees_celsius, temperature.ticks))


if __name__ == "__main__":
    main()
