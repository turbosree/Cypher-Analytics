import sys

MSGS = ()                       # The (list of)secret message/s to challenge you!

TMSG = ""                       # The secret message!

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def random(size):
    return open("/dev/urandom").read(size)

def encrypt(key, msg):
    c = strxor(key, msg)
    # print c.encode('hex')
    return c.encode('hex')

def gen_cypher_text():
    key = random(1024)
    Ctxt = [encrypt(key, msg) for msg in MSGS]
    TCtxt = encrypt(key, TMSG)
    return (Ctxt,TCtxt)
