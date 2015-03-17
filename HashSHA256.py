__author__ = 'Gorilla'

import math
from binascii import hexlify
from Crypto.Hash import SHA256

def readfile(fileobject, blocksize = 1024):
    f = open(fileobject, "rb")
    file = f.read()
    num_block = math.floor(len(file) / blocksize)
    print(num_block)

    #extract the very last block
    #hash it to append to the 2nd last one
    last_block = file[num_block*blocksize:]
    h = SHA256.new(last_block)

    #deal with each block
    for i in range(num_block, 0, -1):
         block = file[(i-1)*blocksize: i*blocksize]
         block += h.digest() #append hash
         #init and hash again
         h = SHA256.new(block)

    return hexlify(h.digest()).decode()


def main():
    file = "C:\DATA\Intro.mp4"
    print(readfile(file))

main()
