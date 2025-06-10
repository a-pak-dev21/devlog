from collections import Counter


def solution(list_of_products):
    counted_purchases = Counter(list_of_products)
    most_popular = counted_purchases.most_common(1)[0][0]
    more_than_ones = [key for key, value in counted_purchases.items() if value > 1]

    return most_popular, more_than_ones

