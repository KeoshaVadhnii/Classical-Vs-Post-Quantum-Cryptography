from benchmark import benchmark
from rsa import *
from ECC import *
from ML_KEM import *
#import cryptography
import time
import statistics
import os
import csv

#def test_operation():
    #time.sleep(0.001)

iterations = 1000

# Prepare RSA keys and test message
private_key, public_key = generate_rsa_keypair()
message = b"This is a test message for RSA-2048."

#to check that RSA encryption and decryption work correctly
test_ciphertext = encrypt_message(public_key, message)
test_plaintext = decrypt_message(private_key, test_ciphertext)

assert test_plaintext == message

print("RSA encryption/decryption test passed.")

signature = sign_message(
    private_key,
    message
)

assert verify_signature(
    public_key,
    signature,
    message
)

print("RSA signature test passed.")

#RSA key generation
def rsa_key_generation(): generate_rsa_keypair()

key_results = benchmark(rsa_key_generation, iterations=iterations)

#RSA encryption
def rsa_encryption(): encrypt_message(public_key, message)
encryption_results = benchmark(rsa_encryption, iterations=iterations)

# Create ciphertext for decryption benchmark
ciphertext = encrypt_message(public_key, message)

#RSA decryption
def rsa_decryption():
    decrypt_message(private_key, ciphertext)

decryption_results = benchmark(rsa_decryption, iterations=iterations)

#RSA signing
def rsa_signing():
    sign_message(private_key,message)

signing_results = benchmark(rsa_signing, iterations=iterations)

#rsa verification
def rsa_verification():
    verify_signature(public_key, signature, message)

verification_results = benchmark(rsa_verification, iterations=iterations)

#store timing results
results = {
    "Key Generation": key_results,
    "Encryption": encryption_results,
    "Decryption": decryption_results,
    "Signing": signing_results,
    "Verification": verification_results
}

#results = benchmark(test_operation)

#print("Benchmark Results:")
#print(f"Iterations: {results['iterations']}")
#print(f"Mean: {results['mean']:.6f} seconds")
#print(f"Median: {results['median']:.6f} seconds")
#print(f"Minimum: {results['minimum']:.6f} seconds")
#print(f"Maximum: {results['maximum']:.6f} seconds")
#print(f"Standard deviation: {results['standard_deviation']:.6f} seconds")

#print("\nKey Generation")
#print("--------------------------")
#print(f"Iterations: {key_results['iterations']}")
#print(f"Mean: {key_results['mean']:.6f} seconds")
#print(f"Median: {key_results['median']:.6f} seconds")
#print(f"Minimum: {key_results['minimum']:.6f} seconds")
#print(f"Maximum: {key_results['maximum']:.6f} seconds")
#print(f"Standard deviation: {key_results['standard_deviation']:.6f} seconds")

#print("\nEncryption")
#print("--------------------------")
#print(f"Iterations:{encryption_results['iterations']}")
#print(f"Mean: {encryption_results['mean']:.6f} seconds")
#print(f"Median: {encryption_results['median']:.6f} seconds")
#print(f"Minimum: {encryption_results['minimum']:.6f} seconds")
#print(f"Maximum: {encryption_results['maximum']:.6f} seconds")
#print(f"Standard deviation: {encryption_results['standard_deviation']:.6f} seconds")

#print("\nDecryption")
#print("--------------------------")
#print(f"Iterations: {decryption_results['iterations']}")
#print(f"Mean: {decryption_results['mean']:.6f} seconds")
#print(f"Median: {decryption_results['median']:.6f} seconds")
#print(f"Minimum: {decryption_results['minimum']:.6f} seconds")
#print(f"Maximum: {decryption_results['maximum']:.6f} seconds")
#print(f"Standard deviation: {decryption_results['standard_deviation']:.6f} seconds")

# print timing results
for operation, result in results.items():

    print(f"\n{operation}")
    print("--------------------------")

    print(f"Iterations: {result['iterations']}")
    print(f"Mean: {result['mean']:.9f} seconds")
    print(f"Median: {result['median']:.9f} seconds")
    print(f"Minimum: {result['minimum']:.9f} seconds")
    print(f"Maximum: {result['maximum']:.9f} seconds")
    print(
        f"Standard deviation: "
        f"{result['standard_deviation']:.9f} seconds"
    )

# RSA size measurements
key_sizes = get_rsa_key_sizes(
    private_key,
    public_key
)

size_results = {

    "RSA modulus": (
        key_sizes["rsa_modulus_bits"],
        "bits"
    ),

    "RSA modulus bytes": (
        key_sizes["rsa_modulus_bytes"],
        "bytes"
    ),

    "Public key DER": (
        key_sizes["public_key_der_bytes"],
        "bytes"
    ),

    "Private key DER": (
        key_sizes["private_key_der_bytes"],
        "bytes"
    ),

    "Message": (
        len(message),
        "bytes"
    ),

    "Ciphertext": (
        len(ciphertext),
        "bytes"
    ),

    "Signature": (
        len(signature),
        "bytes"
    )
}


print("\nRSA Size Measurements")
print("--------------------------")

for metric, (value, unit) in size_results.items():

    print(
        f"{metric}: "
        f"{value} {unit}"
    )

#ECC test
alice_private_key, alice_public_key = generate_ecc_keypair()
bob_private_key, bob_public_key = generate_ecc_keypair()

#EDCH shared secret test
alice_shared_secret = derive_shared_secret(alice_private_key, bob_public_key)

bob_shared_secret = derive_shared_secret(bob_private_key, alice_public_key)

assert alice_shared_secret == bob_shared_secret

print("\nECC ECDH shared secret test passed.")

