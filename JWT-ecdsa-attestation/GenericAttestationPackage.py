# // Attestation test vectors generated with JWT ECDSA/ECC NIST P-256 key 
# // Attestation is the process by which an entity produces evidence about itself 
# // that another party can use to evaluate the trustworthiness of that entity.
# // NIST P-256 ECDSA as specified in FIPS 186-4: Digital Signature Standard
# // Author: sreejith.naarakathil@gmail.com

import jwt
import datetime
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption

# Generate ECC key pair
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Serialize public key
public_pem = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

# Serialize private key
private_pem = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())

# JWT payload
payload = {
    "iss": "Issuer Name",
    "sub": "Subject ID",
    "aud": "Audience",
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
    "deviceInfo": {
        "serialNumber": "1234567890",
        "manufacturer": "Device Manufacturer",
        "model": "Device Model",
        "hardwareVersion": "1.0",
        "softwareVersion": "1.0"
    },
    "cccSpecification": "R3.0"
}

# JWT headers
headers = {
    "alg": "ES256",
    "typ": "JWT",
    "kid": "Key Identifier"
}

# Sign the JWT with the private key
attestation_jwt = jwt.encode(payload, private_pem, algorithm="ES256", headers=headers)

# Print the attestation JWT
print("Attestation JWT:")
print(attestation_jwt)
