# Dynamic URL/QR code generation test application. 
# Input is a combination of one or more of the below values:
# - A domain name for URL
# - SHA256 Hash of custom data of any length
# - A ECDSA/ECC NIST P-256 Signature to verify authenticity
# - SHA256 of current timestamp to verify freshness of URL/QR code
# Output: Dynamic URL and its QR code
# Author: sreejith.naarakathil@gmail.com

import qrcode
import time
from datetime import datetime
import imageio.v2 as imageio
import hashlib
from ecdsa import SigningKey, NIST256p
import struct
import webbrowser

QRCodes = []
domain = "https://gnusfaas.com/?token="
fragment = "#summary"
hash = hashlib.sha256()
hash.update(b'{"name": "name", "email": "name@email.com"}')
# print('digest:', hash.hexdigest())
sha256_digest = str(hash.hexdigest())

# Sample ecdsa signature (concatinated r and s components)
sk = SigningKey.generate(curve=NIST256p)
vk = sk.verifying_key

# Run QR code generation for 10 secs
for i in range(0, 10):
    # Current timestamp with millisecond accuracy
    ts = time.time()

    # Unique timestamp (without milliesecond part) is used to verify the freshness of the QR code.
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    # print('timestamp:', str(timestamp))

    # Non-deterministic ecdsa signature. 
    # A unique signature is generated each time to make the QR code non-deterministic. 
    signature = sk.sign(b'{"domain": "myservice.mydomain.com", "email": "myservice@mydomain.com"}')
    assert vk.verify(signature, b'{"domain": "myservice.mydomain.com", "email": "myservice@mydomain.com"}')

    # Non-deterministic ecdsa signature as a message digest
    ecdsa_digest = sk.sign(b'{"name": "name", "email": "name@email.com"}')
    assert vk.verify(ecdsa_digest, b'{"name": "name", "email": "name@email.com"}')

    # SHA256 hash of timestamp as a freshness token
    hash = hashlib.sha256()
    hash.update(str(timestamp).encode('utf-8'))
    freshness = str(hash.hexdigest())

    # Format the URL in a suitable format for the application
    #URL = domain + sha256_digest + "." + signature.hex() + "#ts=" + str(ts)
    #URL = domain + ecdsa_digest.hex() + "." + signature.hex() + "#ts=" + str(ts)
    URL = domain + ecdsa_digest.hex() + "&ts=" + freshness[0:16] + fragment
    print('URL: ', URL)

    # Create QR code
    img = qrcode.make(URL)
    type(img)  # qrcode.image.pil.PilImage
    filename = "images/" + str(ts) + "-" + str(freshness) + ".png"
    QRCodes.append(filename)
    img.save(filename)
    time.sleep(2)

images = []
for QRCode in QRCodes:
    images.append(imageio.imread(QRCode))
imageio.mimsave('Dynamic-QRCode.gif', images)

# open default web browser and display the QR code image
webbrowser.open("Dynamic-QRCode.gif")