from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_der_public_key
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.asymmetric import ec

import base64
import binascii

# Load the X509 certificate file
with open('../test-ca/ecdsa/inter.cert', 'rb') as cert_file:
    cert_data = cert_file.read()

# Load the X509 certificate object from the PEM-encoded data
cert = load_pem_x509_certificate(cert_data)

# Load the private key file
with open('../test-ca/ecdsa/inter.key', 'rb') as key_file:
    key_data = key_file.read()

# Load the private key object from the PEM-encoded data
private_key = load_pem_private_key(key_data, None)

# Extract the public key from the X509 certificate object
public_key = cert.public_key().public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo
)

# Extract the ECDSA private key from the private key object
ecdsa_private_key = private_key.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.PKCS8,
    encryption_algorithm = serialization.NoEncryption()
)

# Print the public and private keys
print("Public key:")
print(public_key.decode('utf-8'))
print("ECDSA private key:")
print(ecdsa_private_key.decode('utf-8'))

# Remove the PEM header and footer
pem_lines = public_key.decode().split('\n')
der_data = ''.join(pem_lines[1:-1]).encode()

# Decode the base64-encoded DER data
der_bytes = base64.b64decode(der_data)

# Load the public key from the DER data
public_key = load_der_public_key(der_bytes)

# Extract the ECDSA public key
ecdsa_public_key = public_key.public_bytes(
    encoding = serialization.Encoding.DER,
    format = serialization.PublicFormat.SubjectPublicKeyInfo
)

# Extract the 64-byte ECDSA public key from the DER-encoded SubjectPublicKeyInfo structure
ecdsa_public_key = ecdsa_public_key[28:92]

# Do something with the public key
print("ECDSA public key:", ecdsa_public_key.hex())


# TODO: output does not match the attestation example. So this code is buggy!!!