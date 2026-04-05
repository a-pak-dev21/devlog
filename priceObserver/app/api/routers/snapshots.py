from fastapi import APIRouter, status, Depends
from app.api.schemas import Snapshot, InputPairs, PostSnapshotOut
import app.db.db_queries as dbq
from logging import getLogger
from app.services.snapshot_service import run_and_save_snapshot
from typing import Annotated
from sqlalchemy import Connection
from app.db.session import get_conn


logger = getLogger()

router = APIRouter(tags=["snapshots"])

@router.get("/last-snapshot", response_model=list[Snapshot])
def get_last_snapshot(conn: Annotated[Connection, Depends(get_conn)]):
    return dbq.get_latest_snapshot(conn)


@router.post("/post-snapshot", response_model=PostSnapshotOut, status_code=status.HTTP_201_CREATED)
def post_new_snapshot(conn: Annotated[Connection, Depends(get_conn)], pairs: InputPairs):
    result = run_and_save_snapshot(conn, pairs.pairs)
    if result:
        logger.info(f"New snapshot with id: {result['snapshot_id']} saved, {result['rows_inserted']} records has been added")
    else:
        logger.warning("0 rows has been inserted")
    return result