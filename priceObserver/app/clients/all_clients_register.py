from app.clients.base_client import BaseClient
from app.clients.binance import BinanceClient
from app.clients.coinbase import CoinbaseClient


def get_clients() -> list[BaseClient]:
    # In case of more clients add them here
    return [
        BinanceClient(),
        CoinbaseClient()
    ]