# Have list of dictionaries, each of them presenting
# the guest's order. Tasks to do:
#       return 2 most popular products among all clients
#       return how many different clients had bought at least one
# of following products {"milk", "cheese"}
#       return the most often bought products for each client
#       (some of them can be mentioned few times)

import collections as cll
import json


def solution(list_of_orders: list[dict[str, str | list[str]]]) -> json:
    all_orders = cll.Counter()
    clients = cll.defaultdict(cll.Counter)
    for order in list_of_orders:
        all_orders.update(order["products"])
        clients[order["client"]].update(order["products"])

    top_2_products = all_orders.most_common(2)

    milk_or_cheese = sum(1 for name, products in clients.items() if ("milk" in products) or ("cheese" in products))

    clients_fav_product = {name: products.most_common(1)[0][0] for name, products in clients.items()}

    datas = {"top_2_products": [top_2_products[0][0], top_2_products[1][0]],
             "orders_with_milk_or_cheese": milk_or_cheese,
             "clients_fav_products": clients_fav_product}

    return json.dumps(datas, indent=4)


# orders = [
#     {"client": "Alice", "products": ["milk", "bread", "eggs"]},
#     {"client": "Bob", "products": ["bread", "milk"]},
#     {"client": "Charlie", "products": ["eggs", "cheese"]},
#     {"client": "Alice", "products": ["bread", "cheese"]},
#     {"client": "Bob", "products": ["milk", "eggs", "bread"]},
# ]
#
# print(solution(orders))
