# create a script which read datas from /data/people.csv with
# fieldnames: names, age, city.
# Filter only people who living in Prague and who is older than 25
# save result into new file data/prague_filtered.csv

import csv
from pathlib import Path


def solution(file_name: str) -> None:
    csv_file_dir = Path(f"data/{file_name}")
    with open(csv_file_dir, "r", newline="", encoding="utf-8") as r:
        reader = csv.DictReader(r)
        prague_citizens = [row for row in reader if row["city"].capitalize() == "Prague" and int(row["age"]) > 25]

    new_csv_file_dir = csv_file_dir.parent / "prague_filtered.csv"

    with open(new_csv_file_dir, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(prague_citizens)


solution("people.csv")



