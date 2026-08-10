"""
Crypto Agility Demonstration: Classical -> PQC
-----------------------------------------------

Purpose:
    Demonstrates how an application can evolve from a classical digital
    signature algorithm to a post-quantum cryptographic (PQC) algorithm
    without redesigning the application.

The application interacts only with a generic CryptoProvider interface.
The cryptographic policy determines which algorithm is used.

Architecture:

    Application
         |
         v
    Crypto Policy
         |
         v
    Crypto Provider
       /       \
   ECDSA      ML-DSA
  classical    PQC

This example uses a simulated ML-DSA provider so that it can run without
requiring a PQC library. The ML-DSA implementation is NOT cryptographically
real and must not be used for security.

For a production implementation, replace MockMLDSAProvider with a real
PQC implementation.

Dependency:
    pip install cryptography
"""

from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


# =========================================================
# Cryptographic Policy
# =========================================================

@dataclass
class CryptoPolicy:
    name: str
    signature_algorithm: str


CLASSICAL_POLICY = CryptoPolicy(
    name="CLASSICAL",
    signature_algorithm="ECDSA"
)

PQC_POLICY = CryptoPolicy(
    name="PQC",
    signature_algorithm="ML-DSA-65"
)


# =========================================================
# ECDSA Provider
# =========================================================

class ECDSAProvider:

    def __init__(self):
        self.private_key = ec.generate_private_key(
            ec.SECP256R1()
        )

    def sign(self, message: bytes) -> bytes:
        return self.private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )

    def verify(self, message: bytes, signature: bytes) -> bool:

        try:
            self.private_key.public_key().verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True

        except Exception:
            return False


# =========================================================
# Mock ML-DSA Provider
# =========================================================

class MockMLDSAProvider:

    def sign(self, message: bytes) -> bytes:
        """
        Simulated ML-DSA signature.

        This is ONLY for demonstrating crypto agility.
        It is NOT a cryptographic implementation.
        """

        return b"MOCK-ML-DSA-SIGNATURE"


    def verify(
        self,
        message: bytes,
        signature: bytes
    ) -> bool:

        return signature == b"MOCK-ML-DSA-SIGNATURE"


# =========================================================
# Crypto Provider Factory
# =========================================================

def create_crypto_provider(policy):

    if policy.signature_algorithm == "ECDSA":

        return ECDSAProvider()

    elif policy.signature_algorithm == "ML-DSA-65":

        return MockMLDSAProvider()

    else:

        raise ValueError(
            f"Unsupported algorithm: "
            f"{policy.signature_algorithm}"
        )


# =========================================================
# Application
# =========================================================

def process_software_update(crypto):

    """
    Application logic.

    The application does not know whether the underlying
    cryptography is ECDSA or ML-DSA.
    """

    software_update = b"Vehicle software update v2.0"

    signature = crypto.sign(software_update)

    if crypto.verify(
        software_update,
        signature
    ):
        print("Signature VALID")
    else:
        print("Signature INVALID")


# =========================================================
# Deployment Configuration
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # Current deployment: classical cryptography
    # -----------------------------------------------------

    policy = CLASSICAL_POLICY

    crypto = create_crypto_provider(policy)

    print("Policy    :", policy.name)
    print("Algorithm :", policy.signature_algorithm)

    process_software_update(crypto)


    # -----------------------------------------------------
    # Future deployment: PQC
    # -----------------------------------------------------

    print()

    policy = PQC_POLICY

    crypto = create_crypto_provider(policy)

    print("Policy    :", policy.name)
    print("Algorithm :", policy.signature_algorithm)

    process_software_update(crypto)
