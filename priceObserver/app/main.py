'''
Project which in the end will ask for a product name
and will search for this product on 2 or more different webs
to compare its price afterwards will save results to a 
connected database and will analyze dynamic in changes
and compare side by side same product from different webs
'''
import requests
from logging import getLogger
import csv
from abc import ABC, abstractmethod
from pathlib import Path
import os
from typing import Any
from datetime import datetime, timezone
from app.settings import BASE_DIR
from app.logging_config import root_logger_config


# BASE_DIR = Path(__file__).resolve().parent


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s: [%(levelname)s] %(name)s: %(message)s')

# file_handler = logging.FileHandler(filename= BASE_DIR.parent / 'artifacts/gen_logs.log', mode='a')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)

# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)

# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)
# logger.propagate = False




# class BaseClient(ABC):

#     def __init__(self, base_url: str, name: str) -> None:
#         self.base_url = base_url
#         self.name = name
    
#     @abstractmethod
#     def define_price(self, base: str, quote: str, snapshot_time: datetime | None = None) -> dict | None:
#         # Have to define a price for a single pair 
#         pass

#     def define_prices(self, symbols: list[tuple[str, str]]):
#         output_data: list = []
#         for base, quote in symbols:
#             result = self.define_price(base, quote)
#             if result is not None:
#                 output_data.append(result)
#             else:
#                 logger.warning("The price for pair: %s-%s hasn't been defined", base, quote)
#         return output_data
        

# class BinanceClient(BaseClient):

#     def __init__(self) -> None:
#         super().__init__(
#             base_url='https://api.binance.com',
#             name='Binance.com')
        
#     def define_price(self, base: str, quote: str, snapshot_time: datetime | None = None) -> dict | None:
#         symbol = f"{base.upper()}{quote.upper()}"
#         logger.debug("Pair %s has been normalized", symbol)
#         params: dict[str, str | list[str]] = {}
#         price_endpoint = '/api/v3/ticker/price'
#         params['symbol'] = symbol
#         try:
#             price_response = requests.get(self.base_url + price_endpoint, params=params, timeout=10)
#             logger.debug("Response from Binance.com client retured %s code", price_response.status_code)
#             price_response.raise_for_status()
#             data = price_response.json()
#             logger.info("Data from Binance client was successfully parsed: %s", data)
#         except requests.Timeout:
#             logger.exception("Waiting a response from %s exceeded 10 seconds, try again", self.base_url + price_endpoint)
#             return None
#         except requests.HTTPError:
#             logger.exception("Bad response from server: %d, %s, try again",
#                             price_response.status_code,
#                             price_response.text)
#             return None
#         except requests.RequestException as e:
#             logger.error("Error occurred: %s", e)
#             return None
                
#         output: dict[str, Any] = {
#             'stock_exchange': self.name,
#             'base': base,
#             'quote': quote,
#             'pair': f"{base.upper()}-{quote.upper()}",
#             'price': round(float(data['price']), 2)
#             #'timestamp': snapshot_time or datetime.now()
#             }
#         logger.info("Final output from Binance client is: %s", output)
#         return output
    

# class CoinbaseClient(BaseClient):

#     def __init__(self) -> None:
#         super().__init__(
#             base_url='https://api.coinbase.com',
#             name='Coinbase.com')

#     def define_price(self, base: str, quote: str, snapshot_time: datetime | None = None) -> dict | None:
#         symbol = f"{base.upper()}-{quote.upper()}"
#         logger.debug("Pair %s has been normalized", symbol)
#         price_endpoint = f'/v2/prices/{symbol}/spot'
#         logger.debug("Endpoint for pair %s, has been created: %s", symbol, price_endpoint)
#         try:
#             price_response = requests.get(self.base_url + price_endpoint, timeout=10)
#             logger.debug("Response from Coinbase.com client returned %s code", price_response.status_code)
#             price_response.raise_for_status()
#             data = price_response.json()
#             logger.info("Data from Coinbase client was successfully parsed: %s", data)
#         except requests.Timeout:
#             logger.exception("Waiting a response from %s exceeded 10 seconds, try again", self.base_url + price_endpoint)
#             return None
#         except requests.HTTPError:
#             logger.exception("Bad response from server: %d, %s, try again",
#                             price_response.status_code,
#                             price_response.text)
#             return None
#         except requests.RequestException as e:
#             logger.error("Error occurred: %s", e)
#             return None
        
