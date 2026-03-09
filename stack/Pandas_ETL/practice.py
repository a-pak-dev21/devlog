from collections import Counter, defaultdict

def two_sum(nums, target):
    my_dict = {}
    for index, num in enumerate(nums):
        second_num = target - num
        if second_num in my_dict:
            return [index, nums.index(second_num)]
        my_dict[second_num] = index
    print(my_dict)
        
    
test = [2,7,11,15]
target = 9
print(two_sum(test, target))