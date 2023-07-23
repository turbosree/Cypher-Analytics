# // Signature test vectors generated with ECDSA/ECC NIST P-256 with pkcs#12 key store
# // NIST P-256 ECDSA as specified in FIPS 186-4: Digital Signature Standard
# // Author: sreejith.naarakathil@gmail.com

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates
import os
import datetime

# Create an ECDSA key pair
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key = private_key.public_key()

# Create a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Example Inc."),
    x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
])
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    public_key
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).sign(private_key, hashes.SHA256(), default_backend())

# Serialize the key pair and certificate into a PKCS#12 file
password = b"your-password"
filename = "ecdsa_key_pair.pfx"

with open(filename, "wb") as f:
    pfx_data = serialize_key_and_certificates(
        name=filename.encode(),  # Encode the filename as bytes
        key=private_key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )
    f.write(pfx_data)


def load_pkcs12_file(filename, password):
    with open(filename, "rb") as f:
        pfx_data = f.read()

    private_key, cert, _ = serialization.load_key_and_certificates(pfx_data, password, default_backend())  # Original function name
    return private_key, cert


def sign_message(private_key, message):
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    return signature


# Load the PKCS#12 file
loaded_private_key, loaded_cert = load_pkcs12_file(filename, password)

# Sign a message using the loaded private key
message = b"Hello, this is a message to be signed."
signature = sign_message(loaded_private_key, message)

print("Message:", message)
print("Signature:", signature)
