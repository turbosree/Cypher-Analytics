# EXP[1] Danger with many time pad stream cipher: Problem with using the same stream cypher key multiple times. 
# -------------------------------------------------------------------------------------------------------------
# - Letter frequency analisys
# -- Eg: 'e' and 't' occurs frequenctly
# - Redundancies of languages
# -- 'a' XOR ' ' = 'A' etc.

import string
import sys
from operator import itemgetter, attrgetter

from CypherText import *

CHEXE=gen_cypher_text()[0]
TCHEXE=gen_cypher_text()[1]

C=[]
TC=[]

# Module init
def init():
    for i in range(0, len(CHEXE)):
        C.append(CHEXE[i].decode('hex'))
        print type(CHEXE[i]),len(CHEXE[i]),len(C[i])
    TC.append(TCHEXE.decode('hex'))
    print type(TCHEXE),len(TCHEXE),len(TC[0])

# Utilities
def toStr(s):
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def ctxor(c,l=10):
    r=c[0]
    for i in range(1,l):
        # print r
        # print "XOR"
        # print c[i]
        r=strxor(r,c[i])
    return r

def random(size=16):
    return open("/dev/urandom").read(size)

def encrypt(key, msg):
    c = strxor(key, msg)
    print
    print c.encode('hex')
    return c

def letterfreq(C,m1,m2):
    pc=string.ascii_letters
    lt=[]
    m=strxor(C[m1],C[m2])
    for i in range(0,len(pc)):
        n=m.count(pc[i])
        pos=[]
        if n > 0:
            q=0
            while True:
                p=m.find(pc[i],q,len(m))
                if p > -1:
                    pos.append(p)
                    q=p+1
                else:
                    break
            lt.append((pc[i],n,pos))
    return (sorted(lt, key=itemgetter(1), reverse=True),m)

def ctoa(C):
    init()

    lfa=[]
    k=[]
    sp=" "*1024
    print "sp: "+sp.encode('hex')+" sp len: "+str(len(sp))
    for p in range(0,1024):
        k.append(chr(0))
    for j in range(0,10):
        for i in range(j+1,10):
            lfa.append((letterfreq(C,j,i),i))
            print "Letter frequency analisys ("+"m"+str(j)+"XOR"+"m"+str(i)+"): "+" lfa len: "+str(len(lfa))+":"
            print lfa[len(lfa)-1]
    # For every profile (45), perform mXORmXORsp
    for h in range(0,len(lfa)):
        msg=strxor(lfa[h][0][1],sp)
        # print "MsgLen: "+str(len(msg))
        # print lfa[h]
        # For every highly frequent occuring letter in a profile
        # i - Highest frequently occuring letter
        # j - Position of occurence in mXm (XOR of both messages after removing k)
        for i in range(0, len(lfa[h][0][0])):
            # For every position of a particular highly frequent occuring letter in a profile
            for j in range(0, len(lfa[h][0][0][i][2])):
                ti=lfa[h][0][0][i][2][j]
                ci=lfa[h][1]
                # print "Len: "+str(ti)+" "+str(ci)+" "+str(len(lfa[h][0][0][i][2]))
                # print lfa[h]
                # print "StrLen: "+str(len(k))+" "+str(len(msg))+" "+str(len(C))+" "+str(len(C[ci]))
                # print ti,k[ti],msg[ti],C[ci][ti]
                k[ti]=strxor(msg[ti],C[ci][ti])
                print "Predicting k["+str(ti)+"]: "+hex(ord(k[ti]))
                # Check if our prediction is correct with all profiles of mhXORmx. m0XORm1,m0XORm2, etc.
                for x in range(h+1, 10):
                    msgx=strxor(lfa[x-1][0][1],sp)
                    # print "Len: "+str(ti)+" "+str(x)
                    # print lfa[h-1]
                    # print "StrLen: "+str(len(msgx))+" "+str(len(C))+" "+str(len(C[x]))
                    if ti<len(msgx) and ti<len(C[x]) and ti<len(k):
                        if strxor(msgx[ti],k[ti])==C[x][ti]:
                            # print strxor(msgx[ti],k[ti])==C[x][ti]
                            print "Prediction seems to be correct! Fix k["+str(ti)+"]: "+hex(ord(k[ti]))
                        else:
                            k[ti]=chr(0)
                            print "Prediction seems to be wrong! Ignore k["+str(ti)+"]!"
                            break
    key=""
    # print len(k)
    for y in range(0, len(k)):
        key=key+k[y]
    # print len(key)
    print "Target cipher: "+TC[0]
    tm=strxor(TC[0],key)
    print "Target cipher decryption: "+tm
    print "Len of decrypted msg: "+str(len(tm))
    return tm.encode('hex')
    # return key.encode('hex') # Return key

if __name__ == "__main__":
    main()
