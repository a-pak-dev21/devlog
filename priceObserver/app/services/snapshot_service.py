from logging import getLogger
from app.clients.base_client import BaseClient
from app.services.collector import run_snapshot
from app.db.db import save_snapshot
from typing import Annotated
from sqlalchemy import Connection
from fastapi import Depends
from app.db.session import get_conn

logger = getLogger(__name__)

def run_and_save_snapshot(conn: Annotated[Connection, Depends(get_conn)],
                          pairs: list[tuple[str, str]],
                          clients: list[BaseClient] | None = None) -> dict[str, int] | None:
    result = run_snapshot(pairs, clients=clients)
    if result is None:
        logger.error("Function 'run_snapshot' returned None")
        return None
    else:
        records, snapshot_t = result
        result = save_snapshot(conn, records=records, timestamp=snapshot_t)
        return result
    