# Problems mostly focused on using hash maps

class Solution:

    # LeetCode 560. Subarray Sum Equals K
    @staticmethod
    def leetcode_560(nums: list[int], k: int = 0):
        counter = 0
        prefixes = {counter: 0}
        subsum = 0
        for elem in nums:
            subsum += elem
            counter += 1
            prefixes[counter] = subsum
        return prefixes.values()

            
x = Solution()
print(x.leetcode_560([1,2,3,4,-2,1,6,-3], 3))