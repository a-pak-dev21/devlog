def is_valid(s: str) -> bool:
    poss_var = {
        "(": ")",
        "{": "}",
        "[": "]"
    }
    sequence = []
    if len(s) % 2 == 1:
        return False
    for c in s:
        if c in poss_var.keys():
            sequence.append(c)
        elif c in poss_var.values():
            if not sequence or c != poss_var[sequence.pop()]:
                return False
    return not sequence
