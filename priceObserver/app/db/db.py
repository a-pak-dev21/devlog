from sqlalchemy import Engine, Connection
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
from logging import getLogger
from app.services.collector import run_snapshot
from app.db.models import metadata, pairs_table, exchanges_table, prices_table, snapshots_table, errors_table
from app.settings import settings
from datetime import datetime
from typing import Literal, Annotated
from app.db.session import get_engine, get_conn
from fastapi import Depends

logger = getLogger(__name__)




def create_tables(engine: Engine) -> None:
    metadata.create_all(engine)
    logger.debug("Tables belonging to metadata has been created")


def _get_pair_id(conn: Connection, base: str, quote: str) -> int:

    stmt = pg_insert(pairs_table).values(base=base, quote=quote).on_conflict_do_update(
        constraint="uq_pairs",
        set_={
            "base": pairs_table.c.base,
            "quote": pairs_table.c.quote
        }
    ).returning(pairs_table.c.id)
    return int(conn.execute(stmt).scalar_one())
        
    
def _get_exchange_id(conn: Connection, name: str) -> int:

    stmt = pg_insert(exchanges_table).values(name=name).on_conflict_do_update(
        index_elements=["name"],
        set_={
            "name": exchanges_table.c.name
        }
    ).returning(exchanges_table.c.id)
    return int(conn.execute(stmt).scalar_one())
    

def _get_snapshot_id(conn: Connection, timestamp: datetime) -> int:

    stmt = pg_insert(snapshots_table).values(snapshot_time=timestamp).on_conflict_do_update(
        constraint="uq_snapshot",
        set_={
            "snapshot_time": snapshots_table.c.snapshot_time
        }
        ).returning(snapshots_table.c.id)
    return int(conn.execute(stmt).scalar_one())
    

def _insert_prices(conn: Connection, rows_with_ids: list[dict]) -> None:
    stmt = pg_insert(prices_table).values(rows_with_ids).on_conflict_do_nothing(constraint="uq_price_combination")
    conn.execute(stmt)

    
def _insert_errors(conn: Connection, error_type: str, message: str,
                   source: Literal["snapshot_insertion", "pair_insertion", "exchange_insertion", "price_insertion", "validation"],
                   snapshot_id: int | None = None, pair_id: int | None = None,
                   exchange_id: int | None = None) -> None:
    
    error_data = {
        "error_type": error_type,
        "message": message,
        "source": source,
        "snapshot_id": snapshot_id,
        "pair_id": pair_id,
        "exchange_id": exchange_id
    }

    stmt = pg_insert(errors_table).values(error_data)

    try:
        res = conn.execute(stmt)
        logger.debug("Error was successfully inserted into a table")
    except SQLAlchemyError:
        logger.exception("Error appeared during inserting error to a corresponding table")
        return None 
    

def save_snapshot(conn: Annotated[Connection, Depends(get_conn)], records: list[dict], timestamp: datetime) -> dict[str, int] | None:
    
    pairs_cache: dict[tuple[str,str], int | None] = {}
    exchange_cache: dict[str, int | None] = {}
    rows_with_ids: list[dict] = []

    try:
        snapshot_id = _get_snapshot_id(conn, timestamp=timestamp)
    except SQLAlchemyError as e:
        _insert_errors(conn, error_type=type(e).__name__, message=str(e), source="snapshot_insertion")
        logger.exception("Failed to insert snapshot, error inserted into 'error_table'")
        return None
    
    for record in records:
        if any(v is None for v in record.values()):
            missing = [k for k, v in record.items() if v is None]
            message = f"Missing {" ".join(missing)} from record: {record}"
            _insert_errors(conn, error_type="MissingField", message=message, source="validation")
            continue

        base = record["base"].upper().strip()
        quote = record["quote"].upper().strip()
        exchange = record["stock_exchange"].strip().lower()
        price = Decimal(str(record["price"]))
        logger.debug("Initializing base:%s\nquote:%s\nexchange:%s", base, quote, exchange)

        # Getting pair id, if pair has already been presented, take the value from pair_cache
        if (base, quote) not in pairs_cache:
            try:
                pair_id = _get_pair_id(conn, base, quote)
                pairs_cache[base,quote] = pair_id
            except SQLAlchemyError as e:
                _insert_errors(conn, error_type=type(e).__name__, message=str(e), source="pair_insertion", snapshot_id=snapshot_id)
                logger.exception("Failed to insert pair, error inserted into 'error_table'")
                continue
        else:
            pair_id = pairs_cache[base,quote]
        
        # Getting exchange id, if this exchange already has been met take its name from cache
        if exchange not in exchange_cache:
            try:
                exchange_id = _get_exchange_id(conn, exchange)
                exchange_cache[exchange] = exchange_id
            except SQLAlchemyError as e:
                _insert_errors(conn, error_type=type(e).__name__, message=str(e), source="exchange_insertion",
                                snapshot_id=snapshot_id, pair_id=pair_id)
                logger.exception("Failed to insert exchange, error inserted into 'error_table'")
                continue
        else:
            exchange_id = exchange_cache[exchange]

        row_with_id = {
            "snapshot_id": snapshot_id,
            "pair_id": pair_id,
            "exchange_id": exchange_id,
            "price": price
        }

        rows_with_ids.append(row_with_id)
    
    if not rows_with_ids:
        logger.warning("Rows with ids returned 0 rows")

    logger.info("Rows with ids variable for price insretion looking like this: %s", len(rows_with_ids))

    try:
        _insert_prices(conn, rows_with_ids=rows_with_ids)
        return {"snapshot_id": snapshot_id,
                "rows_inserted": len(rows_with_ids)}
    except SQLAlchemyError as e:
        _insert_errors(conn, error_type=type(e).__name__, message=str(e), source="price_insertion",
                        snapshot_id=snapshot_id)
        logger.exception("Failed to insert prices with timestamp, error inserted into 'error_table'")
        return None
    
