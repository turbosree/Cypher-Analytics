
# A simple key store that securely stores cryptographic keys.
# NOTE: Do not use it in production environments
# Usage: python .\SimpleKeyStore.py af787sas7dfa78s6a7sd7asfa my_api_key_1
# Usage: python .\SimpleKeyStore.py "This is the data to be encrypted and decrypted." my_secret_slot_1
# IMPORTANT: Make sure to clear the command line history after running this script. 
# Otherwise, the secret data will be stored in the command line history.
# author: sreejith.naarakathil@gmail.com 

import os
import subprocess
import base64
import hashlib
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import sys

def get_cmd_output(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    output_lines = result.stdout.strip().splitlines()
    return output_lines[-1] if len(output_lines) > 1 else None

def get_unique_identifiers():
    windows_product_key_cmd = 'wmic path SoftwareLicensingService get OA3xOriginalProductKey'
    windows_product_key = get_cmd_output(windows_product_key_cmd)
    return windows_product_key

def get_aes_key(secret_key, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(secret_key.encode())
    return key

def encrypt_data(data, secret_key):
    user_secret = getpass.getpass("Enter a secret password: ")
    secret_key = secret_key + user_secret
    salt = os.urandom(16)
    aes_key = get_aes_key(secret_key, salt)
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return salt + nonce + encrypted_data + encryptor.tag

def decrypt_data(encrypted_data, secret_key):
    user_secret = getpass.getpass("Enter a secret password: ")
    secret_key = secret_key + user_secret    
    salt, nonce, encrypted_data, tag = encrypted_data[:16], encrypted_data[16:28], encrypted_data[28:-16], encrypted_data[-16:]
    aes_key = get_aes_key(secret_key, salt)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

def save_encrypted_data(key_slot_id, encrypted_data):
    key_store = {}

    # Load existing key store if the file exists
    if os.path.exists("key_store.json"):
        with open("key_store.json", "r") as infile:
            key_store = json.load(infile)

    # Update the key store with the new key-value pair
    key_store[key_slot_id] = base64.b64encode(encrypted_data).decode()

    # Save the updated key store to the file
    with open("C:\home\MyGITHUBRepo\Cypher-Analytics\SimpleKeyStore\key_store.json", "w") as outfile:
        json.dump(key_store, outfile)

def load_encrypted_data(key_slot_id):
    with open("C:\home\MyGITHUBRepo\Cypher-Analytics\SimpleKeyStore\key_store.json", "r") as infile:
        loaded_key_store = json.load(infile)
        encrypted_data = base64.b64decode(loaded_key_store[key_slot_id])
    return encrypted_data

def main():
    windows_product_key = get_unique_identifiers()
    print("Windows Product Key:", windows_product_key)

    # Read data from command line
    if len(sys.argv) > 1:
        data = sys.argv[1]
        key_slot_id = sys.argv[2]
    else:
        data = "This is the data to be encrypted and decrypted."
        key_slot_id = "key_slot_1"
    print("Data:", data)
    print("Key slot id:", key_slot_id)

    encrypted_data = encrypt_data(data, windows_product_key)

    # Save encrypted data to the file
    save_encrypted_data(key_slot_id, encrypted_data)
    print("Encrypted Data stored in key store file.")

    # Load the encrypted data from the file
    encrypted_data_from_key_store = load_encrypted_data(key_slot_id)

    decrypted_data = decrypt_data(encrypted_data_from_key_store, windows_product_key)
    print("Decrypted Data:", decrypted_data)

if __name__ == "__main__":
    main()

