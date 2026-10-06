import csv
import statistics
import timeit
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =======================================================
# DO NOT MODIFY THE ALGORITHM IMPLEMENTATIONS
# =======================================================

def find_duplicates_slow(data):
    """An O(n^2) algorithm to find duplicates."""
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            if data[i] == data[j]:
                return True
    return False

def find_duplicates_fast(data):
    """An O(n) algorithm to find duplicates."""
    seen = set()
    for item in data:
        if item in seen:
            return True
        seen.add(item)
    return False


# =======================================================
# YOUR TASK: FIX THE BENCHMARKING SCRIPT BELOW
# =======================================================

def flawed_benchmark():
    sizes = [250, 500, 1000, 2000, 4000]
    slow_times = []
    fast_times = []

    for n in sizes:
        # No duplicates, so neither algorithm can return early.
        data = list(range(n))
        find_duplicates_slow(data)
        find_duplicates_fast(data)

        slow_samples = []
        fast_samples = []
        for trial in range(7):
            # Switch the order each trial so one does not always go first.
            algorithms = [find_duplicates_slow, find_duplicates_fast]
            if trial % 2 == 1:
                algorithms.reverse()

            for algorithm in algorithms:
                # The fast version needs more calls to get a useful timing.
                calls = 5 if algorithm == find_duplicates_slow else 1000
                elapsed = timeit.timeit(lambda: algorithm(data), number=calls)
                seconds = elapsed / calls
                if algorithm == find_duplicates_slow:
                    slow_samples.append(seconds)
                else:
                    fast_samples.append(seconds)

        slow_times.append(statistics.median(slow_samples))
        fast_times.append(statistics.median(fast_samples))
        print(f"n={n}: slow={slow_times[-1]:.8f}s, fast={fast_times[-1]:.8f}s")

    output_dir = Path(__file__).resolve().parent
    with (output_dir / "results.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["n", "slow_seconds", "fast_seconds"])
        writer.writerows(zip(sizes, slow_times, fast_times))

    # Log scales make both lines easy to see despite the large time gap.
    plt.figure(figsize=(8, 5))
    plt.loglog(sizes, slow_times, "o-", label="Slow: O(n²)")
    plt.loglog(sizes, fast_times, "o-", label="Fast: expected O(n)")
    plt.xlabel("Number of elements (log scale)")
    plt.ylabel("Median time per call in seconds (log scale)")
    plt.title("Finding duplicates")
    plt.xticks(sizes, sizes)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "results.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    flawed_benchmark()
