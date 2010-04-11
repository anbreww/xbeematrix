#!/bin/python

import signal
import time

import formatting as form
import ledmatrix
from lcdfont import font

import mpd

import os
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
                m.close()
                ui.terminate()


class Interface():
    '''Contains all UI-related tasks'''
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0) # hide cursor
        self.mpad = curses.newpad(17,98)

    def terminate(self):
        '''kill graphical interface and exit program'''
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()
        os.sys.exit()

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

    def sec_to_hms(self, s):
        # TODO : this belongs in the mpd (or formatter) module!!
        '''convert seconds to h:mm:ss format. accepts str and number types'''
        s = int(s)
        h = s/3600
        s -= 3600*h
        m = s/60
        s -= 60*m
        if h > 0:
            return "%d:%02d:%02d" % (h, m, s)
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
    timestat = "{0} / {1}".format(ui.sec_to_hms(t[0]), ui.sec_to_hms(t[1]))
    n = len(timestat)
    n = str((96-n*6)/10+n+1)
    timestat = ''.join(["{0:>",n,"}"]).format(timestat)
    m.text_to_buffer(timestat , startrow='bottom')

    #os.system("clear")
    if m.sim:
        ui.stdscr.erase()
        ui.stdscr.border()
        (winy, winx) = ui.stdscr.getmaxyx()
        (pady, padx) = ui.mpad.getmaxyx()
        if pady >= winy :
            pady = winy-1
        if padx >= winx :
            padx = winx-1
        pady0 = (winy-pady)/2
        padx0 = (winx-padx)/2



        #if (winy < 18 or winx < 98):
        #    ui.stdscr.addstr(1,1,"Terminal too small!")
        #else:
        lines = []
        lines= f.return_list(m.get_buffer()[:192:2])
        lines.append("")
        lines.extend(f.return_list(m.get_buffer()[1:192:2]))
        ypos = 1
        for line in lines:
            #ui.stdscr.addstr(ypos,1,line,  curses.color_pair(1) | curses.A_BOLD)
            ui.mpad.addstr(ypos,1,line,  curses.color_pair(1) | curses.A_BOLD)
            ypos += 1
        ui.mpad.border()
        #ui.centered_status("LED Matrix Controller - Andrew Watson - 2010")
        #ui.centered_status("Robopoly", ui.stdscr, curses.color_pair(1))
        ui.centered_status(
            "LED Matrix Controller | Andrew Watson | Robopoly - 2010",
            ui.stdscr)

        #mpdclient.connect('localhost',6600)
        ui.stdscr.refresh()
        ui.mpad.refresh( 0,0, pady0, padx0, pady0+pady, padx0+padx)



def sigwinch_handler(n, frame):
    curses.endwin()
    ui.stdscr = curses.initscr()



if __name__ == '__main__':
    ui = Interface()
    m = ledmatrix.Matrix(sim=True,ser=True)
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



#curses.nocbreak(); ui.stdscr.keypad(0); curses.echo()
#curses.endwin()
