from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class PaginationDTO:
    order_by: Literal["time", "exchange", "price", "pair"]
    sort_dir: Literal["asc", "desc"]
    limit: int
    offset: int


@dataclass
class PairFiltersDTO:
    base: str | None
    quote: str | None
    start: datetime | None = None
    end: datetime | None = None
    exchange: str| None = None