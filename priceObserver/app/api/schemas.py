from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import Literal
from fastapi import Query


class PairHistoryFilterDep(BaseModel):
    base: str = Query(min_length=1, max_length=10)
    quote: str = Query(min_length=1, max_length=10)
    start: datetime | None = Query(
        default=None,
        description="Start datetime filter in ISO format",
        examples=["2026-01-01T07:30:00"]
    )
    end: datetime | None = Query(
        default=None,
        description="End datetime filter in ISO format",
        examples=["2026-12-21T10:30:00"]
    )
    exchange: str| None = Query(
        default=None,
        description="Exchange name filter",
        examples=["binance.com"]
    )
      

    @field_validator("base", "quote", mode="before")
    @classmethod
    def base_quote_format(cls, v) -> str:
        if not isinstance(v, str):
            raise ValueError("Base and Quote instances must be a string")
        return v.upper().strip()
    
    @field_validator("exchange", mode="before")
    @classmethod
    def exchange_check(cls, v) -> str | None:

        if v is None:
            return None
        
        if not isinstance(v, str):
            raise ValueError("Exchange name instance must be a string")
        
        return v.lower().strip()

    @model_validator(mode="after")
    def pair_and_timegap_checks(self):
        # base != quote
        if self.base == self.quote:
            raise ValueError("Base and quote values cannot be the same string")
    
        # start <= end
        if self.start is not None and self.end is not None:
            if self.start > self.end:
                raise ValueError("Starting datetime cannot be later then ending datetime")
        return self
    

class PaginationDep(BaseModel):
    order_by: Literal["time", "exchange", "price", "pair"] = Query(
        default="time",
        description="Column to sort by",
        examples=["time"]
        )
    sort_dir: Literal["desc", "asc"] = Query(
        default="desc",
        description="In which direction sort elements",
        examples=["desc"]
        )
    limit: int = Query(default=5, gt=0, le=100, description="Amount of elements on a page")
    offset: int = Query(default=0, ge=0, description="Index to move elements on")


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

class PayloadOut(BaseModel):
    sub: str
    role: str
    exp: datetime