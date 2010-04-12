#!/bin/python

#import signal
import time

# local modules
import formatting as form
import ledmatrix
from lcdfont import font
import mpdinfo

#import mpd

import os
import sys
import threading

import curses


class InputThread(threading.Thread):
    '''Listen for keyboard input.

    Currently only implements 'q' for exit'''

    def run(self):
        #stdscr.addstr(17,0,"Thread running")
        #ui.stdscr.refresh()
        while 1:
            c = ui.stdscr.getch()
            if c == ord('q'):
                break
        ui.terminate()
        m.close()


class Interface():
    '''Contains all UI-related tasks'''

    statusstring = "LED Matrix Controller | Andrew Watson | Robopoly - 2010"

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0) # hide cursor
        self.mpad = curses.newpad(17,98)
        self.init_colors()

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(66, -1, curses.COLOR_WHITE)


    def terminate(self):
        '''kill graphical interface and exit program'''
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()
        sys.exit()

    def centered_status(self,statusmsg, win=None, color=None):
        '''print a centered message at bottom of pad'''
        white_bold = curses.color_pair(0) 
        if not win:
            win = self.mpad
        if not color:
            color = curses.color_pair(0) | curses.A_BOLD
        (winy, winx) = win.getmaxyx()
        status = statusmsg 
        leftx = (winx-len(status))/2+2
        rightx = (winx+len(status))/2+2
        win.addstr(winy-1,leftx-2, "[ ", white_bold)
        win.addstr(winy-1,rightx, " ]", white_bold)
        win.addstr(winy-1,leftx,status, color | curses.A_BOLD)

    def update(self):
        '''update curses ui

        Creates a main window with a border and status line.
        Adds a curses pad in the middle of the window to hold the matrix
        simulator. This should help avoid some problems with terminal sizes.
        '''
        self.stdscr.erase()
        self.stdscr.border()
        (winy, winx) = self.stdscr.getmaxyx()
        (pady, padx) = self.mpad.getmaxyx()
        if pady >= winy :
            pady = winy-1
        if padx >= winx :
            padx = winx-1
        pady0 = (winy-pady)/2
        padx0 = (winx-padx)/2

        lines = []
        lines= f.return_list(m.get_buffer()[:192:2])
        lines.append("")
        lines.extend(f.return_list(m.get_buffer()[1:192:2]))
        ypos = 1
        for line in lines:
            self.mpad.addstr(ypos,1,line,  curses.color_pair(1) | curses.A_BOLD)
            ypos += 1
        self.mpad.border()
        #self.centered_status("LED Matrix Controller - Andrew Watson - 2010")
        #self.centered_status("Robopoly", self.stdscr, curses.color_pair(1))
        self.centered_status(self.statusstring , self.stdscr)

        #mpdclient.connect('localhost',6600)
        self.stdscr.refresh()
        self.mpad.refresh( 0,0, pady0, padx0, pady0+pady, padx0+padx)







def update_buffer(iteration):

    if(iteration < 2):
        m.set_buffer_size(int(m.panel_size*3))

    if(iteration % 2 == 0):
        m.scroll_buffer('left')
        m.scroll_buffer('left')

    
    nowplaying = mpdi.get_nowplaying()
    if mpdi.haschanged:
        m.set_buffer_size(len(nowplaying)*14+30)
        m.text_to_buffer(nowplaying, linebreak=False)

    m.text_to_buffer(mpdi.get_timestring(), startrow='bottom')

    #os.system("clear")
    if m.sim:
        ui.update()


if __name__ == '__main__':
    ENABLE_SIMULATOR = True
    ENABLE_SERIAL    = True

    m = ledmatrix.Matrix(sim=ENABLE_SIMULATOR,ser=ENABLE_SERIAL)
    f = form.Formatter(m.fdict)
    mpdi = mpdinfo.MpdInfo()


    if m.sim:
        ui = Interface()
        InputThread().start()

    iter = 0
    # main program loop
    while 1:
        iter += 1
        time.sleep(0.015)
        update_buffer(iter)
        m.refresh()


