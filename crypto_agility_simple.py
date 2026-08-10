"""
Crypto Agility Demonstration
----------------------------

Purpose:
    Demonstrates how an application can support multiple digital signature
    algorithms while keeping the application logic independent of the
    underlying cryptographic implementation.

Example algorithms:
    - RSA-PSS
    - ECDSA

Crypto agility concept:
    The signing algorithm is selected through configuration rather than being
    hard-coded into the application workflow. This makes it easier to migrate
    to a different algorithm when security requirements, standards, or threat
    capabilities change.

Example migration:
    RSA-PSS  ->  ECDSA  ->  Future/PQC algorithm

This is a simplified educational example and is NOT intended for production
cryptographic use. Production systems should use established cryptographic
libraries, key-management practices, algorithm policies, and secure storage.

Dependency:
    pip install cryptography
"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding


# ---------------------------------------------------------
# Crypto-agile signer
# ---------------------------------------------------------

class Signer:
    def __init__(self, algorithm="RSA"):
        self.algorithm = algorithm.upper()

        if self.algorithm == "RSA":
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )

        elif self.algorithm == "ECDSA":
            self.private_key = ec.generate_private_key(
                ec.SECP256R1()
            )

        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def sign(self, message: bytes) -> bytes:

        if self.algorithm == "RSA":
            return self.private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

        elif self.algorithm == "ECDSA":
            return self.private_key.sign(
                message,
                ec.ECDSA(hashes.SHA256())
            )

    def verify(self, message: bytes, signature: bytes) -> bool:

        public_key = self.private_key.public_key()

        try:
            if self.algorithm == "RSA":
                public_key.verify(
                    signature,
                    message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

            elif self.algorithm == "ECDSA":
                public_key.verify(
                    signature,
                    message,
                    ec.ECDSA(hashes.SHA256())
                )

            return True

        except Exception:
            return False


# ---------------------------------------------------------
# Application logic
# ---------------------------------------------------------

message = b"Vehicle software update v1.2.3"

# Change the algorithm without changing application logic
algorithm = "RSA"
# algorithm = "ECDSA"

signer = Signer(algorithm)

signature = signer.sign(message)

print(f"Algorithm : {algorithm}")
print(f"Signature : {signature.hex()[:40]}...")
print(f"Valid     : {signer.verify(message, signature)}")

