import requests
from pathlib import Path
import pandas as pd
from datetime import datetime

from dateutil.utils import today


class ExchangeRate:

    def __init__(self) -> None:
        self.base_url = "https://api.exchangerate.host/"
        self.access_key = self._access_key()
        self.source_curr = self._source_curr()
        self.currency_list = self._filter_curr()

    @staticmethod
    def _access_key():
        return "8e7d3f68c3ae8d150ca363467d0170ce"

    @staticmethod
    def _source_curr():
        return input("Enter the currency which you want to check: ").upper()

    @staticmethod
    def _filter_curr():
        return input("Enter currencies you're interested in: ").strip().upper().split()

    def week_rates(self, endpoint: str, from_date: str, to_date: str):
        url: str = self.base_url + endpoint
        params: dict[str, str] = {
            "access_key": self.access_key,
            "source": self.source_curr,
            "start_date": from_date,
            "end_date": to_date
        }
        response = requests.get(url, params=params).json()
        if not response.get("success", True):
            raise ValueError("API request failed or exceeded the limit")
        # Return dictionary-type object with different key, value pairs
        # Most interesting for my purposes is: "quotes" key
        # which in case of timeframe contains:
        # dates by days as a keys and inserted dictionary
        # with all names as keys and rates as values
        # example: {"quotes": {"2025-06-26": {"USDAED": 3.67}}}
        data = {"Date": []}
        currencies_data = {key: [] for key in self.currency_list}
        data.update(currencies_data)
        for date, val in response["quotes"].items():
            data["Date"].append(date)
            for currency in self.currency_list:
                curr_name = self.source_curr + currency
                data[currency].append(val[curr_name])
        return data

    def today_rate(self):
        data = self.week_rates("timeframe", "2025-06-23", "2025-06-29")
        today_date = datetime.today().strftime(format='%Y-%m-%d')
        if today_date not in data["Date"]:
            url = self.base_url + "latest"
            params = {
                "access_key": self.access_key,
                "source": self.source_curr
            }
            response = requests.get(url, params=params).json()
            if not response.get("success", True):
                raise ValueError("API request failed or exceeded the limit")

            for key in data.keys():
                if key == "Date":
                    data["Date"].append(today_date)
                else:
                    curr_key = self.source_curr + key
                    data[key].append(response["quotes"][curr_key])
        return data

    def send_to_excel(self):
        df_out = pd.DataFrame(self.today_rate())
        folder_dir = Path("data")
        folder_dir.mkdir(exist_ok=True)
        file_dir = folder_dir / "week_rates.xlsx"
        df_out.to_excel("data/week_rates.xlsx", index=False)


var = ExchangeRate()
var.today_rate()
var.send_to_excel()

