from benchmark import benchmark
from rsa import *
import time
import statistics

#def test_operation():
    #time.sleep(0.001)

# Prepare RSA keys and test message
private_key, public_key = generate_rsa_keypair()
message = b"This is a test message for RSA-2048."

#RSA key generation
def rsa_key_generation(): generate_rsa_keypair()

key_results = benchmark(rsa_key_generation, iterations=100)

#RSA encryption
def rsa_encryption(): encrypt_message(public_key, message)
encryption_results = benchmark(rsa_encryption, iterations=100)

# Create ciphertext for decryption benchmark
ciphertext = encrypt_message(public_key, message)

#RSA decryption
def rsa_decryption():
    decrypt_message(private_key, ciphertext)

decryption_results = benchmark(rsa_decryption, iterations=1000)

#results = benchmark(test_operation)

#print("Benchmark Results:")
#print(f"Iterations: {results['iterations']}")
#print(f"Mean: {results['mean']:.6f} seconds")
#print(f"Median: {results['median']:.6f} seconds")
#print(f"Minimum: {results['minimum']:.6f} seconds")
#print(f"Maximum: {results['maximum']:.6f} seconds")
#print(f"Standard deviation: {results['standard_deviation']:.6f} seconds")

print("\nKey Generation")
print("--------------------------")
print(f"Iterations: {key_results['iterations']}")
print(f"Mean: {key_results['mean']:.6f} seconds")
print(f"Median: {key_results['median']:.6f} seconds")
print(f"Minimum: {key_results['minimum']:.6f} seconds")
print(f"Maximum: {key_results['maximum']:.6f} seconds")
print(f"Standard deviation: {key_results['standard_deviation']:.6f} seconds")

print("\nEncryption")
print("--------------------------")
print(f"Iterations:{encryption_results['iterations']}")
print(f"Mean: {encryption_results['mean']:.6f} seconds")
print(f"Median: {encryption_results['median']:.6f} seconds")
print(f"Minimum: {encryption_results['minimum']:.6f} seconds")
print(f"Maximum: {encryption_results['maximum']:.6f} seconds")
print(f"Standard deviation: {encryption_results['standard_deviation']:.6f} seconds")

print("\nDecryption")
print("--------------------------")
print(f"Iterations: {decryption_results['iterations']}")
print(f"Mean: {decryption_results['mean']:.6f} seconds")
print(f"Median: {decryption_results['median']:.6f} seconds")
print(f"Minimum: {decryption_results['minimum']:.6f} seconds")
print(f"Maximum: {decryption_results['maximum']:.6f} seconds")
print(f"Standard deviation: {decryption_results['standard_deviation']:.6f} seconds")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
