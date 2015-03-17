__author__ = 'Gorilla'

from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto import Random

# AES block is 16B (in hexa it is 32B)
BLOCK_SIZE = 16

#insert dummy block of padding '}'
def pad(s):
    return s + (16 - len(s)%16)*'}'


# input: pt and key both are text
# output: plaintext
def encrypt(pt,key):
    iv = Random.new().read(BLOCK_SIZE)
    k = unhexlify(key)
    cipher = AES.new(k, AES.MODE_CBC, iv)

    toHex = "".join([hex(ord(c))[2:].zfill(2) for c in pad(pt)]) # pad and convert plain to hexa
    plaintext = unhexlify(toHex) #hexa to bytes
    result = iv + cipher.encrypt(plaintext)

    return hexlify(result).decode()  #return hexa then decode to plain


def decrypt_CBC(ct, key):

    BLOCK_SIZE = 32 #32 bytes of hexa string

    #extract iv, ct and pad from ciphertext
    i = ct[0:BLOCK_SIZE]
    pad_len = len(ct) % BLOCK_SIZE
    ct = ct[BLOCK_SIZE:]

    ## conver to bytes and initialize AES decryption
    ciphertext = unhexlify(ct)
    iv = unhexlify(i) # from hexa to bytes
    k = unhexlify(key)
    cipher = AES.new(k, AES.MODE_CBC, iv)

    d = cipher.decrypt(ciphertext) #bytes: b'xxxxx'
    print(d)

    text = d.decode() #to plain text

    if (pad_len == 0):
        return text[:len(d)-1]
    else:
        return text[:(len(d)-pad_len)]



def main():
    msg = 'this is a test for AES encryption method using CBC encryption a'
    CBC_key = '140b41b22a29beb4061bda66b6747e14'

    ciphertext = encrypt(msg,CBC_key)
    print("cipher text is: ", ciphertext)

    c1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
    c2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'
    d1 = decrypt_CBC(c1, CBC_key)
    d2 = decrypt_CBC(c2, CBC_key)

    print('message is:', d1)
    print('message is:', d2)


main()