from benchmark import benchmark
from system_info import get_system_info
from resource_benchmark import (cpu_benchmark,memory_benchmark)
from rsa import *
from ECC import *
from ML_KEM import *
from ML_DSA import *
#import cryptography
import time
import statistics
import os
import csv

#def test_operation():
    #time.sleep(0.001)

iterations = 1000

#System Info

system_information = get_system_info()

print("\nSystem Information")
print("==========================")

for item, value in system_information.items():
    print(f"{item}: {value}")
print("\n=============================\n")

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

rsa_cpu_results =  {
    "Key Generation": cpu_benchmark(rsa_key_generation),
    "Encryption": cpu_benchmark(rsa_encryption),
    "Decryption": cpu_benchmark(rsa_decryption),
    "Signing": cpu_benchmark(rsa_signing),
    "Verification": cpu_benchmark(rsa_verification),
}

rsa_memory_results = {
"Key Generation":memory_benchmark(rsa_key_generation),
    "Encryption":memory_benchmark(rsa_encryption),
    "Decryption":memory_benchmark(rsa_decryption),
    "Signing": memory_benchmark(rsa_signing),
    "Verification":memory_benchmark(rsa_verification)
}

# print timing results
for operation, result in results.items():
    cpu = rsa_cpu_results[operation]
    memory = rsa_memory_results[operation]

    print(f"\n{operation}")
    print("--------------------------")

    #timing
    print(f"Iterations: {result['iterations']}")
    print(f"Mean: {result['mean']:.9f} seconds")
    print(f"Median: {result['median']:.9f} seconds")
    print(f"Minimum: {result['minimum']:.9f} seconds")
    print(f"Maximum: {result['maximum']:.9f} seconds")
    print(
        f"Standard deviation: "
        f"{result['standard_deviation']:.9f} seconds"
    )

    #CPU
    print(f"CPU Iterations: {cpu['iterations']}")
    print(f"Wall time: "f"{cpu['wall_time_seconds']:.6f} seconds")
    print(f"Total CPU time: "f"{cpu['cpu_time_seconds']:.6f} seconds")
    #print(f"CPU time per operation: " f"{cpu['cpu_time_per_operation']:.9f} seconds")
    print(f"CPU utilisation (one-core basis): " f"{cpu['cpu_utilisation']:.2f}%")


    #Memory
    print(f"Memory Iterations: "f"{memory['iterations']}")
    print(f"Memory before: " f"{memory['memory_before_mb']:.4f} MB")
    print(f"Memory after: " f"{memory['memory_after_mb']:.4f} MB")
    print(f"Peak memory: " f"{memory['peak_memory_mb']:.4f} MB")
    print(f"Peak memory increase: " f"{memory['peak_memory_increase_kb']:.2f} KB")


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

    # Average CPU time per RSA operation
print("\nRSA Average CPU Time per Operation")
print("===================================")

