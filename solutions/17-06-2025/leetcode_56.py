# варианты решения:


# находить макс и мин выбивать их со списка продолжать сверяя по паре
# с обеих сторон

# создать 2 отдельных массива значений 1-го индекса и 2-го индекса

# отсортировать список по минимальному значению первого числа пары
# и по максимальному значению второго числа пары и что-то придумать

def solution(intervals: list[list[int]]) -> list[list[int]]:
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    print(sorted_intervals)
    while True:
        for i in range(len(sorted_intervals) - 1):
            print(sorted_intervals[i])
            if sorted_intervals[i][1] >= sorted_intervals[i+1][0]:
                sorted_intervals = [(sorted_intervals[i][0]), max([sorted_intervals[i][1], sorted_intervals[i+1][1]])] + sorted_intervals[i+2:]
                print("")
                break
        else:
            break
    return sorted_intervals


intervals1 = [[2,3],[2,2],[3,3],[1,3],[5,7],[2,2],[4,6]]
solution(intervals1)


