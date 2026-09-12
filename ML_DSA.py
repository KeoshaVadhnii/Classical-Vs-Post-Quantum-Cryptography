import oqs

# ML-DSA configurations
ML_DSA_algorithms = ["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"]

def generate_ml_dsa_keypair(algorithm):
    signer = oqs.Signature(algorithm)

    public_key = signer.generate_keypair()

    return signer, public_key

def sign_ml_dsa_message(signer, message):

    signature = signer.sign(message)

    return signature

def verify_ml_dsa_signature(public_key, signature, message, algorithm):

    with oqs.Signature(algorithm) as verifier:

        valid = verifier.verify(message, signature, public_key)

    return valid

def get_ml_dsa_sizes(public_key, signature, signer):

    secret_key = signer.export_secret_key()

    return {
        "public_key_bytes": len(public_key),
        "secret_key_bytes": len(secret_key),
        "signature_bytes": len(signature)
    }