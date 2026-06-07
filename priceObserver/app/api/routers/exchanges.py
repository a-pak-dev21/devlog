from fastapi import APIRouter, Depends
import app.db.db_queries as dbq
from typing import Annotated
from app.db.session import get_conn
from sqlalchemy import Connection


router = APIRouter(tags=["exchanges"])

@router.get("/exchanges")
def get_exchanges(conn: Annotated[Connection, Depends(get_conn)]):
    return dbq.get_all_exchanges(conn)