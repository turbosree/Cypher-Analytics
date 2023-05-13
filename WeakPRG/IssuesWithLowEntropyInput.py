"""
Title: AES-ECB with Low Entropy Input
Author: sreejith.naarakathil@gmail.com

Description: This script demonstrates the weakness of the AES-ECB encryption mode when used with low entropy input.
It creates a repeating plaintext block and encrypts it with a fixed key, resulting in repeating "magic numbers"
in the output ciphertext. This exemplifies the unsuitability of AES-ECB for many cryptographic applications due to
its lack of input data diffusion.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import binascii

def aes_ecb_encrypt(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    return encryptor.update(padded_data) + encryptor.finalize()

def main():
    # 128-bit key
    key = b'\x00' * 16

    # Low entropy input: 16 bytes, repeated 8 times
    plaintext = b'\x01' * 16 * 8

    ciphertext = aes_ecb_encrypt(key, plaintext)

    # print ciphertext in hex
    print(binascii.hexlify(ciphertext).decode())

if __name__ == '__main__':
    main()
