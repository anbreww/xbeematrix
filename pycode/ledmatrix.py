import serial
import formatting as form
import time
from lcdfont import font

class Matrix():
    '''Wrapper for Quad matrix.

    set sim=False to disable terminal output
    set ser=False to disable output to matrix (simulation mode)
    '''
    num_panels = 4
    lines_per_panel = 2
    panel_size = 24*num_panels*lines_per_panel
    buffer_size = panel_size*3
    panel_columns = num_panels*24
    total_columns = buffer_size/2

    buffer_limit = panel_size # limit serial transmission to n bytes

    s_title = ""
    s_artist = ""

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
        self.formatter = form.Formatter(self.fdict)
        
        if self.ser:
            self.s = serial.Serial('/dev/ttyUSB0', 38400, timeout=0,
                                    parity=serial.PARITY_NONE)
        if self.sim:
            #interface = Interface()
            pass
        else:
            print("Disabled simulator output")

    def set_buffer_size(self,new_size):
        '''Change pixelbuffer size. This currently resets the buffer. Might add
        code later to keep current contents and clip/zeropad while resizing
        '''
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
            buf.extend(self.formatter.make_word(string[i], self.fdict))
            if len(buf) > length:
                return i
        return None

    def roll(self, string, direction='left', padding=0, padchar=' '):
        '''Simple marquee method for a string'''
        s = string
        if direction == 'left':
            i = 1
        else:
            i = -1
        return ''.join( [ s[i:],s[:i] ] )


    def text_to_buffer(self, string, startcol=0, startrow='top', linebreak=True):
        '''Write a string to the pixel buffer.

        Lines break at the end of buffer, not end of physical display.
        If startrow is 'bottom', line break will not occur.
        '''
        index = None
        if linebreak:
            index = self.compute_breakpos(string,self.total_columns-startcol)
        word = self.formatter.make_word(string[:index], self.fdict)
        self.list_to_buffer(word, startcol, startrow)
        if linebreak and startrow=='top':
            word = self.formatter.make_word(string[index:], self.fdict)
            self.list_to_buffer(word, startcol, row='bottom')

    def scroll_buffer(self, direction='left'):
        '''Move entire buffer one pixel sideways (pixels wrap around)'''
        if direction == 'left':
            self.buffer.append(self.buffer.pop(0))
            self.buffer.append(self.buffer.pop(0))
        else:
            self.buffer.insert(0, self.buffer.pop())
            self.buffer.insert(0, self.buffer.pop())

    def get_buffer(self):
        '''Simple getter and setter methods for now, plan to add some different
        format options for abstraction from the buffer format (i.e. load buffer
        from a bitmap-like array
        '''
        return self.buffer

    def set_buffer(self, newbuffer):
        self.buffer = newbuffer



    def refresh(self):
        '''Refresh: write buffer to the display. If serial communication is
        disabled, a delay simulates the data transfer time
        '''
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
            self.s.write(chr(self.buffer_limit))
        else:
            print("ERROR: " + nextchar)

        #time.sleep(0.001)

        #size = s.readline()

        #print("size confirmed : %d (sent %d)" % (int(size), buffer_size))


        buffer_str = ''.join([chr(c) for c in self.buffer[0:self.buffer_limit]])
        self.s.write(buffer_str)