#EDCSA signature test
ecc_signature = ecc_sign_message(alice_private_key, message)
assert ecc_verify_signature(
    alice_public_key, ecc_signature, message)
print ("ECC ECDSA signature test passed.")

#ECC key generation
def ecc_key_generation():
    generate_ecc_keypair()


ecc_key_results = benchmark(
    ecc_key_generation,
    iterations=iterations
)

#ECDH shared secret derivation
def ecc_shared_secret_derivation():
    derive_shared_secret(alice_private_key, bob_public_key)

ecc_ecdh_results = benchmark(
    ecc_shared_secret_derivation,
    iterations=iterations
)

#ECDSA signing
def ecc_signing():
    ecc_sign_message(alice_private_key, message)

ecc_signing_results = benchmark(
    ecc_signing, iterations=iterations)

#ECDSA verification
def ecc_verification():
    ecc_verify_signature(alice_public_key,ecc_signature, message)

ecc_verification_results = benchmark(
    ecc_verification, iterations=iterations)

ecc_results = {
    "ECC Key Generation": ecc_key_results,
    "ECDH Shared Secret": ecc_ecdh_results,
    "ECDSA Signing": ecc_signing_results,
    "ECDSA Verification": ecc_verification_results
}

print("\nECC Benchmark Results")
print("==========================")

for operation, result in ecc_results.items():

    print(f"\n{operation}")
    print("--------------------------")

    print(f"Iterations: {result['iterations']}")
    print(f"Mean: {result['mean']:.9f} seconds")
    print(f"Median: {result['median']:.9f} seconds")
    print(f"Minimum: {result['minimum']:.9f} seconds")
    print(f"Maximum: {result['maximum']:.9f} seconds")
    print(
        f"Standard deviation: "
        f"{result['standard_deviation']:.9f} seconds"
    )

ecc_key_sizes = get_ecc_key_sizes(
    alice_private_key,
    alice_public_key
)

ecc_size_results = {

    "ECC curve": (
        ecc_key_sizes["ecc_curve_bits"],
        "bits"
    ),

    "Public key DER": (
        ecc_key_sizes["public_key_der_bytes"],
        "bytes"
    ),

    "Private key DER": (
        ecc_key_sizes["private_key_der_bytes"],
        "bytes"
    ),

    "Public key raw": (
        ecc_key_sizes["public_key_raw_bytes"],
        "bytes"
    ),

    "Shared secret": (
        len(alice_shared_secret),
        "bytes"
    ),

    "Signature": (
        len(ecc_signature),
        "bytes"
    )
}

print("\nECC Size Measurements")
print("--------------------------")

for metric, (value, unit) in ecc_size_results.items():

    print(
        f"{metric}: "
        f"{value} {unit}"
    )

#ML-KEM correctness testing

kem, ml_kem_public_key = generate_ml_kem_keypair()

ml_kem_ciphertext, client_shared_secret = encapsulate_secret(
    ml_kem_public_key)

server_shared_secret = decapsulate_secret(kem, ml_kem_ciphertext)

assert client_shared_secret == server_shared_secret

print("\nML-KEM shared secret test passed.")

#ML-KEM key generation

# ML-KEM key generation

with oqs.KeyEncapsulation(ML_KEM_algorithm) as kem_keygen_test:

    def ml_kem_key_generation():
        kem_keygen_test.generate_keypair()

    ml_kem_key_results = benchmark(
        ml_kem_key_generation,
        iterations=iterations
    )


# ML-KEM encapsulation

with oqs.KeyEncapsulation(ML_KEM_algorithm) as kem_encap_test:

    def ml_kem_encapsulation():
        kem_encap_test.encap_secret(
            ml_kem_public_key
        )

    ml_kem_encapsulation_results = benchmark(
        ml_kem_encapsulation,
        iterations=iterations
    )


# ML-KEM decapsulation

def ml_kem_decapsulation():
    decapsulate_secret(
        kem,
        ml_kem_ciphertext
    )


ml_kem_decapsulation_results = benchmark(
    ml_kem_decapsulation,
    iterations=iterations
)
ml_kem_results = {

    "ML-KEM Key Generation":
        ml_kem_key_results,

    "ML-KEM Encapsulation":
        ml_kem_encapsulation_results,

    "ML-KEM Decapsulation":
        ml_kem_decapsulation_results
}

print("\nML-KEM Benchmark Results")
print("==========================")

for operation, result in ml_kem_results.items():

    print(f"\n{operation}")
    print("--------------------------")

    print(f"Iterations: {result['iterations']}")
    print(f"Mean: {result['mean']:.9f} seconds")
    print(f"Median: {result['median']:.9f} seconds")
    print(f"Minimum: {result['minimum']:.9f} seconds")
    print(f"Maximum: {result['maximum']:.9f} seconds")

    print(
        f"Standard deviation: "
        f"{result['standard_deviation']:.9f} seconds"
    )

ml_kem_sizes = get_ml_kem_sizes(
    ml_kem_public_key,
    ml_kem_ciphertext,
    client_shared_secret,
    kem
)

ml_kem_size_results = {

    "Public key": (
        ml_kem_sizes["public_key_bytes"],
        "bytes"
    ),

    "Secret key": (
        ml_kem_sizes["secret_key_bytes"],
        "bytes"
    ),

    "Ciphertext": (
        ml_kem_sizes["ciphertext_bytes"],
        "bytes"
    ),

    "Shared secret": (
        ml_kem_sizes["shared_secret_bytes"],
        "bytes"
    )
}

print("\nML-KEM Size Measurements")
print("--------------------------")

for metric, (value, unit) in ml_kem_size_results.items():

    print(
        f"{metric}: "
        f"{value} {unit}"
    )
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
