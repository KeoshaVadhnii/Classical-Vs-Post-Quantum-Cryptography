from benchmark import benchmark
from rsa import *
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
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
