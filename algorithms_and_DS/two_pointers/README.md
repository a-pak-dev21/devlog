# Two Pointers

## Overview
The **Two Pointers** technique uses two indices moving over a sequence to reduce nested loops into a single pass.  
It is one of the most common patterns in coding interviews and appears in problems involving arrays, strings, and linked lists.

Typical pointer movements:
- **Opposite directions** (from both ends towards the middle).
- **Same direction** (fast/slow pointers, or "write"/"read" pointers).

---

## When to Use
- Searching in **sorted arrays** (sum of two numbers, merging).
- Checking **mirror symmetry** (palindromes).
- Filtering/compacting arrays in place (move zeroes, remove duplicates).
- Linked list problems (cycle detection, middle node).

---

## Core Invariants
- **Sum problems**: If sum < target → move left; if sum > target → move right.
- **Palindrome check**: Compare characters, skipping non-alphanumeric.
- **Array compaction**: Maintain `insert_pos` for the next valid element.

---

## Complexity
- Time: usually **O(n)** (single pass with two moving pointers).
- Space: often **O(1)** (in-place operations).

---

## Common Pitfalls
- Using `list.index()`, `pop()`, or slicing inside the loop (leads to O(n²)).
- Forgetting Unicode normalization when lowercasing (prefer `.casefold()`).
- For merging, using `zip()` and losing the “tails” of arrays.

---

## Template Examples

**1. Pair Sum in Sorted Array**
```python
l, r = 0, len(arr) - 1
while l < r:
    s = arr[l] + arr[r]
    if s == target:
        return (l, r)
    elif s < target:
        l += 1
    else:
        r -= 1