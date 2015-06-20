__author__ = 'Gorilla'

import urllib.request, urllib.error, urllib.parse
import math
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
CIPHER = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4' #64B
c =      'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c3bdf302936266926ff37dbf7035d5eeb4'

BLOCK_SIZE = 16
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib.parse.quote(q)    # Create query URL
        req = urllib.request.Request(target)         # Send HTTP request to server
        try:
            f = urllib.request.urlopen(req)          # Wait for response
        except urllib.error.HTTPError as e:
            print("We got: %d" % e.code)       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding


def strxor(a, b):     # xor two strings of different lengths made by Dan Boneh
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def extract(cipher, block_size):
    num_blocks = math.floor(len(cipher) / block_size)
    iv = cipher[0:block_size*2]
    xx = cipher[block_size*2:]
    print(iv)
    print(xx)
    return iv, xx

if __name__ == "__main__":
    po = PaddingOracle()
    #po.query(sys.argv[1])       # Issue HTTP query with the given argument
    po.query(c)
    extract(c,BLOCK_SIZE)