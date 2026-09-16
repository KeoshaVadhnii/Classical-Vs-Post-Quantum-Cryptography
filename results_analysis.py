import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load benchmark data
performance_df = pd.read_csv(
    "results/performance_results.csv"
)

size_df = pd.read_csv(
    "results/size_results.csv"
)

print("Performance dataset")
print("===================")
print(f"Rows: {len(performance_df)}")
print(f"Columns: {len(performance_df.columns)}")
print(f"Runs: {sorted(performance_df['run_id'].unique())}")

print("\nPerformance rows per run:")
print(performance_df.groupby("run_id").size())


print("\nSize dataset")
print("============")
print(f"Rows: {len(size_df)}")
print(f"Columns: {len(size_df.columns)}")
print(f"Runs: {sorted(size_df['run_id'].unique())}")

print("\nSize rows per run:")
print(size_df.groupby("run_id").size())

# performance summary of the 5 runs
performance_summary = (
    performance_df
    .groupby(["algorithm", "operation"])
    .agg(
        average_mean_seconds=("mean_seconds", "mean"),
        between_run_std_seconds=("mean_seconds", "std"),
        average_median_seconds=("median_seconds", "mean"),
        minimum_seconds=("minimum_seconds", "min"),
        maximum_seconds=("maximum_seconds", "max"),
        average_cpu_time_per_operation=(
            "cpu_time_per_operation", "mean"
        ),
        average_cpu_utilisation_percent=(
            "cpu_utilisation_percent", "mean"
        )
    )
    .reset_index()
)

# Convert seconds to milliseconds for easier interpretation
performance_summary["average_mean_ms"] = (
    performance_summary["average_mean_seconds"] * 1000
)

performance_summary["between_run_std_ms"] = (
    performance_summary["between_run_std_seconds"] * 1000
)

performance_summary["average_median_ms"] = (
    performance_summary["average_median_seconds"] * 1000
)

performance_summary["minimum_ms"] = (
    performance_summary["minimum_seconds"] * 1000
)

performance_summary["maximum_ms"] = (
    performance_summary["maximum_seconds"] * 1000
)

performance_summary["average_cpu_time_per_operation_ms"] = (
    performance_summary["average_cpu_time_per_operation"] * 1000
)

print("\nFive-Run Performance Summary")
print("============================")

print(
    performance_summary[
        [
            "algorithm",
            "operation",
            "average_mean_ms",
            "between_run_std_ms",
            "average_median_ms",
            "average_cpu_time_per_operation_ms",
            "average_cpu_utilisation_percent"
        ]
    ].to_string(index=False)
)

# Save summary table
performance_summary.to_csv(
    "results/performance_summary.csv",
    index=False
)

#digital Signature peerformance comparison
signature_algorithms = [
    "RSA-2048",
    "ECC P-256",
    "ML-DSA-44",
    "ML-DSA-65",
    "ML-DSA-87"
]

signature_performance = performance_summary[
    performance_summary["algorithm"].isin(signature_algorithms)
    &
    performance_summary["operation"].isin([
        "Signing",
        "Verification",
        "ECDSA Signing",
        "ECDSA Verification"
    ])
].copy()

# Standardise ECC operation names
signature_performance["operation_type"] = (
    signature_performance["operation"].replace({
        "ECDSA Signing": "Signing",
        "ECDSA Verification": "Verification"
    })
)

signature_pivot = signature_performance.pivot(
    index="algorithm",
    columns="operation_type",
    values=[
        "average_mean_ms",
        "between_run_std_ms"
    ]
)

signature_pivot.columns = [
    "_".join(column)
    for column in signature_pivot.columns
]

signature_pivot = signature_pivot.reset_index()

# Control algorithm order
algorithm_order = [
    "RSA-2048",
    "ECC P-256",
    "ML-DSA-44",
    "ML-DSA-65",
    "ML-DSA-87"
]

signature_pivot["algorithm"] = pd.Categorical(
    signature_pivot["algorithm"],
    categories=algorithm_order,
    ordered=True
)

signature_pivot = (
    signature_pivot
    .sort_values("algorithm")
    .reset_index(drop=True)
)

# Create publication-friendly mean ± SD columns
signature_pivot["Signing time (ms)"] = (
    signature_pivot["average_mean_ms_Signing"]
    .map(lambda x: f"{x:.4f}")
    + " ± "
    + signature_pivot["between_run_std_ms_Signing"]
    .map(lambda x: f"{x:.4f}")
)

