# Small warm up for working with real APIs

import requests
from datetime import datetime
import pandas as pd
from pathlib import Path

url = "https://api.exchangerate.host/live"
params = {
    "access_key": "8e7d3f68c3ae8d150ca363467d0170ce"
}

response = requests.get(url, params=params).json()

exchange_currencies = {"EUR": response["quotes"].get("USDEUR"),
                       "CZK": response["quotes"].get("USDCZK"),
                       "RUB": response["quotes"].get("USDRUB")}

data = {"Date": str(datetime.today().date()),
        "Currency": list(exchange_currencies.keys()),
        "Rate": list(exchange_currencies.values())
        }

df = pd.DataFrame(data)
exchange_summ_dir = Path("data")
exchange_summ_dir.mkdir(exist_ok=True)
df.to_excel(exchange_summ_dir / "today_exchange_rates.xlsx", index=False)

