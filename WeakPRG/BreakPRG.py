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
# EXP[2] Brute-force attack or exhaustive key search: Analyze a weak PRG whose output can be predicted in roughly 2^28 time.
# --------------------------------------------------------------------------------------------------------------------------
# WeakPRG.py implements a weak PRG algorithm whose output can be predicted in 2^28 time.
# With random seeds, each 28 bits, the algorithm will output 9 psuedo-random numbers.
# The below experiment (brute-force attack or exhaustive key search) will predict the 
# 10th psuedo-random number in roughly 2^28 time.

import cProfile
import sys

P = 0   # Give a prime about 2^28

# 9 test outputs of WeakPRG.py with unknown secret seed
PRG = []

class WeakPRG(object):
    def __init__(self, p, x, y):   
        self.p = p
        self.x = x
        self.y = y
        # print "__init__  %d %d" % (x,y)
        
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

def run_main():
    prng = WeakPRG(P,0,0)
    x = 0
    while x < 2**28:
        y_ = ((2*x + 5) % P)^PRG[0]
        # print x_,PRG[0],y_,P
        while (y_-7) > 0 and (y_-7)%3 != 0:
                y_=y_+P
                # print y_
        y = (y_-7)/3
        # print P,x,y
        prng.x = x
        prng.y = y
        i = 0
        while i < 9:
            if PRG[i] != prng.next():
                # print "PRNs at %d dont match!" % i
                break
            # else:
            #     print "PRNs at %d match!" % i
            i = i + 1
        if i == 9:
            print "Seed for WeakPRG found! Predicted (x, y, r) = (%d, %d, %d)" % (x, y, prng.next())
            break
        x = x + 1

def main():
    if P==0 or len(PRG)==0:
        print "Give a prime about 2^28 and 9 test outputs of WeakPRG.py with unknown secret seed!"
        sys.exit()
    cProfile.run('run_main()')
    # run_main()

if __name__ == "__main__":
    main()
