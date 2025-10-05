

class ProblemSolving:

    @staticmethod
    def valid_palindrome_125(s: str) -> bool:
        new_s = "".join(char.casefold() for char in s if char.isalnum())
        left, right = 0, len(new_s) - 1
        while left < right:
            if new_s[left] != new_s[right]:
                return False
            left += 1
            right -= 1
        return True

    @staticmethod
    def moves_zeroes_283(nums: list[int]) -> None:
        insert_pos = 0
        for num in nums:
            if num != 0:
                nums[insert_pos] = num
                insert_pos += 1
        for i in range(insert_pos, len(nums)):
            nums[i] = 0

    @staticmethod
    def merging_sorted_lists(first_l: list[int], second_l: list[int]) -> list[int]:
        final_list = []
        i = j = 0
        while i < len(first_l) and j < len(second_l):
            if first_l[i] < second_l[j]:
                final_list.append(first_l[i])
                i += 1
            else:
                final_list.append(second_l[j])
                j += 1
        final_list.extend(first_l[i:])
        final_list.extend(second_l[j:])
        return final_list

    @staticmethod
    def longest_substring_3(s: str) -> int:
        substring = ""
        max_substring = 0
        right_edge = 0
        for left_edge, char in enumerate(s):
            while s[right_edge] not in substring and right_edge < len(s):
                substring += s[right_edge]
                right_edge += 1
            if len(substring) > max_substring:
                max_substring = len(substring)
            substring = ""
            right_edge = left_edge + 1

        return max_substring


x = ProblemSolving()
print(x.longest_substring_3("abcabcbb"))