signature_pivot["Verification time (ms)"] = (
    signature_pivot["average_mean_ms_Verification"]
    .map(lambda x: f"{x:.4f}")
    + " ± "
    + signature_pivot["between_run_std_ms_Verification"]
    .map(lambda x: f"{x:.4f}")
)

signature_dissertation_table = signature_pivot[
    [
        "algorithm",
        "Signing time (ms)",
        "Verification time (ms)"
    ]
]

print("\nDigital Signature Performance Comparison")
print("========================================")

print(
    signature_dissertation_table.to_string(
        index=False
    )
)

signature_dissertation_table.to_csv(
    "results/signature_performance.csv",
    index=False
)

#signature signing performance chart
signing_data = signature_performance[
    signature_performance["operation_type"] == "Signing"
].copy()

signing_data["algorithm"] = pd.Categorical(
    signing_data["algorithm"],
    categories=algorithm_order,
    ordered=True
)

signing_data = signing_data.sort_values("algorithm")

plt.figure(figsize=(9, 6))

plt.bar(
    signing_data["algorithm"],
    signing_data["average_mean_ms"],
    yerr=signing_data["between_run_std_ms"],
    capsize=5
)

plt.xlabel("Algorithm")
plt.ylabel("Mean signing time (ms)")
plt.title("Digital Signature Generation Performance")

plt.tight_layout()

