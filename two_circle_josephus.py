"""
Two-Circle Josephus Problem Variation
======================================
A variation where participants are split into two circles.
Each circle eliminates one person per round (larger circle goes first).
When one person remains per circle, a final Josephus round determines the winner.

Step size k = 2 throughout.
"""

from collections import deque


def _snapshot(circle_a: deque, circle_b: deque, turn: str, eliminated: int, phase: str = "main"):
    """
    Create a trace snapshot AFTER an elimination.

    Conventions:
    - 'A' and 'B' store the current deque order for each circle.
    - The "pointer" is implicitly the FRONT of each deque (index 0 in the list).
    - 'turn' indicates which circle performed the elimination ("A" or "B").
    - 'phase' is "main" during alternating eliminations, and "final" for the head-to-head.
    """
    return {
        "turn": turn,              # A or B
        "eliminated": eliminated,  # eliminated person ID
        "A": list(circle_a),       # Circle A state (pointer at index 0)
        "B": list(circle_b),       # Circle B state (pointer at index 0)
        "phase": phase,            # main or final
    }


def josephus_eliminate(circle: deque, k: int = 2) -> int:
    """
    Eliminate one person from a circle using the Josephus rule.
    Rotates the deque k-1 times, then removes the front person.

    Args:
        circle: deque representing the circle of people
        k: step size (every k-th person is eliminated)

    Returns:
        The number of the eliminated person
    """
    circle.rotate(-(k - 1))
    eliminated = circle.popleft()
    return eliminated


