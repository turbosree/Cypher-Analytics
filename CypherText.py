#   Copyright (c) 2011 Sreejith Naarakathil
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see <http://www.gnu.org/licenses/>.
#
# Description of module:
# ----------------------

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

def main():
    if len(MSGS) == 0 or len(TMSG) == 0:
        print "No test messages given!"
        sys.exit()
    gen_cypher_text()

if __name__ == "__main__":
    main()