plt.savefig(
    "results/signature_signing_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

#signature verification performance
verification_data = signature_performance[
    signature_performance["operation_type"] == "Verification"
].copy()

verification_data["algorithm"] = pd.Categorical(
    verification_data["algorithm"],
    categories=algorithm_order,
    ordered=True
)

verification_data = verification_data.sort_values("algorithm")

plt.figure(figsize=(9, 6))

plt.bar(
    verification_data["algorithm"],
    verification_data["average_mean_ms"],
    yerr=verification_data["between_run_std_ms"],
    capsize=5
)

plt.xlabel("Algorithm")
plt.ylabel("Mean verification time (ms)")
plt.title("Digital Signature Verification Performance")

plt.tight_layout()

plt.savefig(
    "results/signature_verification_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

#signature size comparison
signature_size_data = size_df[
    (size_df["measurement"] == "Signature")
    &
    (size_df["algorithm"].isin(algorithm_order))
].copy()

signature_size_summary = (
    signature_size_data
    .groupby("algorithm")
    .agg(
        mean_signature_bytes=("size_bytes", "mean"),
        minimum_signature_bytes=("size_bytes", "min"),
        maximum_signature_bytes=("size_bytes", "max")
    )
    .reset_index()
)

signature_size_summary["algorithm"] = pd.Categorical(
    signature_size_summary["algorithm"],
    categories=algorithm_order,
    ordered=True
)

signature_size_summary = (
    signature_size_summary
    .sort_values("algorithm")
    .reset_index(drop=True)
)

print("\nDigital Signature Size Comparison")
print("=================================")

print(
    signature_size_summary.to_string(
        index=False,
        float_format=lambda x: f"{x:.1f}"
    )
)

signature_size_summary.to_csv(
    "results/signature_size_summary.csv",
    index=False
)

plt.figure(figsize=(9, 6))

bars = plt.bar(
    signature_size_summary["algorithm"],
    signature_size_summary["mean_signature_bytes"]
)

plt.xlabel("Algorithm")
plt.ylabel("Signature size (bytes)")
plt.title("Digital Signature Size Comparison")

# Add exact byte values above bars
for bar, value in zip(
    bars,
    signature_size_summary["mean_signature_bytes"]
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.0f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "results/signature_size_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

#key generation performance comparison
key_algorithms = [
    "RSA-2048",
    "ECC P-256",
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024"
]

key_generation_data = performance_summary[
    performance_summary["algorithm"].isin(key_algorithms)
    &
    performance_summary["operation"].isin([
        "Key Generation",
        "ECC Key Generation"
    ])
].copy()

key_generation_data["operation"] = (
    key_generation_data["operation"]
    .replace({
        "ECC Key Generation": "Key Generation"
    })
)

key_generation_data["algorithm"] = pd.Categorical(
    key_generation_data["algorithm"],
    categories=key_algorithms,
    ordered=True
)

key_generation_data = (
    key_generation_data
    .sort_values("algorithm")
    .reset_index(drop=True)
)

key_generation_table = key_generation_data[
    [
        "algorithm",
        "average_mean_ms",
        "between_run_std_ms"
    ]
].copy()

key_generation_table["Key generation time (ms)"] = (
    key_generation_table["average_mean_ms"]
    .map(lambda x: f"{x:.4f}")
    + " ± "
    + key_generation_table["between_run_std_ms"]
    .map(lambda x: f"{x:.4f}")
)

key_generation_table = key_generation_table[
    [
        "algorithm",
        "Key generation time (ms)"
    ]
]

print("\nKey Generation Performance")
print("==========================")

print(
    key_generation_table.to_string(
        index=False
    )
)

key_generation_table.to_csv(
    "results/key_generation_performance.csv",
    index=False
)

#key generation chart
plt.figure(figsize=(9, 6))

bars = plt.bar(
    key_generation_data["algorithm"],
    key_generation_data["average_mean_ms"],
    yerr=key_generation_data["between_run_std_ms"],
    capsize=5
)

plt.yscale("log")

plt.xlabel("Algorithm")
plt.ylabel("Mean key generation time (ms, log scale)")
plt.title("Key Generation Performance")

# Add exact values above each bar
for bar, value in zip(
    bars,
    key_generation_data["average_mean_ms"]
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value * 1.15,
        f"{value:.4f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "results/key_generation_performance_log.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Classical key agreement and confidentiality
key_establishment_data = performance_summary[
    (
        (performance_summary["algorithm"] == "RSA-2048")
        &
        (performance_summary["operation"].isin([
            "Encryption",
            "Decryption"
        ]))
    )
    |
    (
        (performance_summary["algorithm"] == "ECC P-256")
        &
        (performance_summary["operation"] == "ECDH Shared Secret")
    )
    |
    (
        performance_summary["algorithm"].isin([
            "ML-KEM-512",
            "ML-KEM-768",
            "ML-KEM-1024"
        ])
        &
        performance_summary["operation"].isin([
            "Encapsulation",
            "Decapsulation"
        ])
    )
].copy()

classical_operations = key_establishment_data[
    key_establishment_data["algorithm"].isin([
        "RSA-2048",
        "ECC P-256"
    ])
].copy()

classical_operations["Mean time (ms)"] = (
    classical_operations["average_mean_ms"]
    .map(lambda x: f"{x:.4f}")
    + " ± "
    + classical_operations["between_run_std_ms"]
    .map(lambda x: f"{x:.4f}")
)

# Make wording clearer
classical_operations["operation"] = (
    classical_operations["operation"].replace({
        "ECDH Shared Secret": "ECDH shared-secret derivation"
    })
)

classical_table = classical_operations[
    [
        "algorithm",
        "operation",
        "Mean time (ms)"
    ]
].copy()

# Control order
classical_order = [
    ("RSA-2048", "Encryption"),
    ("RSA-2048", "Decryption"),
    ("ECC P-256", "ECDH shared-secret derivation")
]

classical_table["sort_order"] = classical_table.apply(
    lambda row: classical_order.index(
        (row["algorithm"], row["operation"])
    ),
    axis=1
)

classical_table = (
    classical_table
    .sort_values("sort_order")
    .drop(columns="sort_order")
    .reset_index(drop=True)
)

print("\nClassical Cryptographic Operations")
print("=================================")

print(
    classical_table.to_string(
        index=False
    )
)

classical_table.to_csv(
    "results/classical_operations_performance.csv",
    index=False
)

# ML-KEM performance table
# ==========================================

ml_kem_data = key_establishment_data[
    key_establishment_data["algorithm"].isin([
        "ML-KEM-512",
        "ML-KEM-768",
        "ML-KEM-1024"
    ])
].copy()

ml_kem_pivot = ml_kem_data.pivot(
    index="algorithm",
    columns="operation",
    values=[
        "average_mean_ms",
        "between_run_std_ms"
    ]
)

ml_kem_pivot.columns = [
    "_".join(column)
    for column in ml_kem_pivot.columns
]

ml_kem_pivot = ml_kem_pivot.reset_index()

ml_kem_order = [
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024"
]

ml_kem_pivot["algorithm"] = pd.Categorical(
    ml_kem_pivot["algorithm"],
    categories=ml_kem_order,
    ordered=True
)

ml_kem_pivot = (
    ml_kem_pivot
    .sort_values("algorithm")
    .reset_index(drop=True)
)

ml_kem_pivot["Encapsulation time (ms)"] = (
    ml_kem_pivot["average_mean_ms_Encapsulation"]
    .map(lambda x: f"{x:.4f}")
    + " ± "
    + ml_kem_pivot["between_run_std_ms_Encapsulation"]
    .map(lambda x: f"{x:.4f}")
)

ml_kem_pivot["Decapsulation time (ms)"] = (
    ml_kem_pivot["average_mean_ms_Decapsulation"]
    .map(lambda x: f"{x:.4f}")
    + " ± "
    + ml_kem_pivot["between_run_std_ms_Decapsulation"]
    .map(lambda x: f"{x:.4f}")
)

ml_kem_table = ml_kem_pivot[
    [
        "algorithm",
        "Encapsulation time (ms)",
        "Decapsulation time (ms)"
    ]
]

print("\nML-KEM Performance")
print("==================")

print(
    ml_kem_table.to_string(
        index=False
    )
)

ml_kem_table.to_csv(
    "results/ml_kem_performance.csv",
    index=False
)

# Key and ciphertext size comparison
def get_mean_size(algorithm, measurement):
    values = size_df[
        (size_df["algorithm"] == algorithm)
        &
        (size_df["measurement"] == measurement)
    ]["size_bytes"]

    if len(values) == 0:
        return None

    return values.mean()


size_overhead_table = pd.DataFrame([
    {
        "Algorithm": "RSA-2048",
        "Public key (bytes)": get_mean_size(
            "RSA-2048", "Public key DER"
        ),
        "Private/secret key (bytes)": get_mean_size(
            "RSA-2048", "Private key DER"
        ),
        "Ciphertext (bytes)": get_mean_size(
            "RSA-2048", "Ciphertext"
        )
    },

    {
        "Algorithm": "ECC P-256",
        "Public key (bytes)": get_mean_size(
            "ECC P-256", "Public key DER"
        ),
        "Private/secret key (bytes)": get_mean_size(
            "ECC P-256", "Private key DER"
        ),
        "Ciphertext (bytes)": None
    },

    {
        "Algorithm": "ML-KEM-512",
        "Public key (bytes)": get_mean_size(
            "ML-KEM-512", "Public key"
        ),
        "Private/secret key (bytes)": get_mean_size(
            "ML-KEM-512", "Secret key"
        ),
        "Ciphertext (bytes)": get_mean_size(
            "ML-KEM-512", "Ciphertext"
        )
    },

    {
        "Algorithm": "ML-KEM-768",
        "Public key (bytes)": get_mean_size(
            "ML-KEM-768", "Public key"
        ),
        "Private/secret key (bytes)": get_mean_size(
            "ML-KEM-768", "Secret key"
        ),
        "Ciphertext (bytes)": get_mean_size(
            "ML-KEM-768", "Ciphertext"
        )
    },

    {
        "Algorithm": "ML-KEM-1024",
        "Public key (bytes)": get_mean_size(
            "ML-KEM-1024", "Public key"
        ),
        "Private/secret key (bytes)": get_mean_size(
            "ML-KEM-1024", "Secret key"
        ),
        "Ciphertext (bytes)": get_mean_size(
            "ML-KEM-1024", "Ciphertext"
        )
    }
])


print("\nKey and Ciphertext Size Comparison")
print("==================================")

print(
    size_overhead_table.to_string(
        index=False,
        na_rep="N/A",
        float_format=lambda x: f"{x:.0f}"
    )
)

size_overhead_table.to_csv(
    "results/key_ciphertext_size_summary.csv",
    index=False)

#key and iphertext chart
x = np.arange(len(size_overhead_table))
bar_width = 0.25

plt.figure(figsize=(10, 6))

plt.bar(
    x - bar_width,
    size_overhead_table["Public key (bytes)"],
    width=bar_width,
    label="Public key"
)

plt.bar(
    x,
    size_overhead_table["Private/secret key (bytes)"],
    width=bar_width,
    label="Private / secret key"
)

plt.bar(
    x + bar_width,
    size_overhead_table["Ciphertext (bytes)"],
    width=bar_width,
    label="Ciphertext"
)

# Add value labels above bars
for container in plt.gca().containers:
    plt.bar_label(
        container,
        fmt="%.0f",
        padding=3
    )

plt.xticks(
    x,
    size_overhead_table["Algorithm"]
)

plt.xlabel("Algorithm")
plt.ylabel("Size (bytes)")
plt.title("Key and Ciphertext Size Comparison")

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/key_ciphertext_size_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()