def two_circle_josephus(n: int, k: int = 2, verbose: bool = False, trace: bool = False):
    """
    Simulate the two-circle Josephus variation.

    Args:
        n: total number of people (numbered 1 to n)
        k: step size for elimination (default 2)
        verbose: if True, print step-by-step eliminations
        trace: if True, return (winner, steps) where steps is a list of snapshots

    Returns:
        If trace=False: the number of the winning person (int)
        If trace=True:  (winner, steps)
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    # Trace list (only used if trace=True)
    steps = [] if trace else None

    if n == 1:
        if verbose:
            print(f"n={n}: Only one person. Winner: 1")
        return (1, steps) if trace else 1

    # Split into two circles
    mid = (n + 1) // 2  # ceil(n/2) — Circle A gets extra if odd
    circle_a = deque(range(1, mid + 1))
    circle_b = deque(range(mid + 1, n + 1))

    if verbose:
        print(f"\nn={n}, k={k}")
        print(f"  Circle A ({len(circle_a)}): {list(circle_a)}")
        print(f"  Circle B ({len(circle_b)}): {list(circle_b)}")

    # If circle_b is empty (only possible when n=1, already handled), just return circle_a[0]
    if len(circle_b) == 0:
        return (circle_a[0], steps) if trace else circle_a[0]

    # Elimination phase: alternate eliminating from each circle
    round_num = 1
    while len(circle_a) > 1 or len(circle_b) > 1:
        if verbose:
            print(f"  Round {round_num}:", end="")

        # Determine order: larger circle goes first (Circle A goes first on tie)
        if len(circle_a) >= len(circle_b):
            # Circle A goes first
            if len(circle_a) > 1:
                eliminated_a = josephus_eliminate(circle_a, k)
                if trace:
                    steps.append(_snapshot(circle_a, circle_b, turn="A", eliminated=eliminated_a, phase="main"))
                if verbose:
                    print(f" Circle A eliminates {eliminated_a} → {list(circle_a)}", end="")
            elif verbose:
                print(f" Circle A has 1 left ({circle_a[0]}), skips", end="")

            # Then Circle B
            if len(circle_b) > 1:
                eliminated_b = josephus_eliminate(circle_b, k)
                if trace:
                    steps.append(_snapshot(circle_a, circle_b, turn="B", eliminated=eliminated_b, phase="main"))
                if verbose:
                    print(f" | Circle B eliminates {eliminated_b} → {list(circle_b)}", end="")
            elif verbose:
                print(f" | Circle B has 1 left ({circle_b[0]}), skips", end="")
        else:
            # Circle B goes first (strictly larger)
            if len(circle_b) > 1:
                eliminated_b = josephus_eliminate(circle_b, k)
                if trace:
                    steps.append(_snapshot(circle_a, circle_b, turn="B", eliminated=eliminated_b, phase="main"))
                if verbose:
                    print(f" Circle B eliminates {eliminated_b} → {list(circle_b)}", end="")
            elif verbose:
                print(f" Circle B has 1 left ({circle_b[0]}), skips", end="")

            # Then Circle A
            if len(circle_a) > 1:
                eliminated_a = josephus_eliminate(circle_a, k)
                if trace:
                    steps.append(_snapshot(circle_a, circle_b, turn="A", eliminated=eliminated_a, phase="main"))
                if verbose:
                    print(f" | Circle A eliminates {eliminated_a} → {list(circle_a)}", end="")
            elif verbose:
                print(f" | Circle A has 1 left ({circle_a[0]}), skips", end="")

        if verbose:
            print()
        round_num += 1

    # Final round: one person in each circle
    survivor_a = circle_a[0]
    survivor_b = circle_b[0]

    if verbose:
        print(f"  Final round: Circle A survivor = {survivor_a}, Circle B survivor = {survivor_b}")
        print(f"  Mini-circle: [{survivor_a}, {survivor_b}] (Circle A person first)")

    final_circle = deque([survivor_a, survivor_b])
    eliminated_final = josephus_eliminate(final_circle, k)
    winner = final_circle[0]

    if trace:
        # Represent final as a last step. We keep the winner in A for simplicity.
        steps.append({
            "turn": "A", # Circle A considered first in the mini-circle
            "eliminated": eliminated_final,
            "A": [winner],
            "B": [],
            "phase": "final",
        })

    if verbose:
        print(f"  Eliminates {eliminated_final} → Winner: {winner}")

    return (winner, steps) if trace else winner


def original_josephus(n: int, k: int = 2) -> int:
    """
    Solve the original Josephus problem using the iterative formula.
    Returns the 1-indexed position of the survivor.

    J(1, k) = 0
    J(n, k) = (J(n-1, k) + k) % n
    Then convert from 0-indexed to 1-indexed.
    """
    pos = 0
    for i in range(2, n + 1):
        pos = (pos + k) % i
    return pos + 1


def print_results_table(max_n: int = 30):
    """
    Print a comparison table of the two-circle variant vs. the original
    Josephus problem for group sizes 1 to max_n.
    """
    print(f"{'n':>4} | {'Two-Circle Winner':>18} | {'Original Josephus':>18}")
    print("-" * 47)
    for n in range(1, max_n + 1):
        tc_winner = two_circle_josephus(n)
        orig_winner = original_josephus(n)
        print(f"{n:>4} | {tc_winner:>18} | {orig_winner:>18}")


def analyze_pattern(max_n: int = 30):
    """
    Analyze the pattern of winners in the two-circle variant
    and compare with the original Josephus problem.
    """
    print("\n" + "=" * 60)
    print("PATTERN ANALYSIS")
    print("=" * 60)

    two_circle_winners = []
    original_winners = []

    for n in range(1, max_n + 1):
        two_circle_winners.append(two_circle_josephus(n))
        original_winners.append(original_josephus(n))

    # Check how often the two-circle winner matches the original
    matches = sum(1 for i in range(max_n)
                  if two_circle_winners[i] == original_winners[i])
    print(f"\nMatches with original Josephus: {matches}/{max_n}")

    # Check if two-circle winner is always from Circle A
    always_a = True
    for n in range(1, max_n + 1):
        mid = (n + 1) // 2
        winner = two_circle_winners[n - 1]
        if winner > mid:
            always_a = False
            print(f"  n={n}: winner={winner} is from Circle B (Circle A = 1..{mid})")

    if always_a:
        print("\nObservation: The winner is ALWAYS from Circle A (the first circle).")
        print("This is expected because in the final round, Circle A's survivor")
        print("goes first with k=2 and 2 people, which always favors the first person.")

    # Look for power-of-2 patterns (like original Josephus)
    print("\n--- Two-Circle Winners by n ---")
    for n in range(1, max_n + 1):
        mid = (n + 1) // 2
        winner = two_circle_winners[n - 1]
        # The winner's position within Circle A
        print(f"  n={n:>2}, CircleA size={mid:>2}, Winner={winner:>2} (position {winner} in Circle A)")

    # Original Josephus pattern reminder
    print("\n--- Original Josephus Pattern (for reference) ---")
    print("For k=2, the classic formula is:")
    print("  J(n) = 2*L + 1, where n = 2^m + L and 0 <= L < 2^m")
    print("  (i.e., write n in binary, rotate left by 1 bit)")

    # Conjecture
    print("\n--- Conjecture ---")
    print("The two-circle variant effectively runs two independent Josephus")
    print("sub-problems on Circle A (size ceil(n/2)) and Circle B (size floor(n/2)).")
    print("Since the final round with k=2 always favors Circle A's survivor,")
    print("the overall winner equals the Josephus survivor of Circle A alone.")
    print()
    print("Testing this conjecture:")

    conjecture_holds = True
    for n in range(1, max_n + 1):
        mid = (n + 1) // 2
        tc_winner = two_circle_winners[n - 1]
        expected = original_josephus(mid)  # position in circle of size mid

        if tc_winner != expected:
            conjecture_holds = False
            print(f"  MISMATCH at n={n}: two-circle={tc_winner}, J(CircleA size={mid})={expected}")

    if conjecture_holds:
        print("  Conjecture HOLDS for all n from 1 to", max_n)
        print()
        print("FINAL CONJECTURE:")
        print("  For the two-circle variant with k=2:")
        print("  Winner(n) = J(ceil(n/2), 2)")
        print("  where J(m, 2) = 2*L + 1, m = 2^p + L and 0 <= L < 2^p")
    else:
        print("  Conjecture does NOT hold perfectly. See mismatches above.")


def analyze_odd_vs_even_k(max_n: int = 30, max_k: int = 10):
    """
    Analyze whether the winning circle depends on k being odd or even.
    """
    print("\n" + "=" * 60)
    print("ODD vs EVEN k ANALYSIS")
    print("=" * 60)
    print(f"\nTesting k=2 to k={max_k} for group sizes n=2 to {max_n}:")
    print()

    for k in range(2, max_k + 1):
        a_wins = 0
        b_wins = 0
        for n in range(2, max_n + 1):
            mid = (n + 1) // 2
            winner = two_circle_josephus(n, k=k)
            if winner <= mid:
                a_wins += 1
            else:
                b_wins += 1

        total = max_n - 1
        k_type = "even" if k % 2 == 0 else "odd"
        winning_circle = "Circle A" if a_wins > b_wins else "Circle B"
        print(f"  k={k:>2} ({k_type:>4}): Circle A wins {a_wins:>2}/{total} | "
              f"Circle B wins {b_wins:>2}/{total} → {winning_circle} always wins")

    print()
    print("CONCLUSION:")
    print("  Even k → Circle A (first circle) ALWAYS wins the final round")
    print("  Odd  k → Circle B (second circle) ALWAYS wins the final round")
    print()
    print("WHY? In the final head-to-head (2 people, Circle A goes first):")
    print("  - Even k: counting k from person 1 lands on person 2 → eliminate person 2 → Circle A wins")
    print("  - Odd  k: counting k from person 1 lands on person 1 → eliminate person 1 → Circle B wins")


if __name__ == "__main__":
    print("TWO-CIRCLE JOSEPHUS PROBLEM VARIATION")
    print("=" * 60)

    # Step-by-step trace for select examples
    print("\n--- Step-by-Step Trace (select examples) ---")
    for n in [5, 6, 7, 8, 10]:
        two_circle_josephus(n, verbose=True)

    # Full results table
    print("\n\n--- Results Table (n=1 to 30) ---")
    print_results_table(30)
    analyze_pattern(30)

    # Odd vs Even k analysis
    analyze_odd_vs_even_k(30, 10)