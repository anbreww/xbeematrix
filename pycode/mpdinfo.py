import mpd
import formatting as form

class MpdInfo():
    '''Get formatted info from mpd

    MpdInfo is a wrapper around the MPDClient() class to return formatted
    strings with information from an mpd server
    '''

    def __init__(self):
        self.mpdclient = mpd.MPDClient()
        self.mpdclient.connect('localhost',6600)
        self.f = form.Formatter()
        self.nowplaying = ''
        self.haschanged = False

    
    def get_nowplaying(self, formatstr=''):
        '''Now playing string "artist - title"
        '''
        song = self.mpdclient.currentsong()
        t = song['title']
        a = song['artist']
        b = song['album']
        #d = song['date']

        if formatstr == '':
            formatstr = '{a:} - {t:}'

        new = formatstr.format(a=a, t=t, b=b)
        if new != self.nowplaying:
            self.haschanged = True
            self.nowplaying = new
        else:
            self.haschanged = False

        return self.nowplaying

    def get_timestring(self, formatstr='', center=True, width=96):
        '''Elapsed/Total time of current track

        Optional arguments : format string (use {elapsed},{total})
        if center==True, string will be centered in a [width] long string
        padded with spaces. This should really be in a seperate method...
        '''
        t = self.mpdclient.status()['time'].split(':')
        timestat = "{0} / {1}".format(self.f.sec_to_hms(t[0]), self.f.sec_to_hms(t[1]))
        if not center:
            return timestat
        else:
            return self.f.center_text(timestat, width)



