# Description: Distributed Key Management System.
# Author: Sreejith Naarakathil

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom
from cryptography.hazmat.primitives import padding as sym_padding

# Crypto Module that can be initiated on participant nodes/clients/servers/devices.
# Provides a secure method to exchange symmetric keys between nodes using exported public keys.
# Provides a method to map symmetric keys to a key_id and serial number. 
# Later, the key_id and serial number can be used to use the symmetric key for encryption/decryption.
# Provides a method to test the symmetric key using the key_id.
class CryptoModule:
    def __init__(self):
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self._symmetric_keys = {}

    def export_public_key(self):
        public_key = self._private_key.public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        public_key_hash.update(pem)
        serial_number = public_key_hash.finalize()[:12]
        return pem, serial_number

    def provision_symmetric_key(self, encrypted_symmetric_key, key_id):
        decrypted_key = self._private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self._symmetric_keys[key_id] = decrypted_key

        # Pad the key_id to match AES block size
        padder = sym_padding.PKCS7(128).padder()
        padded_key_id = padder.update(key_id.encode()) + padder.finalize()

        # Generate key checksum
        cipher = Cipher(algorithms.AES(decrypted_key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        key_checksum = encryptor.update(padded_key_id) + encryptor.finalize()
        return key_checksum

    def test_symmetric_key(self, key_id, provided_checksum):
        if key_id not in self._symmetric_keys:
            return False

        key = self._symmetric_keys[key_id]
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_checksum = decryptor.update(provided_checksum) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = sym_padding.PKCS7(128).unpadder()
        unpadded_key_id = unpadder.update(decrypted_checksum) + unpadder.finalize()

        return unpadded_key_id.decode() == key_id

# Encrypting the symmetric key with the public key
def encrypt_symmetric_key_with_public_key(symmetric_key, public_key_pem):
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )
    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

# Example Usage
crypto_module = CryptoModule()

# Export Public Key and Serial Number
public_key_pem, serial_number = crypto_module.export_public_key()
print("Public Key:", public_key_pem)
print("Serial Number:", serial_number.hex())

# Encrypt and Provision a Symmetric Key
symmetric_key = urandom(32)  # Generate a 256-bit symmetric key
encrypted_symmetric_key = encrypt_symmetric_key_with_public_key(symmetric_key, public_key_pem)
key_id = "key1"
key_checksum = crypto_module.provision_symmetric_key(encrypted_symmetric_key, key_id)

# Test Symmetric Key
test_result = crypto_module.test_symmetric_key(key_id, key_checksum)
print("Test Result:", "Success" if test_result else "Failure")
