from openpyxl import Workbook
from pathlib import Path


def solution():
    data_dir = Path("datas")
    data_dir.mkdir(exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "1st_task"
    ws.append(["Name", "Age", "City"])
    # Added by user
    ws.append((input("Enter Name, Age and City space-delimited: ").strip()).split(" "))
    # Added just through the file
    ws.append(["John", "21", "Miami"])
    ws.append(["Bob", "55", "Paris"])
    ws.append(["Selena", "19", "Moscow"])
    wb.save(data_dir / "data.xlsx")




