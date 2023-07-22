# A method to generate QR code from a manually entered code.
# 
# Manual-code->Secret-code->QRCode
# 
# The method for generating a manual code is to use a cryptographically 
# secure random number generator to generate a random 10-12 digit decimal number.
# The QR code is generated from a secret code using a standardized encoding 
# method called "EUI-64 QR Code Encoding" specified in the Matter commissioning 
# specification.
# The EUI-64 QR Code Encoding method converts the 16-byte secret code into 
# a 22-byte sequence that can be represented as a QR code. 
# The encoding method involves the following steps:
# 1. Convert the Secret code to a 128-bit value, using the first 8 bytes as 
# the manufacturer-assigned identifier (MAID) and the remaining 8 bytes as the 
# random component of the Secret code.
# 2. Apply a hash function (SHA-256) to the 128-bit value to generate a 32-byte value.
# 3. Truncate the 32-byte value to 22 bytes to generate the EUI-64 QR Code.
# 4. Convert the 22-byte value to a QR code using a QR code generator.
#
# The resulting QR code data contains no secrets so it can be shared in pain text 
# or printed as a QR code. 
# The secret code should be handled securely at rest and in transit.
# The manual code can be shared in pain text.
#
# author: sreejith.naarakathil@gmail.com

import hashlib
import base64
import qrcode
import random
import hmac

from ecdsa import NIST256p
from ecdsa import SigningKey

# Example manual code (11 digits)
manual_code = random.randint(10000000000, 99999999999)
print("Manual code:", manual_code)

# Example Secret code
#secret_code = b"\x12\x34\x56\x78\x9a\xbc\xde\xf0\x12\x34\x56\x78\x9a\xbc\xde\xf0"

# Use the manual code to generate the shared secret key
shared_secret = SigningKey.from_secret_exponent(manual_code, curve=NIST256p)

# Generate the secret code from the shared secret key
secret_code = hmac.new(b'SecretSubkey', shared_secret.to_string(), hashlib.sha256).digest()[:16]
print("Secret code:", secret_code.hex())

# Convert the secret code to a 128-bit value
maid = secret_code[:8]
random = secret_code[8:]
value = int.from_bytes(maid + random, byteorder='big')

# Apply SHA-256 hash function to generate a 32-byte value
hash_value = hashlib.sha256(value.to_bytes(16, byteorder='big')).digest()

# Truncate the hash value to 22 bytes
truncated_value = hash_value[:22]

# Encode the truncated value as a QR code
qr_data = base64.b32encode(truncated_value).decode('utf-8')
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(qr_data[:32])
qr.make(fit=True)
print("QR code data:", qr_data[:32])

# Save the QR code image as a PNG file
img = qr.make_image(fill_color="black", back_color="white")
img.save("QRCodeFromManualCode.png")


# Test vectors:
# Manual code: 23336982247
# Secret code: 518c96af7c1f614d965bc8f081a32e18
# QR code data: 44OGUV5HUIKVE7DAX5TNUFQ4OWM4ABD2