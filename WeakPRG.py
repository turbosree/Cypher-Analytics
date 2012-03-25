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
# A weak PRG whose output can be predicted in 2^28 time.
# With random seeds, each 28 bits, the below algorithm will output 9 psuedo-random numbers.
# The script BreakPRG.py will predict it's 10th output in roughly 2^28 time.

# import random
import sys

P = 0   # Give a prime about 2^28

class WeakPRG(object):
    # Generate seed with 56 bits of entropy. Here initial value of x and y togather contribute 56 bits.
    def __init__(self, p):   
        self.p = p
        self.x = 0 # random.randint(0, p); Give your secret seed#1 here
        self.y = 0 # random.randint(0, p); Give your secret seed#2 here
   
    def next(self):
        # x_{i+1} = 2*x_{i}+5  (mod p)
        self.x = (2*self.x + 5) % self.p
        # print len(bin(self.x))-2

        # y_{i+1} = 3*y_{i}+7 (mod p)
        self.y = (3*self.y + 7) % self.p
        # print len(bin(self.y))-2

        # z_{i+1} = x_{i+1} xor y_{i+1}
        # print len(bin(self.x ^ self.y))-2
        return (self.x ^ self.y) 

def main():
    if P == 0:
        print "Give a prime about 2^28!"
        sys.exit()
    prng = WeakPRG(P)
    for i in range(1, 10):
        print "Output #%d: %d" % (i, prng.next())

if __name__ == "__main__":
    main()

