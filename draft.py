import requests

url = "https://api.coingecko.com/api/v3/coins/bitcoin/history"
headers = {"accept": "application/json"}
params = {"vs_currencies": "eur",
          "date": "03-07-2025"}
response_data = requests.get(url, headers=headers, params=params).json()

print(response_data.keys())
print(response_data["market_data"].keys())
print(response_data["market_data"]["current_price"])
print(type(response_data["market_data"]["current_price"]["eur"]))

