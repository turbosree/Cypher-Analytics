# A dynamic URL and QR code that is only valid for next 30 seconds
#
# Author: Sreejith.Naarakathil@gmail.com

import qrcode
import time
import pyotp

# Generate a time-based one-time password (TOTP)
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)

# Get the current TOTP value
current_totp = totp.now()

# URL domain name and query parameter
domain = "https://myservice.mydomain.com/verify?myid="

# Final URL
URL = domain + current_totp
print('URL: ', URL)

# Generate a QR code with the TOTP value as the content
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(URL)
qr.make(fit=True)

# Save the QR code image as a file
filename = f"totp_qr_{int(time.time())}.png"
img = qr.make_image(fill_color="black", back_color="white")
img.save(filename)

# Display the QR code image
img.show()
