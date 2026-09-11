import oqs

#ML-KEM configuration
ML_KEM_algorithm = "ML-KEM-768"

def generate_ml_kem_keypair():
    kem = oqs.KeyEncapsulation(ML_KEM_algorithm)

    public_key = kem.generate_keypair()

    return kem, public_key

def encapsulate_secret(public_key):

    with oqs.KeyEncapsulation(ML_KEM_algorithm) as client:

        ciphertext, shared_secret = client.encap_secret(public_key)

    return ciphertext, shared_secret

def decapsulate_secret(kem, ciphertext):

    shared_secret = kem.decap_secret(ciphertext)

    return shared_secret

def get_ml_kem_sizes(
        public_key,
        ciphertext,
        shared_secret,
        kem
):

    secret_key = kem.export_secret_key()

    return{
        "public_key_bytes": len(public_key),
        "secret_key_bytes": len(secret_key),
        "ciphertext_bytes": len(ciphertext),
        "shared_secret_bytes": len(shared_secret)
    }