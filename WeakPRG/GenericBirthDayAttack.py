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
# EXP[3] Generic birthday attack - SHA-256 case study: Collision resistence is necesary for security (Message Integrity)
# ----------------------------------------------------------------------------------------------------------------------
# Birthday attack: http://en.wikipedia.org/wiki/Birthday_attack
# Let H:M→{0,1}^n be a hash function (|M| >> 2^n). The below algorithm will find a collision of H in time O(2^(n/2)) hashes.
# Consider the hash function obtained by truncating the output of SHA-256 to 50 bits, say H(x)=LSB50(SHA256(x)), 
# that is we drop all but the right most 50 bits of the output. Our goal is to implement a generic birthday attack to 
# find a collision on this hash function. ie find two strings x≠y such that LSB50(SHA256(x))=LSB50(SHA256(y)). Note the 
# memory utilization when running the script using 'pmap <pid> | grep total'.

from Crypto.Hash import SHA256

f = open("/dev/urandom")
tSet = set()
mSet = set()
tDict= dict()

def random(size=4):
    return f.read(size)

def tag(msg):
  h = SHA256.new()
  h.update(msg)
  s = bin(int(h.hexdigest(),16))
  # print s[-50:],int(s[-50:],2)
  return int(s[-50:],2)

# Using Dictionary
def main():
    i = 0
    while i < 2**25:
        mi = random(4)
        imi = int(mi.encode('hex'),16)
        t = tag(mi)
        if t not in tDict:
            tDict[t] = imi
        elif tDict[t] != imi:
            print "Collision detected!"
            mj = hex(tDict[t])[2:].rstrip('L')
            if len(mj) % 2:
                mj = '0' + mj
            print mi.encode('hex'),mj,t,tag(mj.decode('hex')),len(bin(t))-2
            break
        i = i + 1
    print "Exiting..."

# Using sets
# def main():
#     i = 0
#     while i < 2**25:
#         mi = random(4)
#         if int(mi.encode('hex'),16) not in mSet:
#             t = tag(mi)
#             if t not in tSet:
#                 tSet.add(t)
#                 mSet.add(int(mi.encode('hex'),16))
#             else:
#                 print "Collision detected!"
#                 for mj in mSet:
#                     mk = hex(mj)[2:].rstrip('L')
#                     if len(mk) % 2:
#                         mk = '0' + mk
#                     if tag(mk.decode('hex')) == t:
#                         print mi.encode('hex'),mk,t,tag(mk.decode('hex')),len(bin(t))-2
# 			break
#                 break
#         i = i + 1
#     print "Exiting..."

if __name__ == "__main__":
    main()

