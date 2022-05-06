# Sample application to generate Key diversification 
# test vectors conforming to NXP application note AN10922
# 
# Refer section: 2.2.1 AES-128 key diversification example
# 
# Author: sreejith.naarakathil@gmail.com

from Crypto.Cipher import AES
from Crypto.Hash import CMAC

# Test Master key (K) = 00112233445566778899AABBCCDDEEFF, which will be diversified.
MasterKey_K = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
# The initialization vector to use for encryption or decryption.
IV = bytes.fromhex("00000000000000000000000000000000")

# Test Inputs used for the Diversification of 128-bit AES key
CustumData1 = "0011223344556677"
CustumData2 = "001122334455667788990A0B0C0D0E0F1A1B"
# Diversification constant is '01'
DiversificationInput_M = bytes.fromhex("01" + CustumData1 + CustumData2)

# Refer section: 2.2.1 AES-128 key diversification example
#  Test vectors at step 9 and step 13
DiversificationInput_M_Step9 = bytes.fromhex("0104782E21801D803042F54E585020416275")
DiversificationInput_M_Step13 = bytes.fromhex("0104782E21801D803042F54E5850204195E66EB928278083BFDC8A5A7E0E0D25")

# Calculate diversified key correcponding to test vector at step 15 
Cipher = AES.new(MasterKey_K, AES.MODE_CBC, IV)
DiversifiedKey_Step14 = Cipher.encrypt(DiversificationInput_M_Step13)
DiversifiedKey_Step15 = DiversifiedKey_Step14[-16:].hex()
print("DiversifiedKey_Step15: {}\n".format(DiversifiedKey_Step15))

# Calculate diversified key using standard CMAC
# NOTE: If the length of M is more than 15 bytes, standard CMAC algorithm can be used, without
#       taking care of padding, XOR and encryption. The message for standard CMAC is then
#       the data of step 9.
Cmac = CMAC.new(MasterKey_K, ciphermod=AES)
Cmac.update(DiversificationInput_M_Step9)
DiversifiedKey_UsingDataOfStep9 = Cmac.hexdigest()
print("DiversifiedKey_UsingDataOfStep9: {}\n".format(DiversifiedKey_UsingDataOfStep9))

# Test that the algorithms used from pycryptodome conform to algorithms used in NXP application note AN10922 
assert DiversifiedKey_UsingDataOfStep9 == DiversifiedKey_Step15, f"Test failed, CMAC algorithm implementation do not conform to 2.2.1 AES-128 key diversification example in AN10922"

# If the test passes, go ahead and calculate diversified key using your custom input parameters for Key diversification
#  Parameters: 8-byte Custum data 1, 18-byte Custum data 2 
Cmac = CMAC.new(MasterKey_K, ciphermod=AES)
Cmac.update(DiversificationInput_M)
DiversifiedKey = Cmac.hexdigest()
print("DiversifiedKey: {}\n".format(DiversifiedKey))

# Write Key diversification test vectors to a file
with open('SymmetricKeyDiversificationTestVectors.txt', 'w') as f:
    line =  "Master key [K] : {}\n".format(MasterKey_K.hex()) + \
            "Custum data 1 [CustumData1] : {}\n".format(CustumData1) + \
            "Custum data 2 [CustumData2] : {}\n".format(CustumData2) + \
            "Diversified Key [CMAC] : {}\n".format(DiversifiedKey)
    f.write(line)
