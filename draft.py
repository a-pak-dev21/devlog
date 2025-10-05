def solution(target: int, nums: list[int]) -> int:
    left = 0
    min_substring = float('inf')
    sub_sum = 0
    for right, elem in enumerate(nums):
        sub_sum += elem
        while sub_sum >= target:
            min_substring = min(min_substring, right - left + 1)
            sub_sum -= nums[left]
            left += 1
    return 0 if min_substring == float('inf') else min_substring


x = [2,3,1,2,4,3]
x1 = [1,4,4]
x2 = [1,1,1,1,1,1,1]
target = 11
print(solution(target, x2))
