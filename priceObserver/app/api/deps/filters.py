from fastapi import HTTPException, status, Query
from app.api.schemas import PairHistoryFilterDep
from pydantic import ValidationError
from datetime import datetime

def get_pair_history_filters(base: str = Query(min_length=1, max_length=10),
                             quote: str = Query(min_length=1, max_length=10),
                             start: datetime | None = Query(
                                default=None,
                                description="Start datetime filter in ISO format",
                                examples=["2026-01-01T07:30:00"]
                                ),
                             end: datetime | None = Query(
                                default=None,
                                description="End datetime filter in ISO format",
                                examples=["2026-12-21T10:30:00"]
                                ),
                             exchange: str | None = Query(
                                default=None,
                                description="Exchange name filter",
                                examples=["binance.com"]
                                )
                                ):
    try:
        return PairHistoryFilterDep(base=base, quote=quote,
                                    start=start, end=end,
                                    exchange=exchange)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid pair filter parameters")
