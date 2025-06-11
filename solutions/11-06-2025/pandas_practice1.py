import pandas as pd
from pathlib import Path
from collections import Counter
import json


def solution():
    xlsx_data_dir = Path("datas") / "people_data.xlsx"
    df1 = pd.read_excel(xlsx_data_dir)

    row_amount = len(df1)
    cities = set(df1["City"])
    city_citizens = Counter(df1["City"])

    report = {"Amount of people:": row_amount,
              "Cities": list(cities),
              "Cities' citizens amount:": city_citizens}
    return json.dumps(report)




