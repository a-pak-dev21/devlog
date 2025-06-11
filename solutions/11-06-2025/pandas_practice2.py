# Уровень 2 — Средний
#
# Задача:
# Выведи:
# 	•	Средний возраст всех людей.
# 	•	Средний возраст по каждому городу.
# 	•	Города, где средний возраст выше 30.
#

import pandas as pd
from pathlib import Path
from collections import defaultdict
import json


def solution():

    csv_file_dir = Path("datas") / "people_data.csv"
    df = pd.read_csv(csv_file_dir)
    average_age = df["Age"].mean()
    ages_by_city = defaultdict(list)
    for row in range(len(df)):
        ages_by_city[df.iloc[row]["City"]].append(df.iloc[row]["Age"])

    avg_age_by_city = {key: int(sum(val) / len(val))for key, val in ages_by_city.items()}

    # df1 = pd.DataFrame(avg_age_by_city.items(), columns=["City", "Avg Age"])
    avg_age_over_30 = list(filter(lambda x: x[1] > 30, avg_age_by_city.items()))

    summary = {"Average age": average_age,
               "Average age in each city": avg_age_by_city,
               "Cities with average age over 30": sorted(avg_age_over_30, key=lambda x: x[1])}
    return json.dumps(summary)


solution()
