#!/bin/python

import serial
import time
from font import font

buffer_size = 24*8
offset = 0
buffer_limit = 48*4 # soft limit for testing purposes

# build font dictionary
fdict = dict()
for i in range(len(font)):
    fdict[chr(ord('a')+i)] = font[i]


s = serial.Serial('/dev/ttyUSB0', 38400, timeout=0,
        parity=serial.PARITY_NONE)


buffer = range(buffer_size)

DEBUG = None

def debugprint(str):
    if(DEBUG):
        print(str)

def update_buffer(iteration):
    buffer[10] = (iteration%255)

iter = 0
# main program loop
while 1:
    iter += 1

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
        #s.write(chr(buffer_size))
        s.write(chr(buffer_limit))
    else:
        print("ERROR: " + nextchar)

    #time.sleep(0.001)

    #size = s.readline()

    #print("size confirmed : %d (sent %d)" % (int(size), buffer_size))

    update_buffer(iter)

    buffer_str = ''.join([chr(c) for c in buffer[0:buffer_limit]])
    s.write(buffer_str)

    #for i in range(buffer_size/16):
        #s.write(chr(i+offset))
        #s.write("abcdefghijklmnop")

    offset += 2
    offset %= 255

s.close()
