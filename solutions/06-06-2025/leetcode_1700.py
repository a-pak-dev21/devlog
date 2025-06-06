# Number of student unable to eat lunch

# Given 2 stacks: students[] and sandwiches[].
# There is 2 types of sandwiches represented as 0(circular) and 1(square)
# If student in front of queue don't want to eat sandwich
# he goes to the end of the queue. It continues till the remaining row
# will not contain only students who dont want to eat there lunch
# return the number of this students

def solution(students: list[int], sandwiches: list[int]) -> int:
    # check if there is same amount of 0's and 1's in both lists
    # since both lists has same length and can contain only 0 and 1
    # it's enough to check only 1 element since other will be same anyway

    if students.count(1) == sandwiches.count(1):
        return 0
    else:
        while True:
            if sandwiches[0] not in students:
                return len(students)
            if students[0] == sandwiches[0]:
                students.pop(0)
                sandwiches.pop(0)
            else:
                students.append(students.pop(0))


students = [1, 1, 1, 0, 0, 1]
sandwiches = [1, 0, 0, 0, 1, 1]
print(solution(students, sandwiches))

# notes:
#       1) obviously if there is same amount of 0's and 1's in both
# lists than all students will eat their lunch
#       2) if 0's and 1's is different it means that anyway somebody
#       will be hungry but how many people depends on positions in
#       sandwiches stack
#       it's not enough only rely on
# amount of each type since they are lying as a stack so it also
# depends on their positions in queue
#       3) situations in which students will not each lunch:
#           a) sandwich on top of stack is that type which is not
#           preferable by any students in queue, means all students want same sandwich which is different from top one
#           (ex: all students 1's and top sandwich 0)
#           => when students reach ends of value on top of sandwiches
#
#           b) when I'm out of sandwiches of one of types, which is more
#           preferable since students queue moving, and it means more
#           students will eat their lunch
