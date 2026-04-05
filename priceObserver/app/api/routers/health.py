from fastapi import APIRouter, HTTPException, status, Depends
import app.db.db_queries as dbq
from typing import Annotated
from sqlalchemy import Connection
from app.db.session import get_conn



router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    return {"status": "healthy"}
    

@router.get("/ready")
def db_health_check(conn: Annotated[Connection, Depends(get_conn)]):
    db_ok = dbq.db_health_check(conn)
    if db_ok:
        return {
                "status": "ok",
                "db": "reachable"
                }
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail= {"status": "error", "db": "unreachable"})