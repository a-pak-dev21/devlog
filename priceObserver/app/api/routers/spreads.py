from fastapi import APIRouter, HTTPException, status, Depends
from app.api.schemas import SpreadOut
import app.db.db_queries as dbq
from typing import Annotated
from sqlalchemy import Connection
from app.db.session import get_conn


router = APIRouter(tags=["spreads"])

@router.get("/spreads/{snapshot_id}", response_model=list[SpreadOut])
def get_snapshot_spreads(conn: Annotated[Connection, Depends(get_conn)],
                         snapshot_id: int):
    result = dbq.get_snapshot_spreads(conn, snapshot_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snapshot with this id isn't existing")
    return result