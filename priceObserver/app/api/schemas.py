from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class PaginationDep(BaseModel):
    order_by: Literal["time", "exchange", "price", "pair"] = Field(
        description="Column to sort by",
        examples=["time"]
        )
    sort_dir: Literal["desc", "asc"] = Field(
        default="desc",
        description="In which direction sort elements",
        examples=["desc"]
        )
    limit: int = Field(default=5, gt=0, le=100, description="Amount of elements on a page")
    offset: int = Field(default=0, ge=0, description="Index to move elements on")



class ExchangeOut(BaseModel):
    name: str

class PairOut(BaseModel):
    base: str
    quote: str
    pair: str

class Snapshot(BaseModel):
    time: datetime
    pair: str
    base: str
    quote: str
    exchange: str
    price: float

class SpreadOut(BaseModel):
    time: datetime
    pair: str
    lowest_price: float
    highest_price: float
    abs_spread: float
    pct_spread: float
    best_buy_on: str
    best_sell_on: str

class InputPairs(BaseModel):
    pairs: list[tuple[str, str]] = Field(examples=[[("BTC", "USDT"), ("BNB","USDT"), ("ETH","USDT")]])

class PostSnapshotOut(BaseModel):
    snapshot_id: int
    rows_inserted: int
