# create a script that will read a file from data/sales.csv
# sum all sales from column (amount)
# create a new csv-file data/sales_summary.csv which contains following line:
# total_sales, <sum>

import csv
from csv import DictReader
from pathlib import Path


def solution(file_name: str) -> None:
    file_dir = Path(f"data/{file_name}")
    with open(file_dir, "r", newline="", encoding="utf-8") as r:
        reader = DictReader(r)
        total_sales = sum(int(row["amount"]) for row in reader)

    new_file = file_dir.parent / "sales_summary.csv"
    with open(new_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["total_sales", total_sales])
