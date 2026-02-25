# Two-Circle Josephus Problem

A variation of the classic Josephus problem where participants are split into two circles that take turns eliminating members.

## Project Structure

```
├── README.md                  # Rules, results, and analysis
├── two_circle_josephus.py     # Core simulation, trace, and pattern analysis
├── visualize_two_circle.py    # Matplotlib GUI for step-by-step playback
└── performance_analysis.py    # Deque vs list benchmarks
```

## How to Run

```bash
python two_circle_josephus.py           # simulation + results table + analysis
python visualize_two_circle.py          # GUI (default n=10)
python visualize_two_circle.py 15       # GUI with custom n
python performance_analysis.py          # benchmarks
```

## Rules

1. **Split** `n` people into two circles — Circle A gets `⌈n/2⌉`, Circle B gets the rest.
2. **Each round**, eliminate one person from each circle using the Josephus rule (every k-th person, default k=2). The larger circle goes first. If tied, Circle A goes first.
3. If a circle has one person left, it **skips** that round.
4. **Final round**: when both circles have one survivor, they play a head-to-head Josephus round. Circle A's survivor is placed first.

## Algorithm

Each circle is represented as a `collections.deque`. To eliminate someone, rotate `k-1` times and `popleft()`. This naturally handles the circular counting without needing manual index tracking.

## Results (k=2, n=1 to 30)

| n | Winner | n | Winner | n | Winner |
|---|:-:|---|:-:|---|:-:|
| 1 | 1 | 11 | 5 | 21 | 7 |
| 2 | 1 | 12 | 5 | 22 | 7 |
| 3 | 1 | 13 | 7 | 23 | 9 |
| 4 | 1 | 14 | 7 | 24 | 9 |
| 5 | 3 | 15 | 1 | 25 | 11 |
| 6 | 3 | 16 | 1 | 26 | 11 |
| 7 | 1 | 17 | 3 | 27 | 13 |
| 8 | 1 | 18 | 3 | 28 | 13 |
| 9 | 3 | 19 | 5 | 29 | 15 |
| 10 | 3 | 20 | 5 | 30 | 15 |

## Conjectures

**1. The winner depends only on Circle A.**
Circle B's survivor always loses the final round (when k is even), so the overall winner is just the Josephus survivor of Circle A: `Winner(n) = J(⌈n/2⌉, 2)`. The winner resets to 1 at every power of 2, then climbs by 2 (1, 3, 5, 7...) until the next reset. Verified for n=1 to 30.

**2. Odd vs even k determines which circle wins.**
Even k → Circle A always wins. Odd k → Circle B always wins. Tested for k=2 through 10 across all group sizes. The reason is simple: in the final 2-person round, even k eliminates the second person and odd k eliminates the first.

## Performance Analysis

We implemented both a deque and list version and benchmarked them:

| n | Deque (ms) | List (ms) | Speedup |
|---|:-:|:-:|:-:|
| 100 | 0.014 | 0.017 | 1.2x |
| 1,000 | 0.113 | 0.195 | 1.7x |
| 10,000 | 1.170 | 3.972 | 3.4x |
| 50,000 | 7.125 | 84.439 | **11.9x** |

Deque is O(n) for k=2 while list is O(n²) because `list.pop(i)` shifts elements. The gap grows fast — at n=50,000 deque is nearly 12x faster.

## Bibliography

1. **GeeksforGeeks — "The Josephus Problem"**
   [https://www.youtube.com/watch?v=fZ3p2Iw-O2I&t=268s](https://www.youtube.com/watch?v=fZ3p2Iw-O2I&t=268s)
   Helped with understanding the original Josephus problem and the power-of-2 pattern.

2. **Claude (Anthropic)** — Used as a coding assistant during development.
