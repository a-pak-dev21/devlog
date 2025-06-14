# Working with file company_employees.xlsx in /datas/
# Task #1:
#   count amount of employees
#   average salary by each department
#   The highest salary by each city

# Task #2:
#   for each department and gender:
#       average salary
#       max age
#   save result into dept_gender_summary.xlsx

# Task #3
#   find all people who employed for more than 3 years
#   add them into new column "Seniority" with value:
#       "Senior" if employed > 5 years
#       "Experienced" - 5 > x > 3
#   save result into new file ""long_term_employees.xlsx

# Task #4:
#   find in each department people who are working remotely
#   sor them in descending order and return top 3 departments
#   with highest % of remote workers


import pandas as pd
from pathlib import Path
import json
from datetime import datetime, timedelta


DATAS_DIR = Path("datas") / "company_employees.xlsx"


def task_1(data_dir) -> dict[str, any]:
    df = pd.read_excel(data_dir)
    # sample for easy access to view of table
    sample = df.sample()

    total_employees = len(df)
    avg_salary_by_dep = df.groupby(["Department"])["Salary"].mean().round(2)
    top_sal_by_city = df.groupby(["City"])["Salary"].max()

    result = {"total_employees": total_employees,"average_salary_by_dep": avg_salary_by_dep.to_dict(),
              "highest_salary_by_city": top_sal_by_city.to_dict()}
    return result


def task_2(data_dir) -> None:
    df = pd.read_excel(data_dir)
    # sample for easy access to view of table
    sample = df.sample()
    res = df.groupby(["Department", "Gender"]).agg({"Salary": "mean", "Age": "max"})
    res["Salary"] = res["Salary"].round(2)
    new_file_dir = Path("datas") / "dept_gender_summary.xlsx"
    res.to_excel(new_file_dir, index=True)


def task_3(data_dir) -> None:
    df = pd.read_excel(data_dir)
    # sample for easy access to view of table
    sample = df.sample()

    three_years_ago = datetime.now() - timedelta(days=(365 * 3))
    five_years_ago = datetime.now() - timedelta(days=(365 * 5 + 1))
    df["JoinDate"] = pd.to_datetime(df["JoinDate"], format="%Y-%m-%d")
    working_over_3_years = df[df["JoinDate"] < three_years_ago].copy()
    working_over_3_years["Seniority"] = working_over_3_years["JoinDate"].apply(
        lambda x: "Senior" if x < five_years_ago else "Experienced"
    )
    working_over_3_years["JoinDate"] = working_over_3_years["JoinDate"].dt.strftime("%Y-%m-%d")
    new_file_dir = Path("datas") / "long_term_employees.xlsx"
    working_over_3_years.to_excel(new_file_dir, index=False)


def task_4(data_dir) -> dict[str, dict[str, float]]:
    df = pd.read_excel(data_dir)
    # sample for easy access to view of table
    sample = df.sample()

    working_in_department = df.groupby("Department").size()
    remote_workers_by_department = df.groupby("Department")["IsRemote"].sum()
    percent_of_remote = ((remote_workers_by_department / working_in_department) * 100).round(2)
    top_3 = percent_of_remote.sort_values(ascending=False).head(3)

    return {"top_3_company_by_remote_workers": top_3.to_dict()}


summary_1 = json.dumps(task_1(DATAS_DIR), indent=2)
task_2(DATAS_DIR)
task_3(DATAS_DIR)
task_4(DATAS_DIR)
