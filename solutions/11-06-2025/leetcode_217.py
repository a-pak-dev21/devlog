# 217.Contains Duplicate

def contains_duplicate( nums: list[int]) -> bool:
    if len(nums) != len(set(nums)):
        return True
    else:
        return False