#         output: dict[str, Any] = {
#             'stock_exchange': self.name,
#             'base': base,
#             'quote': quote,
#             'pair': f"{base.upper()}-{quote.upper()}",
#             'price': round(float(data['data']['amount']), 2)
#             }
#         logger.info("Final output from Coinbase client is: %s", output)
#         return output
    

# def get_clients() -> list[BaseClient]:
#     # In case of more clients add them here
#     return [
#         BinanceClient(),
#         CoinbaseClient()
#     ]


# def clients_price(base: str, quote: str, clients: list[BaseClient] | None = None) -> list[dict] | None:
        
#     if clients is None:
#         clients = get_clients()
#     clients_prices = []

#     for client in clients:
#         price = client.define_price(base, quote)
#         if price is not None:
#             clients_prices.append(price)
#         else:
#             logger.warning("%s client returned None for pair %s-%s",
#                            client.name, base, quote)
#     if not clients_prices:
#         logger.warning("All clients returned None for pair %s-%s", base, quote)
#         return None
    
#     return clients_prices


# def clients_prices(pairs: list[tuple[str, str]], clients: list[BaseClient] | None = None) -> list[dict] | None:
#     if any(map(lambda x: len(x) != 2, pairs)):
#         logger.error("All pairs given as (base, quote) tuples sohuld contain only 2 elements")
#         return None
    
#     all_prices = []

#     for base, quote in pairs:
#         pair_prices = clients_price(base, quote, clients=clients)
#         if pair_prices:
#             all_prices.extend(pair_prices)
    
#     if not all_prices:
#         return None
    
#     return all_prices


# def run_snapshot(pairs: list[tuple[str, str]],
#                  clients: list[BaseClient] | None = None) -> tuple[list[dict], datetime] | None:
#     snapshot_t = datetime.now(timezone.utc).replace(microsecond=0)
#     records = clients_prices(pairs=pairs, clients=clients)
#     if records is None:
#         return None

#     return records, snapshot_t

    
def import_to_csv(records: list[dict] | None, filename: Path | str = BASE_DIR / 'artifacts/prices.csv'):
    if not records:
        logger.warning("Not received any data to save at CSV")
        return None
    
    file_path = Path(filename)
    file_exists = file_path.exists()
    file_empty = file_exists and file_path.stat().st_size == 0

    with file_path.open('a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if (not file_exists) or file_empty:
            header = list(records[0].keys())
            header.append('timestamp')
            writer.writerow(header)
        for record in records:
            record['timestamp'] = datetime.now().replace(microsecond=0)
            writer.writerow(list(record.values()))

    logger.info("Saved %d records into %s", len(records), file_path)



if __name__ == '__main__':

    root_logger_config()
    logger = getLogger(__name__)

    test_pairs = [("BTC", "USDT"), ("BNB","USDT"), ("ETH","USDT")]
    compare_test_1 = ["btc-usdt","bnb-usdt","eth-usdt"]
    compare_test_2 = ["eur-usd","blah-blah"]
    compare_test_3 = ["eth-usdt","btcusdt"]
    compare_test_4 = ["eth-btc-usd","bnb"]


    


    # --> succesfully find best deals and log them
    # import_to_csv(valid_test, filename = BASE_DIR / 'best_deals.csv') # --> have to impor best deal to a csv
    # logger.info(compare_prices(compare_test_2)) # invalid test
    # logger.info(compare_prices(compare_test_3)) # invalid test
    # logger.info(compare_prices(compare_test_4)) # invalid test



#TODO:  1) transfer logger logic into separate file to not be caught into import loop trap 
#       2) валидно обрабатывать и возвращать что-то нормально выглядящее в случае
#           невалдиного сбора пар (400 - Binance & 404 - Coinbase)
#       3) раздробить main на несколько файлов и оставить только пусково - сборочную логику
