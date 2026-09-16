import csv
import os

RESULTS_FOLDER = "results"

def save_performance_result( run_id, algorithm, operation, timing, cpu, memory):

    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    file_path = os.path.join(RESULTS_FOLDER, "performance_results.csv")

    file_exists = os.path.exists(file_path)

    fileIdnames = [
        "run_id",
        "algorithm",
        "operation",

        "timing_iterations",
        "mean_seconds",
        "median_seconds",
        "minimum_seconds",
        "maximum_seconds",
        "standard_deviation_seconds",

        "cpu_iterations",
        "cpu_wall_time_seconds",
        "total_cpu_time_seconds",
        "cpu_time_per_operation",
        "cpu_utilisation_percent",

        "memory_iterations",
        "memory_before_mb",
        "memory_after_mb",
        "peak_memory_mb",
        "peak_memory_increase_kb"
    ]

    row = {
        "run_id": run_id,
        "algorithm": algorithm,
        "operation": operation,

        "timing_iterations": timing["iterations"],
        "mean_seconds": timing["mean"],
        "median_seconds": timing["median"],
        "minimum_seconds": timing["minimum"],
        "maximum_seconds": timing["maximum"],
        "standard_deviation_seconds": timing["standard_deviation"],

        "cpu_iterations": cpu["iterations"],
        "cpu_wall_time_seconds": cpu["wall_time_seconds"],
        "total_cpu_time_seconds": cpu["cpu_time_seconds"],
        "cpu_time_per_operation": cpu["cpu_time_per_operation"],
        "cpu_utilisation_percent": cpu["cpu_utilisation"],

        "memory_iterations": memory["iterations"],
        "memory_before_mb": memory["memory_before_mb"],
        "memory_after_mb": memory["memory_after_mb"],
        "peak_memory_mb": memory["peak_memory_mb"],
        "peak_memory_increase_kb": memory["peak_memory_increase_kb"]
    }

    with open(file_path, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fileIdnames)

        if not file_exists:
            writer. writeheader()
        writer.writerow(row)

def save_size_result(
        run_id,
        algorithm,
        measurement,
        size_bytes
):
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    file_path = os.path.join(RESULTS_FOLDER, "size_results.csv")

    file_exists = os.path.exists(file_path)

    fileIdnames = [
        "run_id",
        "algorithm",
        "measurement",
        "size_bytes"
    ]

    row = {
        "run_id": run_id,
        "algorithm": algorithm,
        "measurement": measurement,
        "size_bytes": size_bytes
    }

    with open(file_path, "a", newline="") as file:
        write = csv.DictWriter(file, fieldnames=fileIdnames)

        if not file_exists:
            write. writeheader()

        write. writerow(row)
