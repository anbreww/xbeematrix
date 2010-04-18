#!/usr/bin/python
'''
convert a image made of hashes into an array for display on the matrix
'''

def lines_to_arr(lines):
    n_lines = len(lines) if len(lines) <= 8 else 8 # correct to parse 8 by 8
    max_len = max([len(l.rstrip('\n')) for l in lines]) # find longest line
    fmt = "{0:" + str(max_len) + "s}"
    new_arr = [fmt.format(l.rstrip('\n')) for l in lines]
    output_list = []
    for i in range(max_len):
        byte = "0b"
        for n in range(8):
            if n < n_lines: # zero-padding at the end
                byte = byte + new_arr[n][i].replace(' ','0').replace('#','1')
            else:
                byte = byte + '0'
        output_list.append(eval(byte))
    return output_list

def lines_to_buffers(lines):
    '''input lines of hashes, returns list of numbers

    lines are automatically broken into groups of 8 to fit in a standard led
    matrix "line".
    '''
    full_lines = (len(lines)-1)/8+1 # number of 8-bit lines

    output = []
    for i in range(full_lines):
        output.append(lines_to_arr(lines[i*8:(i+1)*8]))
    return output


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-f", "--file", dest="input_file", 
            help="create hash from FILE", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", default=False,
            help="verbose: print image to stdout", action="store_true" )
    parser.add_option("-a", "--array", dest="array", default=False,
            help="output as array. easier to copy-paste", action="store_true" )

    opts, args = parser.parse_args()

    #print opts.input_file

    if opts.verbose:
        for line in lines:
            print line.rstrip('\n')

    with open(opts.input_file) as input:
        lines = input.readlines()

    array = lines_to_buffers(lines)
    if opts.array:
        print array
    else:
        for group in array:
            print group

