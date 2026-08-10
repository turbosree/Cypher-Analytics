"""
Crypto Agility Demonstration
----------------------------

Purpose:
    Demonstrates crypto agility by separating the application's cryptographic
    requirements from the underlying digital signature algorithm.

Architecture:

    Application
         |
         v
    Crypto Policy
         |
         v
    Crypto Provider
      /       \
 RSA-PSS     ECDSA

The application does not select RSA or ECDSA directly. Instead, it requests
a signature according to a cryptographic policy. The policy determines which
algorithm is currently approved.

This allows the cryptographic algorithm to be changed through configuration
without modifying the application logic.

Example migration:

    Policy v1: RSA-PSS
        |
        v
    Policy v2: ECDSA
        |
        v
    Future policy: PQC algorithm

This is a simplified educational example and is NOT intended for production
cryptographic use.

Dependency:
    pip install cryptography
"""

from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding


# =========================================================
# Cryptographic Policy
# =========================================================

@dataclass
class CryptoPolicy:
    signature_algorithm: str
    hash_algorithm: str = "SHA256"


# ---------------------------------------------------------
# Example cryptographic policies
# ---------------------------------------------------------

POLICIES = {
    "POLICY_V1": CryptoPolicy(
        signature_algorithm="RSA-PSS",
        hash_algorithm="SHA256"
    ),

    "POLICY_V2": CryptoPolicy(
        signature_algorithm="ECDSA",
        hash_algorithm="SHA256"
    ),
}


# =========================================================
# Crypto Provider
# =========================================================

class CryptoProvider:

    def __init__(self, policy: CryptoPolicy):
        self.policy = policy
        self.private_key = self._generate_key()

    def _generate_key(self):

        if self.policy.signature_algorithm == "RSA-PSS":
            return rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )

        elif self.policy.signature_algorithm == "ECDSA":
            return ec.generate_private_key(
                ec.SECP256R1()
            )

        else:
            raise ValueError(
                f"Unsupported algorithm: "
                f"{self.policy.signature_algorithm}"
            )

    def sign(self, message: bytes) -> bytes:

        if self.policy.signature_algorithm == "RSA-PSS":

            return self.private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

        elif self.policy.signature_algorithm == "ECDSA":

            return self.private_key.sign(
                message,
                ec.ECDSA(hashes.SHA256())
            )

    def verify(self, message: bytes, signature: bytes) -> bool:

        public_key = self.private_key.public_key()

        try:

            if self.policy.signature_algorithm == "RSA-PSS":

                public_key.verify(
                    signature,
                    message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

            elif self.policy.signature_algorithm == "ECDSA":

                public_key.verify(
                    signature,
                    message,
                    ec.ECDSA(hashes.SHA256())
                )

            return True

        except Exception:
            return False


# =========================================================
# Application
# =========================================================

def process_software_update():

    # Application selects a POLICY, not an algorithm.
    policy_name = "POLICY_V1"

    policy = POLICIES[policy_name]

    crypto = CryptoProvider(policy)

    message = b"Vehicle software update v1.2.3"

    signature = crypto.sign(message)

    valid = crypto.verify(message, signature)

    print(f"Policy    : {policy_name}")
    print(f"Algorithm : {policy.signature_algorithm}")
    print(f"Signature : {signature.hex()[:40]}...")
    print(f"Valid     : {valid}")


if __name__ == "__main__":
    process_software_update()
