from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    if Counter(s) == Counter(t):
        return True
    else:
        return False
