from pydantic import BaseModel
from datetime import datetime


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
    pairs: list[tuple[str, str]]

class PostSnapshotOut(BaseModel):
    snapshot_id: int
    rows_count: int
