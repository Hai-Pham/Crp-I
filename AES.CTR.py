__author__ = 'Gorilla'

from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto.Util import Counter


def decrypt_CTR(ct, key):

    BLOCK_SIZE = 32 #32 bytes of hexa string

    #extract iv, ct and pad from ciphertext (input: hex)
    i = ct[0:BLOCK_SIZE]
    ct = ct[BLOCK_SIZE:]

    ## conver to bytes and initialize AES decryption
    ciphertext = unhexlify(ct)
    iv = unhexlify(i) # from hexa to bytes: 16 bytes now
    k = unhexlify(key)
    ctr = Counter.new(128, initial_value=int(hexlify(iv), 16))

    print("i is: ", i)
    print("iv is: ", iv)

    cipher = AES.new(k, AES.MODE_CTR, counter=ctr)

    d = cipher.decrypt(ciphertext) #bytes: b'xxxxx'
    print(d)

    return d.decode()


def main():

    CTR_key = '36f18357be4dbd77f050515c73fcf9f2'

    c1 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
    c2 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'
    d1 = decrypt_CTR(c1, CTR_key)
    d2 = decrypt_CTR(c2, CTR_key)

    print('message 1 is:', d1)
    print('message 2 is:', d2)


main()