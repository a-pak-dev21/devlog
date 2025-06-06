# Create a Csv-file data/basic_data.csv, containing some strings

import csv
from pathlib import Path


def solution(folder_name: str, datas: list[any]) -> float:
    folder_dir = Path(folder_name)
    folder_dir.mkdir(exist_ok=True)
    with open(folder_dir / "basic_data.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(datas)
    with open(folder_dir / "basic_data.csv", "r", newline='', encoding="utf-8") as r:
        reader = csv.reader(r)
        ages = [int(row[1]) for row in reader]
        avg_age = sum(ages) / len(ages)

    return round(avg_age, 1)


simple_data = [["Alice",30],
               ["Bob", 21],
               ["John", 15]]

solution("data", simple_data)
