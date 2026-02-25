# Two-Circle Josephus Problem — Rules Specification

## Overview

This is a variation of the classic Josephus problem where participants are divided into **two separate circles** instead of one. Each circle independently eliminates members, and when one person remains in each circle, a final Josephus round determines the winner.

## Rules

### 1. Setup — Circle Division
- Given `n` people numbered `1` to `n`, divide them into two circles:
  - **Circle A**: persons `1` to `ceil(n/2)` — gets the extra person if `n` is odd.
  - **Circle B**: persons `ceil(n/2)+1` to `n`.
- People retain their original numbering throughout the game.

### 2. Elimination Phase — Alternating Turns
- Each round, **one person is eliminated from each circle** (one per circle per round).
- The **larger circle goes first** in each round.
  - If Circle A has more people, Circle A eliminates first, then Circle B.
  - If Circle B has more people, Circle B eliminates first, then Circle A.
  - If both circles are the same size, Circle A goes first (as the "first" circle).
- Within each circle, elimination follows the **standard Josephus rule**: every **k-th person** is eliminated (default `k = 2`), counting from the current position.
- The counting position in each circle carries over between rounds (i.e., after someone is eliminated, the next count starts from the person after the eliminated one).
- If a circle already has only 1 person remaining, it **skips** its turn that round.

### 3. Final Round — Head-to-Head
- When exactly **one person remains in each circle**, the two survivors play a final **standard Josephus round** between them.
- The two remaining people are arranged in a mini-circle.
- The person from **Circle A** (the first circle) is considered **first** (counted from first).
- With `k = 2`: the second person is eliminated, so the Circle A survivor wins.

### 4. Parameters
- **n**: Total number of people (1 to 30 for the results table).
- **k**: Step size / elimination interval (default `k = 2`, every 2nd person eliminated).

## Data Structures
- **`collections.deque`** is used to represent each circle. The deque supports efficient rotation to simulate circular counting and elimination.

## Algorithm Summary
1. Build Circle A and Circle B as deques.
2. Each round:
   - Determine which circle is larger (goes first).
   - Eliminate one person from the first circle (rotate `k-1` times, then `popleft`).
   - Eliminate one person from the second circle (same method).
   - If a circle has only 1 person left, skip its elimination.
   - Continue until each circle has exactly one person.
3. Play a final Josephus round between the two survivors, with Circle A's survivor going first.
4. Return the winner's original number.

## Edge Cases
- **n = 1**: Only one person exists. Circle A = [1], Circle B = []. Person 1 wins by default.
- **n = 2**: Circle A = [1], Circle B = [2]. Final round immediately: Person 1 wins (for even k).
- **Odd n**: Circle A gets one extra person (e.g., n=5 → A=[1,2,3], B=[4,5]).

## Output

### Step-by-Step Trace
The program outputs a detailed trace for select group sizes, showing the initial circle split, every round's elimination from both circles, and the final head-to-head result.

Example for n=6, k=2:
```
n=6, k=2
  Circle A (3): [1, 2, 3]
  Circle B (3): [4, 5, 6]
  Round 1: Circle A eliminates 2 → [3, 1] | Circle B eliminates 5 → [6, 4]
  Round 2: Circle A eliminates 1 → [3]    | Circle B eliminates 4 → [6]
  Final round: Circle A survivor = 3, Circle B survivor = 6
  Mini-circle: [3, 6] (Circle A person first)
  Eliminates 6 → Winner: 3
```

### Results Table (k=2, n=1 to 30)

| n | Two-Circle Winner | Original Josephus |
|---|-------------------|-------------------|
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 3 | 1 | 3 |
| 4 | 1 | 1 |
| 5 | 3 | 3 |
| 6 | 3 | 5 |
| 7 | 1 | 7 |
| 8 | 1 | 1 |
| 9 | 3 | 3 |
| 10 | 3 | 5 |
| 11 | 5 | 7 |
| 12 | 5 | 9 |
| 13 | 7 | 11 |
| 14 | 7 | 13 |
| 15 | 1 | 15 |
| 16 | 1 | 1 |
| 17 | 3 | 3 |
| 18 | 3 | 5 |
| 19 | 5 | 7 |
| 20 | 5 | 9 |
| 21 | 7 | 11 |
| 22 | 7 | 13 |
| 23 | 9 | 15 |
| 24 | 9 | 17 |
| 25 | 11 | 19 |
| 26 | 11 | 21 |
| 27 | 13 | 23 |
| 28 | 13 | 25 |
| 29 | 15 | 27 |
| 30 | 15 | 29 |

## Pattern Analysis & Conjectures

### Conjecture 1: Winner Reduces to Classic Josephus on Circle A

