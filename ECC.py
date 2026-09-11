from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

#ECC configuration
ECC_curve = ec.SECP256R1()

def generate_ecc_keypair():

    private_key= ec.generate_private_key(
        ECC_curve
    )

    public_key = private_key.public_key()

    return private_key, public_key

def derive_shared_secret(private_key, peer_public_key):

    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)

    return shared_secret

def ecc_sign_message(private_key, message):
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def ecc_verify_signature(public_key, signature, message):
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))

    return True

def get_ecc_key_sizes(private_key, public_key):
    public_key_der = public_key.public_bytes(
        encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    private_key_der = private_key.private_bytes(encoding=serialization.Encoding.DER, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())

    public_key_raw = public_key.public_bytes(encoding=serialization.Encoding.X962, format=serialization.PublicFormat.UncompressedPoint)

    return {
        "ecc_curve_bits": public_key.curve.key_size,
        "public_key_der_bytes": len(public_key_der),
        "private_key_der_bytes": len(private_key_der),
        "public_key_raw_bytes": len(public_key_raw)
    }