from abc import ABC, abstractmethod
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)

class BaseClient(ABC):

    def __init__(self, base_url: str, name: str) -> None:
        self.base_url = base_url
        self.name = name
    
    @abstractmethod
    def define_price(self, base: str, quote: str, snapshot_time: datetime | None = None) -> dict | None:
        # Have to define a price for a single pair 
        pass

    def define_prices(self, symbols: list[tuple[str, str]]):
        output_data: list = []
        for base, quote in symbols:
            result = self.define_price(base, quote)
            if result is not None:
                output_data.append(result)
            else:
                logger.warning("The price for pair: %s-%s hasn't been defined", base, quote)
        return output_data
