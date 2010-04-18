# Array manipulation utilities

These scripts provide functionality to convert standard image
formats as well as "hash-images" to a python array of bytes, ready
to be written directly to an LED matrix.

In the resulting array, the first byte contains the left-most
vertical byte (MSb at top-left of display). The second byte is the
one directly to its right, etc.

If an image takes up more than 8 pixels vertically, the next 8
pixels are stored in a second array, and so on. The structure is
something like this:

    [ 
        [ First 8-bit line - first byte, second byte ],
        [ Second 8-bit line, second byte of second line ],
    ]

The `hashtoarray` utility will produce this output if used with
the -a switch. Otherwise it will simply output one array per line,
for better readability.

## hashtoarray

This utility takes a text file of hashes and blanks and converts
it to a python array.

Example input:

      #     #  
    #  #   #  #
    # ####### #
    ### ### ###
    ###########
     ######### 
      #     #  
     #       #

if this is stored in the file `critter`, then we can use the
following command :

    ./hashtoarray.py -f critter

which will produce the following output:

    [120, 29, 190, 108, 60, 60, 60, 108, 190, 29, 120]

Where 120 corresponds to `' ####   '` placed vertically.

`./hashtoarray.py -f critter -a` produces the same output, with an
extra set of braces. use this for images that are larger than 8
pixels tall.

## imgtohashes

This utility takes a picture file as input and outputs a series of
hashes and blanks, which can be processed by the `hashtoarray`
utility.

The picture file can be any format supported by the Python Imaging
Library (PIL), but must be 1-bit depth. Use the included png file
as an example.

to convert picture.png to hashes, use the following command:

    ./imgtohashes.py picture.png 

this will print the result of the conversion to standard output.

## putting it all together

Although they don't accept input from stdio, these two utilities
can be used together quite easily to produce an array from a
picture. To do so, simply:

    ./imgtohashes.py picture.png > picture
    cat picture # check that you get what you expected!
    ./hashestoarray.py -f picture -a > picture.py

Note that hashestoarray.py does not yet prefix the array with a
variable assignment, so you'll have to edit the file yourself to
add this.
