# XBEE-MATRIX Project

This is a work in progress to write a driver for sure electronics LED matrices.
Final objective is to have a 96x16 display which can be controlled wirelessly via ZigBee (using XBee modules).

## Current status

The hardware currently accepts raw data through the serial port to display on the device.

A basic python test script sends some data continuously to the matrix at maximum attainable speed with the current hardware (approx 15 fps) which is mostly limited by the data rate of the serial connection
