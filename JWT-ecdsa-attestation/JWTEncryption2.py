from jose import jwe
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import sys
import binascii

message = 'test'
method = 'A128GCM'
password = 'pass'
management = 'dir'

if len(sys.argv) > 1:
    message = str(sys.argv[1])
if len(sys.argv) > 2:
    password = str(sys.argv[2])
if len(sys.argv) > 3:
    method = str(sys.argv[3])
if len(sys.argv) > 4:
    management = str(sys.argv[4])

print(f"Message: {message}")
print(f"Password: {password}")
print(f"Method: {method}\n")

# Deriving key using HKDF
salt = b'you should have a secure salt here'  # Should be a secure random value
info = b'optional context and application specific information'
backend = default_backend()
hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,  # Maximum length for AES key (256 bits)
    salt=salt,
    info=info,
    backend=backend
)
key = hkdf.derive(password.encode())

if "128" in method: key = key[:16]
if "192" in method: key = key[:24]
if "256" in method: key = key[:32]

print(f"Key used: {binascii.hexlify(key)}\n")

try:
    token = jwe.encrypt('Hello, World!', key, algorithm=management, encryption=method)
    print(f"Token: {token}")
    rtn = jwe.decrypt(token, key)
    print(f"Decrypted: {rtn}")

except Exception as error:
    print(error)
