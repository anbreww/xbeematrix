#!/bin/python

import serial
import signal
import time
import formatting as form
from lcdfont import font
import mpd

import os
import threading

import curses

#curses.keypad(1)

buffer_size = 24*8
buffer_limit = 48*4 # soft limit for testing purposes
total_columns = 96

class InputThread(threading.Thread):
    '''Listen for keyboard input.

    Currently only implements 'q' for exit'''

    def run(self):
        #stdscr.addstr(17,0,"Thread running")
        m.stdscr.refresh()
        while 1:
            c = m.stdscr.getch()
            if c == ord('q'):
                m.terminate()


DEBUG = None

class Matrix():
    '''Wrapper for Quad matrix.

    set sim=False to disable terminal output
    set ser=False to disable output to matrix (simulation mode)
    '''
    num_panels=4
    lines_per_panel=2
    panel_size=24*num_panels*lines_per_panel
    buffer_size=panel_size*3

    s_title=""
    s_artist=""

    #fdict=dict() # font dictionary

    buffer = []
    
    def __init__(self, sim=True, ser=True):
        '''Initialize a matrix module with serial communication and font lookup
        table
        '''
        self.buffer_size=self.panel_size*3
        self._build_font()
        self.buffer = [0 for i in range(self.buffer_size)]
        self.sim = sim
        self.ser = ser
        self.finished = False
        
        if self.ser:
            self.s = serial.Serial('/dev/ttyUSB0', 38400, timeout=0,
                                    parity=serial.PARITY_NONE)
        if self.sim:
            self.stdscr = curses.initscr()
            curses.start_color()
            curses.use_default_colors()
            curses.cbreak()
            curses.noecho()
            curses.curs_set(0) # hide cursor
            self.mpad = curses.newpad(17,98)
        else:
            print("Disabled simulator output")

    def set_buffer_size(self,new_size):
        self.buffer_size=new_size
        self.buffer = [0 for i in range(self.buffer_size)]

    def __del__(self):
        #self.s.close()
        pass

    def close(self):
        '''Close all open connections'''
        if self.ser:
            self.s.close()
        self.finished = True

    def _build_font(self,fnt='default'):
        '''Parse font from a file and populate dictionary'''
        self.fdict = dict()
        for i in range(len(font)):
            self.fdict[chr(ord(' ')+i)] = font[i]

        self.fdict[' '] = (0,0,0) # override space to make it smaller


    def list_to_buffer(self, list, startcol=0, row='top'):
        '''Write a list to buffer on one line''' 
        row = 0 if row == 'top' else 1
        begin = startcol*2 + row
        end = begin+2*len(list)
        if end > len(self.buffer):
            end = len(self.buffer)
        self.buffer[begin:end:2] = list[:(end-begin/2)/2]

    def compute_breakpos(self, string, length=96):
        '''Returns index of line break for a given string
        If string occupies less than [length], return 0'''
        buf = []
        for i in range(len(string)):
            buf.extend(f.make_word(string[i], self.fdict))
            if len(buf) > length:
                return i
        return None

    def roll(self, string, direction='left', padding=0, padchar=' '):
        s = string
        if direction == 'left':
            i = 1
        else:
            i = -1
        return ''.join( [ s[i:],s[:i] ] )


    def text_to_buffer(self, string, startcol=0, startrow='top', linebreak=True):
        index = None
        if linebreak:
            index = self.compute_breakpos(string,total_columns-startcol)
        word = f.make_word(string[:index], self.fdict)
        self.list_to_buffer(word, startcol, startrow)
        if linebreak and startrow=='top':
            word = f.make_word(string[index:], self.fdict)
            self.list_to_buffer(word, startcol, row='bottom')

    def scroll_buffer(self, direction='left'):
        if direction == 'left':
            self.buffer.append(self.buffer.pop(0))
            self.buffer.append(self.buffer.pop(0))
        else:
            self.buffer.insert(0, self.buffer.pop())
            self.buffer.insert(0, self.buffer.pop())

    def get_buffer(self):
        return self.buffer

    def set_buffer(self, newbuffer):
        self.buffer = newbuffer

    def terminate(self):
        self.close()
        if self.sim:
            curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
            curses.endwin()
        os.sys.exit()


    def refresh(self):
        if self.ser == False:
            time.sleep(0.03)
            return
        # wait until matrix is ready to receive data
        while(self.s.read() != 'R'):
            self.s.write('A')
            time.sleep(0.0001)

        #send start byte
        self.s.write('s')

        nextchar = self.s.read()
        while(nextchar == ''):
            nextchar = self.s.read()

        if nextchar == 'K':
            #print("target confirmed. sending size")
            #s.write(chr(buffer_size))
            self.s.write(chr(buffer_limit))
        else:
            print("ERROR: " + nextchar)

        #time.sleep(0.001)

        #size = s.readline()

        #print("size confirmed : %d (sent %d)" % (int(size), buffer_size))


        buffer_str = ''.join([chr(c) for c in self.buffer[0:buffer_limit]])
        self.s.write(buffer_str)



