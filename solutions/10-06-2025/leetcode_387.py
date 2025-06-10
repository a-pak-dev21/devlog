from collections import Counter


def first_uniq_char(s: str) -> int:
    s_counter = Counter(s)
    if s_counter.most_common()[-1][1] > 1:
        return -1
    else:
        for index, c in enumerate(s):
            if s_counter[c] == 1:
                return index
