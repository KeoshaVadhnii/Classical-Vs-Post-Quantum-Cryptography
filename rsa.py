from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

#RSA configuration
RSA_key_size = 2048
Public_EXP = 65537

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=Public_EXP,
        key_size=RSA_key_size,
    )

    public_key = private_key.public_key()

    return private_key, public_key

def encrypt_message(public_key, message):
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext

def decrypt_message(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext

def sign_message(private_key, message):
    signature = private_key.sign(message, padding.PSS(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return signature

def verify_signature(public_key, signature, message):

    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return True

def get_rsa_key_sizes(private_key, public_key):
    public_key_der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_key_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return{
        "rsa_modulus_bits": public_key.key_size,
        "rsa_modulus_bytes": public_key.key_size // 8,
        "public_key_der_bytes": len(public_key_der),
        "private_key_der_bytes": len(private_key_der)
    }