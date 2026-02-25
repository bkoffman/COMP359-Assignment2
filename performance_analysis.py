"""
Performance Analysis: Two-Circle Josephus
==========================================
Compares deque-based vs list-based implementations and benchmarks
the simulation for various group sizes.
"""

import time
import statistics
from collections import deque


# ========== DEQUE IMPLEMENTATION (Original) ==========

def josephus_eliminate_deque(circle: deque, k: int = 2) -> int:
    """Eliminate using deque rotation — O(k) per elimination."""
    circle.rotate(-(k - 1))
    return circle.popleft()


def two_circle_josephus_deque(n: int, k: int = 2) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        return 1

    mid = (n + 1) // 2
    circle_a = deque(range(1, mid + 1))
    circle_b = deque(range(mid + 1, n + 1))

    if len(circle_b) == 0:
        return circle_a[0]

    while len(circle_a) > 1 or len(circle_b) > 1:
        if len(circle_a) >= len(circle_b):
            if len(circle_a) > 1:
                josephus_eliminate_deque(circle_a, k)
            if len(circle_b) > 1:
                josephus_eliminate_deque(circle_b, k)
        else:
            if len(circle_b) > 1:
                josephus_eliminate_deque(circle_b, k)
            if len(circle_a) > 1:
                josephus_eliminate_deque(circle_a, k)

    final = deque([circle_a[0], circle_b[0]])
    josephus_eliminate_deque(final, k)
    return final[0]


# ========== LIST IMPLEMENTATION (For comparison) ==========

def josephus_eliminate_list(circle: list, ptr: int, k: int = 2):
    """Eliminate using list indexing + pop — O(n) per elimination due to shift."""
    idx = (ptr + k - 1) % len(circle)
    eliminated = circle.pop(idx)
    if len(circle) == 0:
        return eliminated, 0
    new_ptr = idx % len(circle)
    return eliminated, new_ptr


def two_circle_josephus_list(n: int, k: int = 2) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        return 1

    mid = (n + 1) // 2
    circle_a = list(range(1, mid + 1))
    circle_b = list(range(mid + 1, n + 1))
    ptr_a, ptr_b = 0, 0

    if len(circle_b) == 0:
        return circle_a[0]

    while len(circle_a) > 1 or len(circle_b) > 1:
        if len(circle_a) >= len(circle_b):
            if len(circle_a) > 1:
                _, ptr_a = josephus_eliminate_list(circle_a, ptr_a, k)
            if len(circle_b) > 1:
                _, ptr_b = josephus_eliminate_list(circle_b, ptr_b, k)
        else:
            if len(circle_b) > 1:
                _, ptr_b = josephus_eliminate_list(circle_b, ptr_b, k)
            if len(circle_a) > 1:
                _, ptr_a = josephus_eliminate_list(circle_a, ptr_a, k)

    final = [circle_a[0], circle_b[0]]
    ptr = 0
    _, ptr = josephus_eliminate_list(final, ptr, k)
    return final[0]


# ========== BENCHMARKING ==========

def benchmark(func, n, k=2, trials=5):
    """Run func(n, k) multiple times and return timing stats."""
    times = []
    for _ in range(trials):
        start = time.perf_counter()
        func(n, k)
        end = time.perf_counter()
        times.append(end - start)
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
    }


def verify_correctness():
    """Verify both implementations produce the same results."""
    print("Verifying correctness (deque vs list)...")
    all_match = True
    for n in range(1, 101):
        for k in [2, 3, 5, 7]:
            d = two_circle_josephus_deque(n, k)
            l = two_circle_josephus_list(n, k)
            if d != l:
                print(f"  MISMATCH: n={n}, k={k}: deque={d}, list={l}")
                all_match = False
    if all_match:
        print("Both implementations produce identical results for n=1..100, k=2,3,5,7\n")
    return all_match


