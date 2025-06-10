from collections import Counter


def frequency_sort(s: str) -> str:
    s_counter = Counter(s)
    sorted_s = sorted(s_counter.items(), key=lambda x: x[1], reverse=True)
    return "".join(key * val for key, val in sorted_s)
