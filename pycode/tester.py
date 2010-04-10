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

fdict[' '] = (0,0)


s = serial.Serial('/dev/ttyUSB0', 38400, timeout=0,
        parity=serial.PARITY_NONE)


buffer = range(buffer_size)

DEBUG = None

def debugprint(str):
    if(DEBUG):
        print(str)

def makeword(string):
    '''Return a list of bytes with characters and spaces'''
    outlist = []
    for c in string:
        outlist.extend(fdict[c])
        outlist.append(0)
    return outlist

def list_to_buffer(list, startcol=0, row='top'):
    '''Write a list to buffer on one line''' 
    row = 0 if row == 'top' else 1
    begin = startcol*2 + row
    end = begin+2*len(list)
    buffer[begin:end:2] = list



def update_buffer(iteration):
    buffer[190] = (iteration%255)
    buffer[191] = (iteration%255)
    buffer[0:10:2] = fdict['a']
    list_to_buffer(makeword("robopoly \x7f"))
    list_to_buffer(makeword("my name is andrew "), 0, 'bottom')





iter = 0
# main program loop
while 1:
    iter += 1

    # wait until matrix is ready to receive data
    while(s.read() != 'R'):
        s.write('A')
        time.sleep(0.0001)

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
