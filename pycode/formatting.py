from lcdfont import font as xfont


def char_to_hashes(char):
    return [disp_bin(c) for c in char]
def disp_bin(n):
    '''display binary as # and ' ' '''
    binstr = "{0:07b}".format(n)
    return binstr.replace('0b','').replace('1','#').replace('0',' ')

def rotate_list(hash):
    output = []
    for i in range(len(hash[0])):
        output.append(''.join(w[i] for w in hash))
    return output

def print_list(list):
    hashes = char_to_hashes(list)
    output = rotate_list(hashes)
    for line in output:
        print(line)

def return_list(list):
    '''same as print_list but return a list of lines instead of printing'''
    hashes = char_to_hashes(list)
    output = rotate_list(hashes)
    return output

def print_dict():
    for (key, char) in fdict.items():

        hashes = char_to_hashes(char)
        output = rotate_list(hashes)

        for line in output:
            print(line)

def print_alpha():
    for letter in "abcdefghijklmnopqrstuvwxyz":
        print_list(fdict[letter])

def make_word(string):
    word = []
    for c in string:
        word.extend(fdict[c])
        word.extend([0])
    return word

def print_text(string, maxlen=0):
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
        word = make_word(line)
        print
        print_list(word)

if __name__ == '__main__':
    fdict = dict()
    for i in range(len(xfont)):
        fdict[chr(ord(' ')+i)] = xfont[i]

    print_text("hello world 1234567890 &%#", 6)
