from fastapi import APIRouter, Depends, Query
from app.api.schemas import Snapshot, PairOut, PaginationDep, PairHistoryFilterDep
import app.db.db_queries as dbq
from typing import Annotated
from sqlalchemy import Connection
from app.db.session import get_conn
from app.api.dto import PaginationDTO, PairFiltersDTO


router = APIRouter(tags=["pairs"])
  

@router.get("/pairs", response_model=list[PairOut])
def get_pairs(conn: Annotated[Connection, Depends(get_conn)],
              limit: int = Query(default=5, gt=0, description="Amount of elements on page"),
              offset: int = Query(default=0, ge=0, description="Offset n elements")):
    
    return dbq.get_all_pairs(conn, limit, offset)


@router.get("/pairs/history", response_model= list[Snapshot])
def get_pair_history(conn: Annotated[Connection, Depends(get_conn)],
                     pagination_params: Annotated[PaginationDep, Depends(PaginationDep)],
                     filter_params: Annotated[PairHistoryFilterDep, Depends(PairHistoryFilterDep)]
                     ):
    
    pagination = PaginationDTO(**pagination_params.model_dump())
    filters = PairFiltersDTO(**filter_params.model_dump())

    return dbq.get_pair_timeseries(conn, pagination, filters)