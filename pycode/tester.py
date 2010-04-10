#!/bin/python

import serial
import time
import formatting as f
from lcdfont import font

import os
import threading

import curses

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
curses.curs_set(0) # hide cursor
#curses.keypad(1)

buffer_size = 24*8
offset = 0
buffer_limit = 48*4 # soft limit for testing purposes
total_columns = 96

class InputThread(threading.Thread):
    '''Check user input on curses'''
    def run(self):
        #stdscr.addstr(17,0,"Thread running")
        stdscr.refresh()
        while 1:
            c = stdscr.getch()
            if c == ord('q'):
                terminate()


# build font dictionary
fdict = dict()
for i in range(len(font)):
    fdict[chr(ord(' ')+i)] = font[i]

fdict[' '] = (0,0,0)


s = serial.Serial('/dev/ttyUSB0', 38400, timeout=0,
        parity=serial.PARITY_NONE)


buffer = [0 for i in range(buffer_size*3)]
global text 

DEBUG = None

def debugprint(str):
    if(DEBUG):
        print(str)

def make_word(string):
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
    if end > len(buffer):
        end = len(buffer)
    buffer[begin:end:2] = list[:(end-begin/2)/2]

def compute_breakpos(string, length=96):
    '''Returns index of line break for a given string
    If string occupies less than [length], return 0'''
    buf = []
    for i in range(len(string)):
        buf.extend(make_word(string[i]))
        if len(buf) > length:
            return i
    return None

def roll(string, direction='left', padding=0, padchar=' '):
    s = string
    if direction == 'left':
        i = 1
    else:
        i = -1
    return ''.join( [ s[i:],s[:i] ] )


def text_to_buffer(string, startcol=0, startrow='top', linebreak=True):
    index = None
    if linebreak:
        index = compute_breakpos(string,total_columns-startcol)
    word = make_word(string[:index])
    list_to_buffer(word, startcol, startrow)
    if linebreak and startrow=='top':
        word = make_word(string[index:])
        list_to_buffer(word, startcol, row='bottom')

def scroll_buffer(direction='left'):
    if direction == 'left':
        buffer.append(buffer.pop(0))
        buffer.append(buffer.pop(0))
    else:
        buffer.insert(0, buffer.pop())
        buffer.insert(0, buffer.pop())




def update_buffer(iteration):
    #buffer[191] = (iteration%255)
    #buffer[0:10:2] = fdict['a']
    if (iteration % 64 > -1):
        #text_to_buffer("  Robopoly 2010, le jeu du vivapoly youpie   ")

        global text
        if(iteration < 2):
            global text
            text = "Here is a really long paragraph of text yayz"
            text_to_buffer(text, linebreak=False)
            text = "This here is the second line!"
            text_to_buffer(text, startrow='bottom',linebreak=False)
        #text = roll(text, 'Right')
        #text_to_buffer("{0:<15d}        ".format(iteration**2), 0, 'bottom')
    scroll_buffer('left')
    scroll_buffer('left')
    #else:
    #    text_to_buffer("     Bienvenue a           ")
    #    text_to_buffer("       VIVAPOLY        ", 0, 'bottom')
    #buffer[190] = (iteration%255)

    #os.system("clear")
    lines = []
    lines= f.return_list(buffer[:192:2])
    lines.append("")
    lines.extend(f.return_list(buffer[1:192:2]))
    ypos = 0
    for line in lines:
        stdscr.addstr(ypos,0,line, curses.A_BOLD)
        ypos += 1

    stdscr.refresh()

def terminate():
    s.close()

    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
    raise SystemExit






if __name__ == '__main__':
    InputThread().start()
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

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
