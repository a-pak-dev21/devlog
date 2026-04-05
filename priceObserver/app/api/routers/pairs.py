from fastapi import APIRouter, HTTPException, status, Depends
from app.api.schemas import Snapshot, PairOut, PaginationDep
from datetime import datetime
import app.db.db_queries as dbq
from typing import Annotated
from sqlalchemy import Connection
from app.db.session import get_conn


router = APIRouter(tags=["pairs"])
  

@router.get("/pairs", response_model=list[PairOut])
def get_pairs(conn: Annotated[Connection, Depends(get_conn)],
              pagination_params: Annotated[PaginationDep, Depends(PaginationDep)]):
    return dbq.get_all_pairs(conn,
                             pagination_params.order_by,
                             pagination_params.sort_dir,
                             pagination_params.limit,
                             pagination_params.offset
                             )


@router.get("/pairs/history", response_model= list[Snapshot])
def get_pair_history(conn: Annotated[Connection, Depends(get_conn)],
                     pagination_params: Annotated[PaginationDep, Depends(PaginationDep)],
                     base: str, quote: str,
                     start: datetime | None = None, end: datetime | None = None,
                     exchange: str | None = None
                     ):
    
    if base == quote:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The base and quote cannot be same")

    if start is not None and end is not None:
        if start > end:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="starttime cannot be greater then endtime")

    return dbq.get_pair_timeseries(conn,
                                pagination_params.order_by,
                                pagination_params.sort_dir,
                                pagination_params.limit,
                                pagination_params.offset,
                                base, quote, start, end, exchange)