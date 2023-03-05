# A dynamic URL and QR code that can be used as a method of attestation
# using X509 certificates. The URL and QR code is only valid for 
# 30 seconds in this example.
#
# Attestation is the process by which an entity produces evidence about itself 
# that another party can use to evaluate the trustworthiness of that entity.
#
# Author: Sreejith.Naarakathil@gmail.com

import jwt
import datetime
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import qrcode
import time
import pyotp

# set the private key and algorithm
with open('../test-ca/ecdsa/inter.key', 'rb') as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)
public_key = private_key.public_key()
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')
algorithm = 'ES256'

# set the payload for the JWT message
payload = {
    'user_id': '123',
    'username': 'johndoe',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
}

# generate the JWT message
jwt_message = jwt.encode(payload, private_key_pem, algorithm=algorithm)

# print the JWT message
print(jwt_message)

# URL domain name and query parameter
domain = "https://myservice.mydomain.com/verify?myid="

# Final URL
URL = domain + jwt_message
print('URL: ', URL)

# Generate a QR code with the TOTP value as the content
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(URL)
qr.make(fit=True)

# Save the QR code image as a file
filename = f"jwt_qr_{int(time.time())}.png"
img = qr.make_image(fill_color="black", back_color="white")
img.save(filename)

# Display the QR code image
img.show()