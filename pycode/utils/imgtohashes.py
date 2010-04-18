#!/usr/bin/python
'''
Convert images to hashes.

This script takes a 1 bit (black and white) indexed image as input and outputs
a list of hashes and spaces, for use with the led matrix drivers

'''
import Image
import sys


if len(sys.argv) < 2:
    sys.stderr.write("Error: you must specify name of file to convert\n")
    raise SystemExit

im = Image.open(sys.argv[1])

(imx,imy) = im.size

line = ''

for y in range(imy):
    for x in range(imx):
        line = line + ('#' if im.getpixel((x,y)) != 1 else ' ')
    print line
    line = ''
