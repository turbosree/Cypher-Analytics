# Description: This file contains the code for selective disclosure JWT attestation
# Author: Sreejith Naarakathil

import jwt
import datetime

# Sample payload with more detailed claims
payload = {
    "sub": "1234567890",
    "name": "Bjorn Larsson",
    "admin": True,
    "iat": datetime.datetime.utcnow(),
    # Selective disclosure claim
    "disclosure": {
        "age": 30,
        "email": "bjorn.larsson@example.com",
        "address": "Johanneberg, Gothenburg, Sweden",
    }
}

# Secret key for JWT encoding
secret = 'your-256-bit-secret'

# Create a JWT token just for the disclosure claim
disclosure_token = jwt.encode(payload["disclosure"], secret, algorithm="HS256")

# Verify that user provided claim matches the decoded token
user_provided_claim =    {"disclosure": {
        "age": 31,
        "email": "bjorn.larsson@example.com",
        "address": "Johanneberg, Gothenburg, Sweden",
    }}
try:
    # Decode the token
    decoded = jwt.decode(disclosure_token, secret, algorithms="HS256")
    # Verify that the user provided claim matches the decoded token
    if decoded == user_provided_claim["disclosure"]:
        print("Claim verified")
    else:
        print("Claim not verified")
except jwt.ExpiredSignatureError:
    print("Token expired")
except jwt.InvalidTokenError:
    print("Invalid token")

# Verify if the claimed age > 18 is true using a zero knowledge proof
# TODO

