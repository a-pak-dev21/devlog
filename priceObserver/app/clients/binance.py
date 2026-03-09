import requests
from datetime import datetime
from logging import getLogger
from typing import Any
from app.clients.base_client import BaseClient


logger = getLogger(__name__)

class BinanceClient(BaseClient):

    def __init__(self) -> None:
        super().__init__(
            base_url='https://api.binance.com',
            name='Binance.com')
        
    def define_price(self, base: str, quote: str, snapshot_time: datetime | None = None) -> dict | None:
        symbol = f"{base.upper()}{quote.upper()}"
        logger.debug("Pair %s has been normalized", symbol)
        params: dict[str, str | list[str]] = {}
        price_endpoint = '/api/v3/ticker/price'
        params['symbol'] = symbol
        try:
            price_response = requests.get(self.base_url + price_endpoint, params=params, timeout=10)
            logger.debug("Response from Binance.com client retured %s code", price_response.status_code)
            price_response.raise_for_status()
            data = price_response.json()
            logger.info("Data from Binance client was successfully parsed: %s", data)
        except requests.Timeout:
            logger.exception("Waiting a response from %s exceeded 10 seconds, try again", self.base_url + price_endpoint)
            return None
        except requests.HTTPError:
            logger.exception("Bad response from server: %d, %s, try again",
                            price_response.status_code,
                            price_response.text)
            return None
        except requests.RequestException as e:
            logger.error("Error occurred: %s", e)
            return None
                
        output: dict[str, Any] = {
            'stock_exchange': self.name,
            'base': base,
            'quote': quote,
            'pair': f"{base.upper()}-{quote.upper()}",
            'price': round(float(data['price']), 2)
            #'timestamp': snapshot_time or datetime.now()
            }
        logger.info("Final output from Binance client is: %s", output)
        return output