The two-circle variant winner is determined entirely by Circle A's internal Josephus problem:

```
Winner(n) = J(⌈n/2⌉, 2)
```

Where `J(m, 2) = 2L + 1` with `m = 2^p + L` and `0 ≤ L < 2^p` (the classic Josephus formula).

In plain terms:
- Circle B's elimination process is irrelevant to the final outcome — its survivor always loses the final round (when k is even).
- The winner is whoever would survive the classic Josephus problem played only within Circle A.
- Within Circle A, the winner follows the power-of-2 pattern: every time Circle A's size hits a power of 2 (1, 2, 4, 8, 16...), the winner resets to person 1. Between powers of 2, the winner increases by 2 each step (1, 3, 5, 7, 9...).

This conjecture was verified for all n from 1 to 30.

### Conjecture 2: Odd vs Even k Determines Winning Circle

The winning circle is entirely determined by whether k is odd or even:

| k parity | Winning Circle | Win Rate (tested k=2 to 10, n=2 to 30) |
|----------|---------------|----------------------------------------|
| Even k   | Circle A (first circle) | 100% |
| Odd k    | Circle B (second circle) | 100% |

**Why?** It all comes down to the final head-to-head round between 2 people, where Circle A's survivor is placed first:
- **Even k**: Counting k positions from person 1 in a 2-person circle lands on person 2. Person 2 is eliminated → Circle A wins.
- **Odd k**: Counting k positions from person 1 in a 2-person circle lands on person 1. Person 1 is eliminated → Circle B wins.

The elimination rounds leading up to the final don't affect which circle wins — only k's parity matters. This means:
- For even k: `Winner(n) = J(⌈n/2⌉, k)` — the Josephus survivor of Circle A.
- For odd k: `Winner(n) = ⌈n/2⌉ + J(⌊n/2⌋, k)` — the Josephus survivor of Circle B (offset by Circle A's size to get the original person number).

### Relationship to Original Josephus Problem

The two-circle variant does **not** follow the Fibonacci sequence. The pattern is governed by **powers of 2** and binary representations, consistent with the original Josephus problem's mathematical structure. The key difference is that the two-circle variant applies the Josephus formula to half the group (Circle A's size) rather than the full group.

## How to Run

```bash
python two_circle_josephus.py
```

This will output:
1. Step-by-step traces for select group sizes (n=5, 6, 7, 8, 10)
2. Full results table for n=1 to 30
3. Pattern analysis with conjecture verification
4. Odd vs even k analysis for k=2 to 10

To run a single simulation with verbose output:
```python
from two_circle_josephus import two_circle_josephus
winner = two_circle_josephus(n=10, k=2, verbose=True)
```

# Visualization

## Interactive Visualization of the Two-Circle Josephus Variant

An interactive visualization was implemented using **Matplotlib** to illustrate the execution of the two-circle Josephus variation. The visualization renders a deterministic execution trace produced by the simulation (`trace=True`) and does not recompute elimination logic independently. This guarantees consistency between the numerical results and the visual output.

The visualization displays two distinct circular structures:

- **Circle A** (left) — participants 1 through ⌈n/2⌉  
- **Circle B** (right) — participants ⌈n/2⌉+1 through n  

At each elimination step, the interface presents:

- The current **pointer position** in each circle (front of the deque, index 0)
- The **active circle** performing the elimination
- The **eliminated participant**
- The current **simulation phase** (`main` alternating elimination or `final` head-to-head)
- The current **step index** within the execution trace

Because the visualization consumes a precomputed trace, it functions as a replay mechanism rather than a second implementation of the algorithm. This design enforces correctness and reproducibility.

---

## Interaction Controls

The visualization provides on-screen controls:

- **Prev** — move one step backward in the elimination sequence  
- **Next** — advance one step forward  
- **Reset** — return to the initial state  

This allows stepwise inspection of the elimination dynamics, pointer progression, and alternating-circle logic.

---

## How to Run the Visualization

### Install Required Dependency
The visualization requires Matplotlib:

```bash
pip install matplotlib
```
## Execute the Visualization
From the project directory:
```bash
python visualize_two_circle.py
```
To run the visualization for a specific group size n:
```bash
python visualize_two_circle.py 12
```

This will:
- Run the two-circle Josephus simulation with tracing enabled
- Print the winner in the terminal
- Launch an interactive window displaying the elimination sequence

## Implementation Notes

-Each circle is represented using collections.deque to efficiently model circular behavior.
-The front of the deque (index 0) represents the current counting position.
-Eliminations are performed by rotating the deque k − 1 positions and removing the front element.
-After every elimination, a structured snapshot of both circles is recorded.
-The visualization sequentially renders these snapshots to reproduce the algorithm’s execution deterministically.