for operation, cpu in rsa_cpu_results.items():
    print(
        f"{operation}: "
        f"{cpu['cpu_time_per_operation']:.9f} "
        f"seconds/operation"
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

ecc_cpu_results = {
    "ECC Key Generation": cpu_benchmark(ecc_key_generation),
    "ECDH Shared Secret": cpu_benchmark(ecc_shared_secret_derivation),
    "ECDSA Signing": cpu_benchmark(ecc_signing),
    "ECDSA Verification": cpu_benchmark(ecc_verification)
}

ecc_memory_results = {
    "ECC Key Generation": memory_benchmark(ecc_key_generation),
    "ECDH Shared Secret": memory_benchmark(ecc_shared_secret_derivation),
    "ECDSA Signing": memory_benchmark(ecc_signing),
    "ECDSA Verification": memory_benchmark(ecc_verification)
}

print("\nECC Benchmark Results")
print("==========================")

for operation, result in ecc_results.items():

    cpu = ecc_cpu_results[operation]
    memory = ecc_memory_results[operation]

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

    # CPU
    print(f"CPU Iterations: {cpu['iterations']}")
    print(f"Wall time: "f"{cpu['wall_time_seconds']:.6f} seconds")
    print(f"Total CPU time: "f"{cpu['cpu_time_seconds']:.6f} seconds")
    # print(f"CPU time per operation: " f"{cpu['cpu_time_per_operation']:.9f} seconds")
    print(f"CPU utilisation (one-core basis): " f"{cpu['cpu_utilisation']:.2f}%")

    # Memory
    print(f"Memory Iterations: "f"{memory['iterations']}")
    print(f"Memory before: " f"{memory['memory_before_mb']:.4f} MB")
    print(f"Memory after: " f"{memory['memory_after_mb']:.4f} MB")
    print(f"Peak memory: " f"{memory['peak_memory_mb']:.4f} MB")
    print(f"Peak memory increase: " f"{memory['peak_memory_increase_kb']:.2f} KB")

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

print("\nECC Average CPU Time per Operation")
print("===================================")

for operation, cpu in ecc_cpu_results.items():

    print(
        f"{operation}: "
        f"{cpu['cpu_time_per_operation']:.9f} "
        f"seconds/operation"
    )

#ML-KEM testing and benchmarking
all_ml_kem_results = {}
all_ml_kem_sizes = {}

all_ml_kem_cpu_results = {}
all_ml_kem_memory_results = {}

for algorithm in ML_KEM_algorithm:
    print(f"\n===========================")
    print(f"{algorithm}")
    print(f"===============================")

    kem, ml_kem_public_key = generate_ml_kem_keypair(algorithm)

    ml_kem_ciphertext, client_shared_secret = encapsulate_secret(
        ml_kem_public_key,algorithm)

    server_shared_secret = decapsulate_secret(kem, ml_kem_ciphertext)

    assert client_shared_secret == server_shared_secret

    print(f"{algorithm} shared secret test passed")


    #ML-KEM key generation

    with oqs.KeyEncapsulation(algorithm) as kem_keygen_test:

        def ml_kem_key_generation():
            kem_keygen_test.generate_keypair()

        ml_kem_key_results = benchmark(
            ml_kem_key_generation,
            iterations=iterations
        )

        ml_kem_key_cpu = cpu_benchmark(ml_kem_key_generation)

        ml_kem_key_memory = memory_benchmark(ml_kem_key_generation)


    # ML-KEM encapsulation

    with oqs.KeyEncapsulation(algorithm) as kem_encap_test:

        def ml_kem_encapsulation():
            kem_encap_test.encap_secret(
                ml_kem_public_key
            )

        ml_kem_encapsulation_results = benchmark(
            ml_kem_encapsulation,
            iterations=iterations
        )

        ml_kem_encapsulation_cpu = cpu_benchmark(ml_kem_encapsulation)

        ml_kem_encapsulation_memory = memory_benchmark(ml_kem_encapsulation)


    # ML-KEM decapsulation

    def ml_kem_decapsulation():
        decapsulate_secret(
            kem,
            ml_kem_ciphertext
        )

    ml_kem_decapsulation_results = benchmark(ml_kem_decapsulation, iterations=iterations)

    ml_kem_decapsulation_cpu = cpu_benchmark(ml_kem_decapsulation)

    ml_kem_decapsulation_memory = memory_benchmark(ml_kem_decapsulation)


    ml_kem_results = {

        "Key Generation":
            ml_kem_key_results,

        "Encapsulation":
            ml_kem_encapsulation_results,

        "Decapsulation":
            ml_kem_decapsulation_results
    }

    ml_kem_cpu_results = {
        "Key Generation": ml_kem_key_cpu,
        "Encapsulation": ml_kem_encapsulation_cpu,
        "Decapsulation": ml_kem_decapsulation_cpu
    }

    ml_kem_memory_results = {
        "Key Generation": ml_kem_key_memory,
        "Encapsulation": ml_kem_encapsulation_memory,
        "Decapsulation": ml_kem_decapsulation_memory
    }

    all_ml_kem_results[algorithm] = ml_kem_results
    all_ml_kem_cpu_results[algorithm] = ml_kem_cpu_results
    all_ml_kem_memory_results[algorithm] = ml_kem_memory_results


    print("\nBenchmark Results")
    print("==========================")

    print(f"{algorithm} benchmark results")
    print("==================================")

    for operation, result in ml_kem_results.items():
        cpu = ml_kem_cpu_results[operation]
        memory = ml_kem_memory_results[operation]

        print(f"\n{operation}")
        print("--------------------------")

        #timing
        print(f"Iterations: {result['iterations']}")
        print(f"Mean: {result['mean']:.9f} seconds")
        print(f"Median: {result['median']:.9f} seconds")
        print(f"Minimum: {result['minimum']:.9f} seconds")
        print(f"Maximum: {result['maximum']:.9f} seconds")

        print(
            f"Standard deviation: "
            f"{result['standard_deviation']:.9f} seconds"
        )

        #cpu
        print(f"CPU Iterations: {cpu['iterations']}")
        print(f"Wall time:"
              f"{cpu['wall_time_seconds']:.6f} seconds")
        print(f"Total CPU time: " f"{cpu['cpu_time_seconds']:.6f} seconds")
        print(f"CPU utilisation: {cpu['cpu_utilisation']:.2f} %")

        #memory
        print(f"Memory Iterations: " f"{memory['iterations']}")
        print(f"Memory before: " f"{memory['memory_before_mb']:.4f} MB")
        print(f"Memory after: " f"{memory['memory_after_mb']:.4f} MB")
        print(f"Peak memory: " f"{memory['peak_memory_mb']:.4f} MB")
        print(f"Peak memory increase: " f"{memory['peak_memory_increase_kb']:.2f} KB")


    #size measurements
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

    all_ml_kem_sizes[algorithm] = ml_kem_size_results

    print("\nML-KEM Size Measurements")
    print("--------------------------")

    for metric, (value, unit) in ml_kem_size_results.items():

        print(
            f"{metric}: "
            f"{value} {unit}"
        )

    print(f"\n{algorithm} Average CPU Time per Operation")
    print("------------------------")

    for operation, cpu, in ml_kem_cpu_results.items():

        print(f"{operation}: " f"{cpu['cpu_time_per_operation']:.9f} " f"seconds/operation")

#ML-DSA correctness testing

all_ml_dsa_results = {}
all_ml_dsa_sizes = {}

all_ml_dsa_cpu_results = {}
all_ml_dsa_memory_results = {}

for algorithm in ML_DSA_algorithms:
    print("\n=====================\n")
    print(algorithm)
    print("======================")



    ml_dsa_signer, ml_dsa_public_key = generate_ml_dsa_keypair(algorithm)

    ml_dsa_signature = sign_ml_dsa_message(ml_dsa_signer, message)

    ml_dsa_valid = verify_ml_dsa_signature(ml_dsa_public_key, ml_dsa_signature, message, algorithm)

    assert ml_dsa_valid

    print(f"{algorithm} signature passed")

    #key generation benchmark
    with oqs.Signature(algorithm) as ml_dsa_keygen_test:

        def ml_dsa_key_generation():
            ml_dsa_keygen_test.generate_keypair()

        ml_dsa_key_results = benchmark(ml_dsa_key_generation,iterations=iterations)

        ml_dsa_key_cpu_results = cpu_benchmark(ml_dsa_key_generation)

        ml_dsa_key_memory_results = memory_benchmark(ml_dsa_key_generation)

    #signing benchmark
    def ml_dsa_signing():
        sign_ml_dsa_message(ml_dsa_signer, message)

    ml_dsa_signing_results = benchmark(ml_dsa_signing,iterations=iterations)

    ml_dsa_signing_cpu_results = cpu_benchmark(ml_dsa_signing)

    ml_dsa_signing_memory_results = memory_benchmark(ml_dsa_signing)

    #verification benchmark
    with oqs.Signature(algorithm) as ml_dsa_verifier:

        def ml_dsa_verification():
            ml_dsa_verifier.verify(message, ml_dsa_signature, ml_dsa_public_key)

        ml_dsa_verification_results = benchmark(ml_dsa_verification,iterations=iterations)

        ml_dsa_verification_cpu_results = cpu_benchmark(ml_dsa_verification)

        ml_dsa_verification_memory_results = memory_benchmark(ml_dsa_verification)

    #store timing results

    ml_dsa_results = {
        "Key Generation": ml_dsa_key_results,
        "Signing": ml_dsa_signing_results,
        "Verification": ml_dsa_verification_results
    }

    ml_dsa_cpu_results = {
        "Key Generation": ml_dsa_key_cpu_results,
        "Signing": ml_dsa_signing_cpu_results,
        "Verification": ml_dsa_verification_cpu_results
    }

    ml_dsa_memory_results = {
        "Key Generation": ml_dsa_key_memory_results,
        "Signing": ml_dsa_signing_memory_results,
        "Verification": ml_dsa_verification_memory_results
    }

    all_ml_dsa_results[algorithm] = ml_dsa_results
    all_ml_dsa_cpu_results[algorithm] = ml_dsa_cpu_results
    all_ml_dsa_memory_results[algorithm] = ml_dsa_memory_results

    #Print benchmark results
    print(f"\n{algorithm} Benchmarks Results")
    print("==========================")

    for operation, result in ml_dsa_results.items():

        cpu = ml_dsa_cpu_results[operation]
        memory = ml_dsa_memory_results[operation]

        print(f"\n{operation}")
        print("----------------------")

        print(f"Iterations: {result['iterations']}")
        print(f"Mean: {result['mean']:.9f} seconds")
        print(f"Median: {result['median']:.9f} seconds")
        print(f"Minimum: {result['minimum']:.9f} seconds")
        print(f"Maximum: {result['maximum']:.9f} seconds")
        print(f"Standard deviation: {result['standard_deviation']:.9f} seconds")

        #CPU
        print(f"CPU Iterations: {cpu['iterations']}")
        print(f"Wall Time: " f"{cpu['wall_time_seconds']:.9f} seconds")
        print(f"Total CPU Time: " f"{cpu['cpu_time_seconds']:.9f} seconds")
        print(f"CPU Utilisation: " f"{cpu['cpu_utilisation']:.2f} %")

        #Memory
        print(f"Memory Iterations:" f"{memory['iterations']}")
        print(f"Memory before: " f"{memory['memory_before_mb']:.4f} MB")
        print(f"Memory after: " f"{memory['memory_after_mb']:.4f} MB")
        print("Peak Memory: " f"{memory['peak_memory_mb']:.4f} MB")
        print(f"Peak Memory Increase: " f"{memory['peak_memory_increase_kb']:.2f} KB")


    #Size measurements
    ml_dsa_sizes = get_ml_dsa_sizes(ml_dsa_public_key, ml_dsa_signature, ml_dsa_signer)

    ml_dsa_size_results = {
        "Public key": (ml_dsa_sizes["public_key_bytes"], "bytes"),
        "Secret key": (ml_dsa_sizes["secret_key_bytes"], "bytes"),
        "Signature": (ml_dsa_sizes["signature_bytes"], "bytes"),
    }

    all_ml_dsa_sizes[algorithm] = ml_dsa_size_results

    print(f"\n{algorithm} Size Measurements")
    print("--------------------------")
    for metric, (value, unit) in ml_dsa_size_results.items():
        print(
            f"{metric}: "
            f"{value} {unit}"
        )

    print(
        f"\n{algorithm} Average CPU Time per Operation"
    )
    print("------------------------")

    for operation, cpu in ml_dsa_cpu_results.items():
        print(
            f"{operation}: "
            f"{cpu['cpu_time_per_operation']:.9f} "
            f"seconds/operation"
        )

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