s_title = ""
s_artist = ""

def sec_to_hms(s):
    s = int(s)
    h = s/3600
    s -= 3600*h
    m = s/60
    s -= 60*m

    if h > 0:
        return "%2s:%s:%s" % (h, m, s)
    else:
        return "%d:%02d" % (m,s)

def update_buffer(iteration):
    #buffer[191] = (iteration%255)
    #buffer[0:10:2] = fdict['a']
    #if (iteration % 64 > -1):
        #text_to_buffer("  Robopoly 2010, le jeu du vivapoly youpie   ")

    if(iteration < 2):
        m.set_buffer_size(int(m.panel_size*3))
        #text = "I can display long lines of text on here :)"
            #m.text_to_buffer(text, linebreak=False)
            #text = "      @  And I can write on two lines!  @"
            #m.text_to_buffer(text, startrow='bottom',linebreak=False)
        #text = roll(text, 'Right')
        #text_to_buffer("{0:<15d}        ".format(iteration**2), 0, 'bottom')
    m.scroll_buffer('left')
    m.scroll_buffer('left')
    #else:
    #    text_to_buffer("     Bienvenue a           ")
    #    text_to_buffer("       VIVAPOLY        ", 0, 'bottom')
    #buffer[190] = (iteration%255)
    song = mpdclient.currentsong()
    if(song['title'] != m.s_title or song['artist'] != m.s_artist):
        m.s_title = song['title']
        m.s_artist = song['artist']
        m.set_buffer_size((len(m.s_title)+len(m.s_artist))*14+30)
        m.text_to_buffer("{1:} - {0:<20}".format(m.s_title, m.s_artist), linebreak=False)
        #m.text_to_buffer("{0:<20s}".format(song['artist']), linebreak=False)
        #m.text_to_buffer("{0:<25s}".format(song['title']), linebreak=False, startrow='bottom')
    t = tuple(mpdclient.status()['time'].split(':'))
    timestat = "{0} / {1}".format(sec_to_hms(t[0]), sec_to_hms(t[1]))
    n = len(timestat)
    n = str((96-n*6)/10+n+1)
    timestat = ''.join(["{0:>",n,"}"]).format(timestat)
    m.text_to_buffer(timestat , startrow='bottom')

    #os.system("clear")
    if m.sim:
        m.stdscr.erase()
        m.stdscr.border()
        (winy, winx) = m.stdscr.getmaxyx()
        (pady, padx) = m.mpad.getmaxyx()
        if pady >= winy :
            pady = winy-1
        if padx >= winx :
            padx = winx-1
        pady0 = (winy-pady)/2
        padx0 = (winx-padx)/2



        #if (winy < 18 or winx < 98):
        #    m.stdscr.addstr(1,1,"Terminal too small!")
        #else:
        lines = []
        lines= f.return_list(m.get_buffer()[:192:2])
        lines.append("")
        lines.extend(f.return_list(m.get_buffer()[1:192:2]))
        ypos = 1
        for line in lines:
            #m.stdscr.addstr(ypos,1,line,  curses.color_pair(1) | curses.A_BOLD)
            m.mpad.addstr(ypos,1,line,  curses.color_pair(1) | curses.A_BOLD)
            ypos += 1
        m.mpad.border()
        centered_status("LED Matrix Controller - Andrew Watson - 2010")
        #mpdclient.connect('localhost',6600)
        m.stdscr.refresh()
        m.mpad.refresh( 0,0, pady0, padx0, pady0+pady, padx0+padx)


def centered_status(statusmsg):
    (winy, winx) = m.mpad.getmaxyx()
    status = "[ " + statusmsg + " ]"
    m.mpad.addstr(winy-1,(winx-len(status))/2,status, curses.color_pair(0) |
            curses.A_BOLD)

def sigwinch_handler(n, frame):
    curses.endwin()
    m.stdscr = curses.initscr()



if __name__ == '__main__':
    m = Matrix(sim=True,ser=True)
    f = form.Formatter(m.fdict)

    mpdclient = mpd.MPDClient()
    mpdclient.connect('localhost',6600)

    if m.sim:
        InputThread().start()

        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(66, -1, curses.COLOR_WHITE)

        signal.signal(signal.SIGWINCH, sigwinch_handler)

    iter = 0
    # main program loop
    while 1:
        iter += 1

        time.sleep(0.05)
        update_buffer(iter)
        m.refresh()

        #if m.finished:
            #os.sys.exit()



#curses.nocbreak(); m.stdscr.keypad(0); curses.echo()
#curses.endwin()
