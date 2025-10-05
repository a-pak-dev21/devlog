from collections import defaultdict


class Solution:

    # 3. Longest Substring Without Repeating Characters
    @staticmethod
    def length_of_longest_substring(s: str) -> int:
        left = 0
        substring = {}
        max_substring = 0
        for right, elem in enumerate(s):
            if elem in substring and substring[elem] >= left:
                left = substring[elem] + 1
            substring[elem] = right
            max_substring = max(max_substring, right - left + 1)
        return max_substring

    # 209. Minimum Size Subarray Sum
    @staticmethod
    def min_subarray_len(target: int, nums: list[int]) -> int:
        left = 0
        min_substring = float('inf')
        sub_sum = 0
        for right, elem in enumerate(nums):
            sub_sum += elem
            while sub_sum >= target:
                if min_substring == 1:
                    return 1
                min_substring = min(min_substring, right - left + 1)
                sub_sum -= nums[left]
                left += 1
        return 0 if min_substring == float('inf') else min_substring

    # 424. Longest Repeating Character Replacement
    @staticmethod
    def character_replacement(s: str, k: int) -> int:
        left = 0
        longest = 0
        most_common_char = 0
        count = defaultdict(int)
        for right, char in enumerate(s):
            count[char] += 1
            if count[char] > most_common_char:
                most_common_char = count[char]

            while (right - left + 1) - most_common_char > k:
                count[s[left]] -= 1
                left += 1

            window_len = right - left + 1
            print(window_len)
            print(s[left:right + 1])
            if window_len > longest:
                longest = window_len
        return longest