def run_benchmarks():
    """Run benchmarks across various group sizes."""
    test_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000]
    k = 2
    trials = 5

    print(f"{'n':>8} | {'Deque (ms)':>12} | {'List (ms)':>12} | {'Speedup':>10} | {'Winner':>8}")
    print("-" * 62)

    results = []

    for n in test_sizes:
        """Adjust trials for large n"""
        t = trials if n <= 10000 else 3

        deque_stats = benchmark(two_circle_josephus_deque, n, k, t)
        list_stats = benchmark(two_circle_josephus_list, n, k, t)

        deque_ms = deque_stats['mean'] * 1000
        list_ms = list_stats['mean'] * 1000
        speedup = list_ms / deque_ms if deque_ms > 0 else float('inf')
        winner = "Deque" if deque_ms < list_ms else "List"

        print(f"{n:>8} | {deque_ms:>11.3f} | {list_ms:>11.3f} | {speedup:>9.2f}x | {winner:>8}")

        results.append({
            'n': n, 'deque_ms': deque_ms, 'list_ms': list_ms,
            'speedup': speedup, 'winner': winner
        })

    return results


def run_k_impact_benchmark():
    """Benchmark how different k values affect performance."""
    print(f"\n{'k':>4} | {'n=1000 Deque (ms)':>18} | {'n=1000 List (ms)':>18} | {'Speedup':>10}")
    print("-" * 58)

    for k in [2, 3, 5, 10, 50, 100]:
        deque_stats = benchmark(two_circle_josephus_deque, 1000, k, 5)
        list_stats = benchmark(two_circle_josephus_list, 1000, k, 5)

        deque_ms = deque_stats['mean'] * 1000
        list_ms = list_stats['mean'] * 1000
        speedup = list_ms / deque_ms if deque_ms > 0 else float('inf')

        print(f"{k:>4} | {deque_ms:>17.3f} | {list_ms:>17.3f} | {speedup:>9.2f}x")


def print_complexity_analysis():
    """Print theoretical complexity comparison."""
    print("\n" + "=" * 60)
    print("TIME COMPLEXITY ANALYSIS")
    print("=" * 60)

    print("""
DEQUE-BASED IMPLEMENTATION:
  - Each elimination: O(k) for rotation + O(1) for popleft
  - Total eliminations per circle: ~n/2
  - Total time: O(n * k)
  - For k=2 (constant): O(n)
  - Space: O(n)

LIST-BASED IMPLEMENTATION:
  - Each elimination: O(1) for indexing + O(n) for list.pop (shifts elements)
  - Total eliminations per circle: ~n/2
  - Total time: O(n²)
  - Space: O(n)

COMPARISON:
  - For small n (< 100): Both are fast, difference is negligible
  - For medium n (100 - 1000): Deque starts to show advantage
  - For large n (> 1000): Deque is significantly faster
  - For very large n (> 10000): List becomes impractical, deque scales linearly

  The key difference is that list.pop(i) requires shifting all elements
  after index i, making it O(n) per operation. Deque.rotate() + popleft()
  avoids this shift entirely.

WHY DEQUE IS THE RIGHT CHOICE:
  1. O(1) popleft vs O(n) list.pop(0)
  2. rotate() perfectly models circular counting
  3. No manual pointer/index management needed
  4. Clean, readable code that maps directly to the problem
""")


if __name__ == "__main__":
    print("PERFORMANCE ANALYSIS: TWO-CIRCLE JOSEPHUS")
    print("=" * 62)
    print()

    # Step 1: Verify correctness
    verify_correctness()

    # Step 2: Benchmark deque vs list
    print("--- Benchmark: Deque vs List (k=2) ---")
    results = run_benchmarks()

    # Step 3: Impact of k
    print("\n--- Benchmark: Impact of k Value (n=1000) ---")
    run_k_impact_benchmark()

    # Step 4: Complexity analysis
    print_complexity_analysis()
