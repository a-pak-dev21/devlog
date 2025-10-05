# Sliding Window

## Overview
The **Sliding Window** technique maintains a "window" (a subarray or substring) defined by two pointers `left` and `right`.  
The window is expanded and shrunk dynamically to satisfy certain conditions, making it ideal for subarray/substring problems.

Two main types:
- **Fixed-size window**: The window has a constant length `k`.
- **Variable-size window**: The window grows and shrinks depending on problem constraints.

---

## When to Use
- Find **longest/shortest subarray** satisfying a condition.
- Count substrings with constraints (e.g., unique characters).
- Handle **sums, frequencies, distinct characters** in a substring.
- Optimize problems where a naive nested loop would be O(n²).

---

## Core Invariants
- **No duplicates allowed**: shrink window while duplicate exists.
- **Sum ≥ target**: shrink from left while sum still valid.
- **Replace up to k characters**: maintain `len(window) - max_freq ≤ k`.

---

## Complexity
- Time: typically **O(n)** — each element enters and leaves the window at most once.
- Space: **O(k)** for frequency maps/sets (where `k` is alphabet size).

---

## Common Pitfalls
- Recomputing expensive functions inside the loop (e.g. `sum(nums[left:right])`, `set(...)`) → leads to O(n²).
- Assuming only 2 characters in #424 (there can be more).
- Forgetting to update or track `max_freq` correctly (can keep as "observed max").

---

## Template Examples

**1. Longest Substring Without Repeating Characters**
```python
left = 0
seen = set()
best = 0
for right, ch in enumerate(s):
    while ch in seen:
        seen.remove(s[left])
        left += 1
    seen.add(ch)
    best = max(best, right - left + 1)
return best