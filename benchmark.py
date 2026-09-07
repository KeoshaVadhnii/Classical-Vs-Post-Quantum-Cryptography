import time
import statistics
def benchmark(operation, iterations=1000, warmup = 10):

    #warmup to help reduce the effect of initial setup/cache behaviour (not recorded)
    for _ in range(warmup):
        operation()

    times = []

    #runs cryptographic operations repeatedly
    times = []

    for _ in range(iterations):
        start = time.perf_counter_ns()

        operation()

        end = time.perf_counter_ns()

        elapsed_time = (end - start) / 1_000_000_000 #to change nanoseconds to seconds
        times.append(elapsed_time)  #in seconds

    return {
        "iterations": iterations,
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "minimum": min(times),
        "maximum": max(times),
        "standard_deviation": statistics.stdev(times),
        "raw_times": times
    }