import time
import statistics
def benchmark(operation, iterations=1000):
    #runs cryptographic operations repeatedly

    times = []

    for _ in range(iterations):
        start = time.perf_counter()

        operation()

        end = time.perf_counter()

        elapsed = end - start
        times.append(elapsed)

    return {
        "iterations": iterations,
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "minimum": min(times),
        "maximum": max(times),
        "standard_deviation": statistics.stdev(times)
    }