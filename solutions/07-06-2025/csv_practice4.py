# working with file from /06-06-2025/data/sales.csv
# the script should read csv file, find the total sales
# Find sales by each product name ( product: total_amount)
# Create top-3 days by sales (date: total_amount)
# Create a Json-report which will contain all this info

import json
import csv
from pathlib import Path


def solution() -> None:
    sales_dir = Path("../06-06-2025/data/sales.csv")
    product_sales = {}
    dates = {}
    total_sales = 0
    with open(sales_dir, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_sales += int(row["amount"])
            product_sales.setdefault(row["product"], 0)
            dates.setdefault(row["date"], 0)
            product_sales[row["product"]] += int(row["amount"])
            dates[row["date"]] += int(row["amount"])

    sorted_by_sales = sorted(dates.items(), key=lambda x: x[1], reverse=True)
    top_three_sales_dates = [{"date": elem[0], "amount": elem[1]} for elem in sorted_by_sales[:3]]
    complete_report = {"total_sales": total_sales,
                       "sales_by_product": product_sales,
                       "top_3_days": top_three_sales_dates}

    new_json_report_dir = Path("../06-06-2025/data/sales_report.json")
    with open(new_json_report_dir, "w", encoding="utf-8") as f_out:
        json.dump(complete_report, f_out)


solution()



