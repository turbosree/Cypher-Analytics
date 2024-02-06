# With JWTs (JSON Web Tokens), we can create a claim and then sign it with 
# public key encryption or HMAC. Below script is to encrypt data with a JWT 

from jose import jwe
import hashlib
import sys
import binascii

message='test'
method='A128GCM'
password='pass'
management='dir'


if (len(sys.argv)>1):
  message=str(sys.argv[1])
if (len(sys.argv)>2):
  password=str(sys.argv[2])
if (len(sys.argv)>3):
  method=str(sys.argv[3])
if (len(sys.argv)>4):
  management=str(sys.argv[4])

print(f"Message: {message}")
print(f"Password: {password}")
print(f"Method: {method}\n")
pwd = hashlib.sha256(password.encode())
key=pwd.digest()


if ("128" in method): key=key[:16]
if ("192" in method): key=key[:24]
if ("256" in method): key=key[:32]

print(f"Key used: {binascii.hexlify(key)}\n")

try: 
 token=jwe.encrypt('Hello, World!',key, algorithm=management, encryption=method)
 print(f"Token: {token}")
 rtn=jwe.decrypt(token,key)
 print(f"Decrypted: {rtn}")

except Exception as error:

 print(error)