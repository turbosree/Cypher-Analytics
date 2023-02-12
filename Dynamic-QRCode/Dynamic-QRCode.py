# Dynamic QR code generation test application. 
# Input:
# - A domain name for URL
# - SHA256 Hash of custom data of any length
# - A ECDSA/ECC NIST P-256 Signature to verify authenticity
# - Current timestamp to verify freshness of QR code
# Output: Dynamic URL and its QR code
# Author: sreejith.naarakathil@gmail.com

import qrcode
import time
import imageio.v2 as imageio
import hashlib
from ecdsa import SigningKey, NIST256p
import sys

QRCodes = []
domain = "https://myservice.mydomain.com/verify?myid="
hash = hashlib.sha256()
hash.update(b'{"name": "name", "email": "name@email.com"}')
# print('digest:', hash.hexdigest())
digest = str(hash.hexdigest())

# Sample ecdsa signature (concatinated r and s components)
sk = SigningKey.generate(curve=NIST256p)
vk = sk.verifying_key

# Run QR code generation for 10 secs
for i in range(0, 10):
    # Unique timestamp is used to verify the freshness of the QR code.
    ts = time.time()
    # print('Time:', ts)

    # Non-deterministic ecdsa signature. 
    # A unique signature is generated each time to make the QR code non-deterministic. 
    signature = sk.sign(b'{"domain": "myservice.mydomain.com", "email": "myservice@mydomain.com"}')
    assert vk.verify(signature, b'{"domain": "myservice.mydomain.com", "email": "myservice@mydomain.com"}')

    # Format the URL
    URL = domain + digest + "." + signature.hex() + "#ts=" + str(ts)
    print('URL: ', URL)

    # Create QR code
    img = qrcode.make(URL)
    type(img)  # qrcode.image.pil.PilImage
    filename = "images/" + str(ts) + ".png"
    QRCodes.append(filename)
    img.save(filename)
    time.sleep(1)

images = []
for QRCode in QRCodes:
    images.append(imageio.imread(QRCode))
imageio.mimsave('Dynamic-QRCode.gif', images)