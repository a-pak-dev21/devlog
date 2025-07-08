import requests
from datetime import datetime, timedelta
from collections import defaultdict
import time
import pandas as pd


class CryptoAnalyser:

    def __init__(self) -> None:
        self.base_url = "https://api.coingecko.com/api/v3/"
        self.headers = self._headers()
        self.params = self._params()

    @staticmethod
    def _headers() -> dict[str, str]:
        return {"accept": "application/json"}

    @staticmethod
    def _params(new_params: dict[str, str] = None) -> dict[str, str]:
        std_params = {"vs_currencies": "eur"}
        if new_params is not None:
            std_params.update(new_params)
        return std_params

    def _constructor(self, endpoint: str, coin_id_list: list[str] | None):
        url = self.base_url + endpoint
        list_as_str = ",".join(coin_id_list)
        params = self._params({"ids": list_as_str})
        return requests.get(url, headers=self.headers, params=params)

    def coin_in_eur(self, endpoint: str, coin_id_list: list[str]):
        response = self._constructor(endpoint, coin_id_list)
        data = {key.upper(): val["eur"] for key, val in response.json().items()}
        return data

    def compare_by_day(self, coin_id_list: list[str], day1=datetime.today().date(),
                       day2=(datetime.today() - timedelta(days=1)).date()) -> dict[str, list[str]]:
        day1_to_str: str = day1.strftime(format="%d-%m-%Y")
        day2_to_str: str = day2.strftime(format="%d-%m-%Y")
        coins_url_list: list[str] = [f"{self.base_url}coins/{coin}/history" for coin in coin_id_list]
        data: dict[str, list[str]] = defaultdict(list)
        my_currency = self._params()["vs_currencies"]
        # coin_converted: dict[str, float | list[str]] = {}
        for day in [day1_to_str, day2_to_str]:
            params = self._params({"date": day})
            data["Date"].append(day)
            for url in coins_url_list:
                response = requests.get(url, headers=self.headers, params=params)
                time.sleep(1)
                if response.status_code != 200:
                    print("Bad response", response.status_code)
                    return None
                response_data = response.json()
                curr_value = response_data.get("market_data", {}).get("current_price", {}).get("eur")
                data[response_data.get("symbol")].append(curr_value)
        return data


coin_list = ["bitcoin", "ethereum", "tether"]
res = CryptoAnalyser()
# print(res.coin_in_eur("simple/price", coin_list))
df = pd.DataFrame(res.compare_by_day(coin_list))
df.to_excel("crypto_analyzer.xlsx", index=False)
