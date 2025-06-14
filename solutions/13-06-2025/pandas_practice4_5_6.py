# Task #1:
#   return average age for all datas
#   unique cities and amount of people in each of them
#   average salary for male and female separately

# Task #2
#   return cities where avg salary is higher than 70 000
#   for each city - amount of people younger than 30
#   Find all employees, who is working more than 1 year(JoinDate)

# Task #3
#   sort table by City and after by Salary
#   create a column "Group Info" with a row as:
#       "<Name> from <City> earns <Salary>
#   for each gender and city count average salary and max age -
#   after save result and save as a new table "gender_city_stats.xlsx"


import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


DATAS_DIR = Path("datas") / "advanced_people_data.xlsx"


def solution_1():

    df = pd.read_excel(DATAS_DIR)
    average_age = df["Age"].mean()
    city_citizens = df.groupby(["City"]).size()
    city_citizens = city_citizens.sort_values(ascending=False)
    avg_salary_by_gender = df.groupby("Gender")["Salary"].mean()

    summary = {"average_age": average_age,
               "amount_of_citizens_in_cities": city_citizens.to_dict(),
               "average_salary_by_gender": {key: val for key, val in avg_salary_by_gender.items()}}
    return summary


def solution_2():

    df = pd.read_excel(DATAS_DIR)
    cities_with_high_vg_sal = df.groupby("City")["Salary"].mean()
    cities_with_high_vg_sal = cities_with_high_vg_sal[cities_with_high_vg_sal > 70000]

    people_under_30_by_cities = df[df["Age"] < 30].groupby("City").size()
    people_under_30_by_cities = people_under_30_by_cities.sort_values(ascending=False)

    one_year_ago = pd.to_datetime(datetime.now() - timedelta(days=365))
    df["JoinDate"] = pd.to_datetime(df["JoinDate"], format="%Y-%m-%d")
    employed_over_year = df[df["JoinDate"] < one_year_ago]

    summary = {"cities_with_high_avg_sal": cities_with_high_vg_sal.to_dict(),
               "people_under_30_by_cities": people_under_30_by_cities.to_dict(),
               "employed_over_year": employed_over_year.to_dict("records")}

    return summary


def solution_3():

    df = pd.read_excel(DATAS_DIR)
    df = df.sort_values(["City", "Salary"], ascending=[True, False])

    df["Group Info"] = df.apply(lambda row: f"{row['Name']} from {row['City']} earns {row['Salary']}", axis=1)

    city_gender = df.groupby(["City", "Gender"]).agg({"Salary": "mean", "Age": "max"})
    city_gender["Salary"] = city_gender["Salary"].round(2)

    df_out = pd.DataFrame(city_gender)
    df_out.to_excel("datas/grouped_by_cities_and_genders.xlsx", index=False)


# solution_1()
# solution_2()
# solution_3()
