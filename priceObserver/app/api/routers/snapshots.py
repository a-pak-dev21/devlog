from fastapi import APIRouter, status, Depends
from app.api.schemas import Snapshot, InputPairs, PostSnapshotOut
import app.db.db_queries as dbq
from logging import getLogger
from app.services.snapshot_service import run_and_save_snapshot
from typing import Annotated
from sqlalchemy import Connection
from app.db.session import get_conn
from app.api.deps.api_auth import get_current_user
from datetime import datetime, timezone
from fastapi.exceptions import HTTPException
from app.api.schemas import PayloadOut


logger = getLogger()

router = APIRouter(tags=["snapshots"])

@router.get("/last-snapshot", response_model=list[Snapshot])
def get_last_snapshot(conn: Annotated[Connection, Depends(get_conn)]):
    return dbq.get_latest_snapshot(conn)


@router.post("/post-snapshot", response_model=PostSnapshotOut, status_code=status.HTTP_201_CREATED)
def post_new_snapshot(conn: Annotated[Connection, Depends(get_conn)],
                      pairs: InputPairs,
                      payload: Annotated[PayloadOut, Depends(get_current_user)]):
    
    logger.info(f"Authorized request by user-{payload.sub}")
    
    if payload.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin role required")
    
    logger.info(f"For testing authorization, User which currently sending request is: {payload.sub}")

    result = run_and_save_snapshot(conn, pairs.pairs)
    
    if not result:
        logger.warning("Price insertion ends with error, check error table")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Price insertion fell of with error")
    
    return result
