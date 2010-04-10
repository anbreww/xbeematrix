from lcdfont import font as xfont

class Formatter():
    '''Provides various buffer and string manipulation methods'''
    def __init__(self, font_dictionary):
        self.fdict = font_dictionary

    def char_to_hashes(self,char):
        return [self.disp_bin(c) for c in char]
    def disp_bin(self,n):
        '''display binary as # and ' ' '''
        binstr = "{0:07b}".format(n)
        return binstr.replace('0b','').replace('1','#').replace('0',' ')

    def rotate_list(self,hash):
        output = []
        for i in range(len(hash[0])):
            output.append(''.join(w[i] for w in hash))
        return output

    def print_list(self,list):
        hashes = self.char_to_hashes(list)
        output = self.rotate_list(hashes)
        for line in output:
            print(line)

    def return_list(self,list):
        '''same as print_list but return a list of lines instead of printing'''
        hashes = self.char_to_hashes(list)
        output = self.rotate_list(hashes)
        return output

    def print_dict(self):
        for (key, char) in self.fdict.items():

            hashes = self.char_to_hashes(char)
            output = self.rotate_list(hashes)

            for line in output:
                print(line)

    def print_alpha(self):
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.print_list(self.fdict[letter])

    def make_word(self,string, fdict):
        '''Return a list of bytes from a string of chars and spaces, using
        font lookup table (fdict is a dictionary)
        '''
        word = []
        for c in string:
            word.extend(self.fdict[c])
            word.extend([0])
        return word

    def print_text(self, string, maxlen=0):
        if maxlen > 0:
            n_lines = len(string)/maxlen
            lines=[]
            for i in range(n_lines):
                lines.append(string[i*maxlen:i*maxlen+maxlen])
            if len(string)%maxlen != 0:
                lines.append(string[n_lines*maxlen:])
        else:
            lines=[string]
        for line in lines:
            word = self.make_word(line, self.fdict)
            print
            self.print_list(word)

if __name__ == '__main__':
    fontdict = dict()
    for i in range(len(xfont)):
        fontdict[chr(ord(' ')+i)] = xfont[i]

    f = Formatter(fontdict)
    f.print_text("hello world 1234567890 &%#", 6)
