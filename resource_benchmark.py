import os
import time
import threading
import psutil

def warm_up(operation, warmup=10):
    for _ in range(warmup):
        operation()

#CPU benchmarking

def cpu_benchmark (operation, minimum_duration=3.0, minimum_iterations=100, warmup=10):

    warm_up(operation,warmup)

    process = psutil.Process(os.getpid())

    cpu_before = process.cpu_times()

    wall_start = time.perf_counter()

    iterations = 0

    while True:
        operation()
        iterations += 1

        if iterations >= minimum_iterations:
            elapsed = time.perf_counter() - wall_start
            if elapsed >= minimum_duration:
                break

    wall_end = time.perf_counter()

    cpu_after = process.cpu_times()

    wall_time = wall_end - wall_start

    cpu_time = (
        (cpu_after.user - cpu_before.user) + (cpu_after.system - cpu_before.system)
    )

    return {
        "iterations": iterations,
        "wall_time_seconds": wall_time,
        "cpu_time_seconds": cpu_time,
        "cpu_time_per_operation": cpu_time / iterations,
        "cpu_utilisation": (cpu_time / wall_time) * 100,
    }

# Memory benchmark
def memory_benchmark(operation, minimum_duration=1.0, minimum_iterations=100, warmup=10, sample_interval=0.001):

    warm_up(operation,warmup)

    process = psutil.Process(os.getpid())

    memory_before = process.memory_info().rss

    peak_memory = {"value": memory_before}

    stop_event = threading.Event()

    def sample_memory():
        while not stop_event.is_set():
            current_memory = (process.memory_info().rss)

            if current_memory > peak_memory["value"]:
                peak_memory["value"] = (current_memory)

            time.sleep(sample_interval)

    memory_thread = threading.Thread(target=sample_memory, daemon=True)

    memory_thread.start()

    wall_start = time.perf_counter()
    iterations = 0

    while True:
        operation()

        iterations += 1

        if iterations >= minimum_iterations:
            elapsed = (time.perf_counter() - wall_start)

            if elapsed >= minimum_duration:
                break

    stop_event.set()

    memory_thread.join()

    memory_after = process.memory_info().rss

    peak =  max(peak_memory["value"], memory_after)

    peak_increase = max(0, peak - memory_before)

    return {
        "iterations":
            iterations,

        "memory_before_mb":
            memory_before / (1024 ** 2),

        "memory_after_mb":
            memory_after / (1024 ** 2),

        "peak_memory_mb":
            peak / (1024 ** 2),

        "peak_memory_increase_mb":
            peak_increase / (1024 ** 2),

        "peak_memory_increase_kb":
            peak_increase / 1024
    }
