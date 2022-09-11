# An implementation of Shamir's Secret Sharing scheme for distributed embedded systems.
# The test application generates fragements of a secret (Eg: AES128 Key)
# for the purpose of distributing it in a distributed embedded control 
# system.
#
# TODO: Secure storage and trasport of secret cryptographic materials
#
# Author: sreejith.naarakathil@gmail.com
# 
# Reference:
# https://github.com/twhiteman/pyDes
# https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
# https://en.wikipedia.org/wiki/Key_checksum_value

import binascii
from pyDes import *

def XOR_Bytes(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

# A sample secret; an AES128 key that needs to be securely distributed
secret = '00112233445566778899AABBCCDDEEFF'
secret = binascii.unhexlify(secret)

# Generate 2 random numbers. Chosen below values for demonstration purpose only
random1 = 'FFEEDDCCBBAA99887766554433221100'
random2 = 'FF00EE11DD22CC33BB44AA5599668877'
random1 = binascii.unhexlify(random1)
random2 = binascii.unhexlify(random2)

# A sample message to generate a Key checksum value
msg = '00000000000000000000000000000000'
msg = binascii.unhexlify(msg)

tdes = triple_des(secret, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
kcv = tdes.encrypt(msg)

# Generate fragments to share with the nodes in the distributed system
frag1 = XOR_Bytes(secret, random1)
frag2 = XOR_Bytes(random1, random2)

print('Secret: ' + str(secret.hex()))
print('Key checksum value: ' + str(kcv.hex()))
# print(str(kcv.hex()[0:16]))
print('random1: ' + str(random1.hex()))
print('random2: ' + str(random2.hex()))
print('frag1: ' + str(frag1.hex()))
print('frag2: ' + str(frag2.hex()))
print('frag3: ' + str(random2.hex()))

assert kcv.hex()[0:16] == "fb09759972301af4"

# Output:
# $ python3 SymmetricKeyExchange.py 
# Secret: 00112233445566778899aabbccddeeff
# Key checksum value: fb09759972301af4fb09759972301af4de5167551d7ba60f
# random1: ffeeddccbbaa99887766554433221100
# random2: ff00ee11dd22cc33bb44aa5599668877
# frag1: ffffffffffffffffffffffffffffffff
# frag2: 00ee33dd668855bbcc22ff11aa449977
# frag3: ff00ee11dd22cc33bb44aa5599668877
