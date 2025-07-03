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
        self.file_dir = Path("draft") / file_name
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
        if not isinstance(self.df["datum narození"].iloc[0], str):
            self.df["datum narození"] = self.df["datum narození"].dt.strftime("%d.%m.%Y")

        self.df = self.df[self.df["datum narození"] != "00.00.0000"].copy()

    def check_first_name(self) -> None:
        blank_name = self.df[(self.df["jméno"].isna()) & (self.df["příjmení"].str.split(" ").str.len() >= 2)]
        for idx, row in blank_name[["příjmení", "jméno"]].iterrows():
            split_name = row["příjmení"].split(" ")
            last_name, first_name = " ".join(split_name[:-1]), split_name[-1]
            self.df.loc[idx, ["příjmení", "jméno"]] = last_name, first_name
        self.df = self.df.dropna(subset=["jméno"])

    def viza_validation(self) -> None:
        self.df = self.df[(~self.df["státní občanství"].isin(self.viza_obligated))
                          | ((self.df["státní občanství"].isin(self.viza_obligated)) & (self.df["číslo víza"].notna()))]
        self.df["číslo víza"] = self.df["číslo víza"].fillna("")

    def pass_no_filter(self) -> None:
        self.df = self.df.dropna(subset=["číslo cestovního dokladu"])

    def fill_rsn_of_stay(self) -> None:
        self.df["Unnamed: 13"] = self.df["Unnamed: 13"].fillna("10")

    def address_filler(self) -> None:
        self.df[","] = self.df.apply(
            lambda row: choice(self.addresses[row["státní občanství"]]) if (len(str(row[","])) < 5) and
            (row["státní občanství"] in self.addresses) else row[","],
            axis=1
        )

    def apply_changes(self) -> pd.DataFrame:
        self.remove_invalid_dob()
        self.pass_no_filter()
        self.check_first_name()
        self.viza_validation()
        self.fill_rsn_of_stay()
        self.address_filler()
        return self.df


csv_path = Path("data/visa_obligated.csv")
json_path = Path("data/addresses_data.json")

my_df = DataCleaner("Ubydata_19B.xls", "Seznam", csv_path, json_path)
df_out = my_df.apply_changes()
df_out.to_excel("draft/solution.xlsx", index=False)


# TODO: 1) correctly return all columns data types? mostly string, or dates
#       2) fix addresses with duplicate cities, and "Street 1"
#       3) if iso2 index in address is not in my json, update it
#       by adding new key and notify about this, so i would know to
#       add new values to this keys
#       4) remove duplicate guests by passport number and names
#       pretty much 2 rows would be the same so maybe set()?
#       5) len(pass) <= 5
#       6) pass = "XXXXXX123"
#       7) len(firstName) > 1 word
