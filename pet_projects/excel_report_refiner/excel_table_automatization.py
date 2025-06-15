"""
Script to automate the cleaning/modifying guest's data in Excel format.
See guest_cleaner_README.md for detailed specification and usage.
"""

import pandas as pd
from pathlib import Path
import json
import openpyxl
from random import choice


class DataCleaner:

    # Initializing path to our data_file and new instance of DataFrame to work with datas
    # Also control if both values are strings

    def __init__(self, file_name: str, sheet_name: str, viza_path: str | Path, addresses_path: str | Path) -> None:
        assert isinstance(file_name, str), "The name of file should be a string value"
        assert isinstance(sheet_name, str), "Insert valid name of the excel sheet"
        self.file_dir = Path("data") / file_name
        self.df = pd.read_excel(self.file_dir, sheet_name=sheet_name)
        self.viza_obligated = self._load_viza_required(viza_path)
        self.addresses = self._load_addresses(addresses_path)

    # From this part, we will start to modify our table
    # First in priorities we will perform all method which removing
    # invalid rows to not fill and process them for nothing
    # after modify and fill remaining rows

    @staticmethod
    def _load_viza_required(path: str | Path) -> set:
        return set(pd.read_csv(path)["Visa Obligated"])

    @staticmethod
    def _load_addresses(path: str | Path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def remove_invalid_dob(self) -> None:
        if not isinstance(self.df["DoB"].iloc[0], str):
            self.df["DoB"] = self.df["DoB"].dt.strftime("%d.%m.%Y")

        self.df = self.df[self.df["DoB"] != "00.00.0000"].copy()

    def check_first_name(self) -> None:
        blank_name = self.df[(self.df["FirstName"].isna()) & (self.df["LastName"].str.split(" ").str.len() >= 2)]
        for idx, row in blank_name[["LastName", "FirstName"]].iterrows():
            split_name = row["LastName"].split(" ")
            last_name, first_name = " ".join(split_name[:-1]), split_name[-1]
            self.df.loc[idx, ["LastName", "FirstName"]] = last_name, first_name
        self.df = self.df.dropna(subset=["FirstName"])

    def viza_validation(self) -> None:
        self.df = self.df[(~self.df["Nationality"].isin(self.viza_obligated))
                          | ((self.df["Nationality"].isin(self.viza_obligated)) & (self.df["VizaNumber"].notna()))]
        self.df["VizaNumber"] = self.df["VizaNumber"].fillna("")

    def missing_pass_no(self) -> None:
        self.df = self.df.dropna(subset=["PassportNumber"])

    def fill_rsn_of_stay(self) -> None:
        self.df["ReasonOfStay"] = self.df["ReasonOfStay"].fillna("10")

    def address_filler(self) -> None:
        self.df["Address"] = self.df.apply(
            lambda row: choice(self.addresses[row["Nationality"]]) if (len(str(row["Address"])) < 5) and
            (row["Nationality"] in self.addresses) else row["Address"],
            axis=1
        )

    def apply_changes(self) -> pd.DataFrame:
        self.remove_invalid_dob()
        self.missing_pass_no()
        self.check_first_name()
        self.viza_validation()
        self.fill_rsn_of_stay()
        self.address_filler()
        return self.df


csv_path = Path("data/visa_obligated.csv")
json_path = Path("data/addresses_data.json")

x = DataCleaner("guest_file.xlsx", "Sheet1", csv_path, json_path)
df_out = x.apply_changes()
print(df_out.sample(5)[["LastName", "FirstName", "Nationality","Address","VizaNumber","ReasonOfStay"]])


