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
        if not m.sim:
            self.show_help()
        while 1:
            if m.sim:
                c = ui.stdscr.getch()
                if c == ord('q'):
                    break
            else:
                print "\n >",
                i = raw_input()
                if i == 'q':
                    break
                elif i == 'h':
                    self.show_help()
                else:
                    print("Command not recognized")
        m.finished = True
        m.running = False
        #ui.terminate()

    def show_help(self):
        print("Available commands:")
        print("q - quit")
        print("h - help")


class Interface():
    '''Contains all UI-related tasks'''

    statusstring = "LED Matrix Controller | Andrew Watson | Robopoly - 2010"
    display_fps = False
    simfps = ''
    matrixfps = ''

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

    def statusline(self, statusmsg, color=None, offset=0):
        '''print a status message at the bottom of main window'''
        win = self.stdscr
        if not color:
            color = curses.color_pair(0)
        (winy, winx) = win.getmaxyx()
        xbegin = winx - len(statusmsg) - 1
        win.addstr(winy-2-offset,xbegin,statusmsg, color | curses.A_BOLD)


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
        if self.display_fps:
            self.statusline(self.simfps)
            self.statusline(self.matrixfps, offset=1)
        self.centered_status(self.statusstring , self.stdscr)

        #mpdclient.connect('localhost',6600)
        self.stdscr.refresh()
        self.mpad.refresh( 0,0, pady0, padx0, pady0+pady, padx0+padx)



class MatrixUpdater(threading.Thread):
    '''Thread to update matrix at a given rate'''
    def run(self, framerate=40.1):
        timer = Timer()
        timer.start()
        interval = 1./framerate
        #time.sleep(2)
        while 1 and m.running:
            timer.wait_until_reaches(interval)
            if m.sim:
                ui.matrixfps = "Matrix FPS : {0:<5.1f}".format(
                        1/(timer.get_elapsed()))
            timer.start()
            buffer_lock.acquire()
            m.copybuffer()
            buffer_lock.release()
            m.refresh()


class Timer():
    '''Basic timer operations'''
    id = 0

    def __init__(self):
        Timer.id += 1
        self.begin_time = None
        self.stop_time = None

    def start(self):
        self.begin_time = time.time()

    def get_elapsed(self):
        #return self.stop_time - self.begin_time
        return time.time() - self.begin_time

    def stop(self):
        self.stop_time = time.time()

    def wait_until_reaches(self, interval):
        while time.time() < self.begin_time + interval:
            time.sleep(0.0001)
        self.stop()

    def wait(self, interval):
        self.start()
        self.wait_until_reaches(interval)





def update_buffer(iteration):

    if(iteration < 2):
        m.set_buffer_size(int(m.panel_size*3))

    nowplaying = mpdi.get_nowplaying()

    buffer_lock.acquire()
    if(iteration % 1 == 0):
        m.scroll_buffer('left')
        m.scroll_buffer('left')

    
    if mpdi.haschanged:
        m.set_buffer_size(len(nowplaying)*14+30)
        m.text_to_buffer(nowplaying, linebreak=False)

    m.text_to_buffer(mpdi.get_timestring(), startrow='bottom')
    buffer_lock.release()

    #os.system("clear")
    if m.sim:
        ui.update()

buffer_lock = threading.Lock()

if __name__ == '__main__':
    ENABLE_SIMULATOR = True
    ENABLE_SERIAL    = True

    m = ledmatrix.Matrix(sim=ENABLE_SIMULATOR,ser=ENABLE_SERIAL)
    f = form.Formatter(m.fdict)
    mpdi = mpdinfo.MpdInfo()

    lasttime = time.time()


    if m.sim:
        ui = Interface()
        ui.display_fps = True
    InputThread().start()

    iter = 0
    updater = MatrixUpdater().start()

    # in fps
    buffer_scroll_rate = 30
    buffer_timer = Timer()
    buffer_timer.start()

    # main program loop
    while 1 and m.running:
        buffer_timer.wait_until_reaches(1./buffer_scroll_rate)
        buffer_timer.start()
        if iter % 10 == 0 and m.sim == True:
            newtime = time.time()
            frame_time = newtime - lasttime
            lasttime = newtime
            if iter > 0:
                ui.simfps = "Buffer FPS : {0:<5.1f}".format(10/frame_time)
        iter += 1
        #time.sleep(1./buffer_scroll_rate)
        update_buffer(iter)
        #m.copybuffer()
        #m.refresh()

    if m.sim:
        ui.terminate()


