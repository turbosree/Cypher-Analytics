# Sometimes obfuscating some secret is enough to protect it from
# visible exposure. This can be achieved by encoding the secret. 
# This script encodes a secret using base64 encoding. And uses 
# HMAC and SHA256 to generate a hash of the secret. 
# Input is a combination of one or more of the below values:
# - Vendor ID
# - Product ID
# - Setup PIN Code
# - and some custum data
# Output: Encoded data with the setup PIN code
# TODO: Relate pin code and the manual pairing code cryptographically
# Author: sreejith.naarakathil@gmail.com

import hashlib
import hmac
import base64

# Encode the commissioning information as bytes
vendor_id = 1
product_id = 2
commissioning_flow = 3
rendezvous_information = 4
discriminator = 701
setup_pin_code = 12332

# Base64 encode the setup_pin_code
setup_pin_code_bytes = base64.b64encode(setup_pin_code.to_bytes(4, byteorder='big'))

commissioning_info_bytes = vendor_id.to_bytes(2, byteorder='big') + product_id.to_bytes(2, byteorder='big') \
                            + commissioning_flow.to_bytes(1, byteorder='big') + rendezvous_information.to_bytes(1, byteorder='big') \
                            + discriminator.to_bytes(2, byteorder='big') + setup_pin_code_bytes

# Generate the onboarding subkey
onboarding_subkey = hashlib.sha256(b'MatterOnboardingSubkey').digest()

# Generate the shared secret from the onboarding subkey
shared_secret = hmac.new(onboarding_subkey, commissioning_info_bytes, hashlib.sha256).digest()

# Generate the onboarding code
onboarding_code = hmac.new(b'OnboardingSubkey', shared_secret, hashlib.sha256).digest()
print("onboarding_code:", onboarding_code)

# Convert the onboarding code to a base 16 encoded string
onboarding_code_string = base64.b16encode(onboarding_code).decode()

# Generate the manual pairing code from the onboarding code
manual_pairing_code = "{:011d}".format(int(onboarding_code_string, 16))

print("Manual pairing code:", manual_pairing_code)

# Ensure that the input string has an even length
if len(manual_pairing_code) % 2 == 1:
    manual_pairing_code = '0' + manual_pairing_code

# Decode the manual pairing code to extract the commissioning information
manual_pairing_code_bytes = base64.b16decode(manual_pairing_code.encode('utf-8'))

vendor_id = int.from_bytes(manual_pairing_code_bytes[0:2], byteorder='big')
product_id = int.from_bytes(manual_pairing_code_bytes[2:4], byteorder='big')
commissioning_flow = int.from_bytes(manual_pairing_code_bytes[4:5], byteorder='big')
rendezvous_information = int.from_bytes(manual_pairing_code_bytes[5:6], byteorder='big')
discriminator = int.from_bytes(manual_pairing_code_bytes[6:8], byteorder='big')

# Base64 decode the setup_pin_code
setup_pin_code = int.from_bytes(base64.b64decode(manual_pairing_code_bytes[8:]), byteorder='big')

# Print the extracted commissioning information
print(f"Vendor ID: {vendor_id}")
print(f"Product ID: {product_id}")
print(f"Commissioning Flow: {commissioning_flow}")
print(f"Rendezvous Information: {rendezvous_information}")
print(f"Discriminator: {discriminator}")
print(f"Set Up PIN Code: {setup_pin_code}")

