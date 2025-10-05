class solution:

    # 167. Two Sum II - Input Array Is Sorted
    @staticmethod
    def two_sum(numbers: list[int], target: int) -> list[int]:
        left_p = 0
        right_p = len(numbers) - 1
        while left_p != right_p:
            if (numbers[left_p] + numbers[right_p]) == target:
                return [left_p + 1, right_p + 1]
            elif (numbers[left_p] + numbers[right_p]) < target:
                left_p += 1
            elif (numbers[left_p] + numbers[right_p]) > target:
                right_p -= 1

    # 125. Valid Palindrome
    @staticmethod
    def is_palindrome(s: str) -> bool:
        new_s = "".join(char.lower() for char in s if char.isalnum())
        left, right = 0, len(new_s) - 1
        while left < right:
            if new_s[left] != new_s[right]:
                return False
            left += 1
            right -= 1
        return True

    # 283. Move Zeroes
    @staticmethod
    def move_zeroes(nums: list[int]) -> None:
        insert_pos = 0
        for num in nums:
            if num != 0:
                nums[insert_pos] = num
                insert_pos += 1
        for i in range(insert_pos, len(nums)):
            nums[i] = 0
