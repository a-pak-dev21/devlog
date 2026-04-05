from fastapi import APIRouter, Depends
from app.api.schemas import ExchangeOut
import app.db.db_queries as dbq
from typing import Annotated
from app.db.session import get_conn
from sqlalchemy import Connection


router = APIRouter(tags=["exchanges"])

@router.get("/exchanges", response_model=list[ExchangeOut])
def get_exchanges(conn: Annotated[Connection, Depends(get_conn)]):
    return dbq.get_all_exchanges(conn)