def solution(numbers, target):
    left_p = 0
    right_p = len(numbers) - 1
    while left_p != right_p:
        if (numbers[left_p] + numbers[right_p]) == target:
            return [left_p + 1, right_p + 1]
        elif (numbers[left_p] + numbers[right_p]) < target:
            left_p += 1
        elif (numbers[left_p] + numbers[right_p]) > target:
            right_p -= 1
