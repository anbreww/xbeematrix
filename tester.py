#!/bin/python

import serial
import time
from font import font

buffer_size = 24*8
offset = 0

# build font dictionary
fdict = dict()
for i in range(len(font)):
    fdict[chr(ord('a')+i)] = [chr(c) for c in font[i]]



s = serial.Serial('/dev/ttyUSB0', 38400, timeout=0,
        parity=serial.PARITY_NONE)

buffer = list(buffer_size*chr(offset))

for j in range(10000):
    buffer[-1] = chr(offset)

    while(s.read() != 'R'):
        s.write('A')
        time.sleep(0.001)

#send start byte
    s.write('s')

    nextchar = s.read()
    while(nextchar == ''):
        nextchar = s.read()

    if nextchar == 'K':
        #print("target confirmed. sending size")
        s.write(chr(buffer_size))
    else:
        print("ERROR: " + nextchar)

    #time.sleep(0.001)

    #size = s.readline()

    #print("size confirmed : %d (sent %d)" % (int(size), buffer_size))

    #buffer[0:10:2] = [chr(c) for c in font[0]]
    buffer[0:-1:2] = [chr(0) for i in buffer[0:-1:2]]
    #buffer[1:-1:2] = [chr(0) for i in buffer[1:-1:2]]


    for i in range(0,192,12):
        buffer[i:i+10:2] = fdict[chr(ord('a')+(i/12+offset/12)%46)]

    fillchar = 0xff if (4*j) % (2*buffer_size) < buffer_size else 0x00
    buffer[-(4*j+1)%192] = chr(fillchar)
    buffer[-(4*j+3)%192] = chr(fillchar)
    buffer_str = ''.join(buffer)
    s.write(buffer_str)

    #for i in range(buffer_size/16):
        #s.write(chr(i+offset))
        #s.write("abcdefghijklmnop")

    offset += 2
    offset %= 255

s.close()
