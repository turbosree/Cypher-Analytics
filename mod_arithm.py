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
# EXP[4] Meet in the middle attack: Compute discrete log modulo a prime p.
# ---------------------------------------------------------------------------------------------------
# Meet-in-the-middle attack: http://en.wikipedia.org/wiki/Meet-in-the-middle_attack
# Let g be some element in Zp* (Set of invertible evlements in Zp = {0,1,2...,p-1}) and suppose we are given h in Zp∗ 
# such that h=g^x where 1≤x≤2^40. Our goal is to find x! We will use meet in the middle attack to find x.
# Let B=2^20. Since x is less than B2 we can write the unknown x base B as x=x0*B+x1 where x0,x1 are in the range [0,B−1]. 
# Then,
#    h=g^x=g^(x0*B+x1)=(g^B)^x0 * g^x1 in Zp.
# By moving the term g^x1 to the other side we obtain,
#    h/g^x1=(g^B)^x0 in Zp. From this equality, we can find (x0,x1) such that there is a collision between LHS and RHS.
# Steps:
#  -  First build a hash table of all possible values of the left hand side h/g^x1 for x1=0,1,…,2^20.
#  -  Then for each value x0=0,1,2,…,2^20 check if the right hand side (g^B)^x0 is in this hash table.
#  -  If a collision is found, then x = x0*B+x1
# To do modular arithmatic with large numbers, we will use gmpy.

import gmpy
from gmpy import mpz

# Inputs to the algorithm
p=mpz(13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171)
g=mpz(11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568)
h=mpz(3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333)

hTable = {}

def main():
    i = mpz(0)
    j = mpz(0)
    gI = gmpy.invert(g,p)
    B = pow(2,20)
    gC = pow(g,B,p)
    while i <= B:
        hTable[(h * pow(gI, i, p)) % p]=i
        i = i + 1
    print "Hash table created!"
    while j <= B:
        rhs = pow(gC, j, p)
        if rhs in hTable:
            i=hTable[rhs]
            break
        j = j + 1
    print "Result: ",i,j,j*B+i
    
if __name__ == "__main__":
    main()

