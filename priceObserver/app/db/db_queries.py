# придумать функции которые будут реализованы в виде SQL запросов для взятия какого-то примитивного вида данных
# в analysis.py уже реализована только история по паре и то как вспомогательная функция так-что можно практически все

from app.db.models import pairs_table, exchanges_table, prices_table, snapshots_table, errors_table
from sqlalchemy import select, Select, func, Connection
from datetime import datetime
from logging import getLogger
from typing import Literal
from app.api.dto import PaginationDTO, PairFiltersDTO


logger = getLogger(__name__)

pagination_map: dict = {
    "time": snapshots_table.c.snapshot_time,
    "exchange": exchanges_table.c.name,
    "price": prices_table.c.price,
    "pair": func.concat(pairs_table.c.base,"-",pairs_table.c.quote)
}

sort_dir_map: dict = {
    "desc": lambda expression: expression.desc(),
    "asc": lambda expression: expression.asc()
}

def all_columns() -> tuple:
    return (
        snapshots_table.c.snapshot_time.label("time"),
        func.concat(pairs_table.c.base,"-",pairs_table.c.quote).label("pair"),
        pairs_table.c.base,
        pairs_table.c.quote,
        exchanges_table.c.name.label("exchange"),
        prices_table.c.price
        )


def launcher(conn: Connection, stmt: Select, mode: Literal["mappings", "scalars", "rows"] = "mappings"):
    
    if mode == "mappings":
        return conn.execute(stmt).mappings().all()
    elif mode == "scalars":
        return conn.execute(stmt).scalars().all()
    elif mode == "rows":
        return conn.execute(stmt).all()


def _join_builder():

    stmt = prices_table.join(
            snapshots_table, snapshots_table.c.id == prices_table.c.snapshot_id
        ).join(
            pairs_table, pairs_table.c.id == prices_table.c.pair_id
        ).join(
            exchanges_table, exchanges_table.c.id == prices_table.c.exchange_id
        )
    
    return stmt


def _apply_filters(stmt: Select,
                   filters: PairFiltersDTO):
    
    if filters.start and filters.end:
        stmt = stmt.where(snapshots_table.c.snapshot_time >= filters.start,
                          snapshots_table.c.snapshot_time <= filters.end)
    elif filters.start:
        stmt = stmt.where(snapshots_table.c.snapshot_time >= filters.start)
    elif filters.end:
        stmt = stmt.where(snapshots_table.c.snapshot_time <= filters.end)

    if filters.base and filters.quote:
        base = filters.base.upper().strip()
        quote = filters.quote.upper().strip()
        stmt = stmt.where(pairs_table.c.base == base,
                          pairs_table.c.quote == quote)
        
    if filters.exchange:
        exchange = filters.exchange.lower().strip()
        stmt = stmt.where(exchanges_table.c.name == exchange)
    
    return stmt


def _pagination_filter(stmt: Select,
                       pagination: PaginationDTO                       
                       ):
    
    col_to_order = pagination_map[pagination.order_by]

    stmt = stmt.order_by(
        sort_dir_map[pagination.sort_dir](col_to_order)
        ).limit(pagination.limit).offset(pagination.offset)

    return stmt
    

def get_all_pairs(conn: Connection, limit: int, offset: int):
    stmt = select(pairs_table.c.base,
                  pairs_table.c.quote,
                  func.concat(pairs_table.c.base, "-", pairs_table.c.quote).label("pair")
                  ).select_from(pairs_table).limit(limit).offset(offset)
    
    return launcher(conn, stmt)


def get_all_exchanges(conn: Connection):
    stmt = select(exchanges_table.c.name.label("name")).select_from(exchanges_table)

    return launcher(conn, stmt, mode="scalars")


def db_health_check(conn: Connection):
    try:
        launcher(conn, select(1))
        return True
    except:
        return False


def get_latest_snapshot(conn: Connection):
    subquery = select(func.max(snapshots_table.c.id)).select_from(snapshots_table).scalar_subquery()
    stmt = select(
        *all_columns()
    ).select_from(_join_builder()).where(snapshots_table.c.id == subquery)
        
    return launcher(conn, stmt)


def get_all_prices(conn: Connection, filters: PairFiltersDTO):
    
    stmt = select(prices_table.c.price).select_from(_join_builder())
   
    stmt = _apply_filters(stmt, filters)
    
    return launcher(conn, stmt, "scalars")


def get_snapshot(conn: Connection, snapshot_id: int | None = None, snapshot_time: datetime | None = None):

    if snapshot_id is not None and snapshot_time is not None:
        logger.error("You have to get snapshot either by id or by time not both together")
        return None
    elif snapshot_id:
        stmt = select(
            *all_columns()
        ).select_from(_join_builder()).where(snapshots_table.c.id == snapshot_id)
    elif snapshot_time:
        stmt = select(
            *all_columns()
        ).select_from(_join_builder()).where(snapshots_table.c.snapshot_time == snapshot_time)
    else:
        logger.error("Either snapshot_id or snapshot_time have to be initialized")
        return None
    
    return launcher(conn, stmt)


def get_pair_timeseries(conn: Connection,
                        pagination: PaginationDTO,
                        filters: PairFiltersDTO):
    stmt = select(
        *all_columns()
    ).select_from(_join_builder())

    stmt = _apply_filters(stmt, filters)

    stmt = _pagination_filter(stmt, pagination)

    return launcher(conn, stmt)


def get_snapshot_spreads(conn: Connection, snapshot_id: int):
    # должна для каждого снепшота возввращать минимальную цену, максимальную цену, спред цен(макс - мин), 
    # спред в проценте, best_buy_on, best_sell_on(name of stock exchange)
    ranked = (select(
        *all_columns(),
        func.row_number().over(
            partition_by=(snapshots_table.c.id, pairs_table.c.id),
            order_by=prices_table.c.price.asc()
        ).label("rn_min"),
        func.row_number().over(
            partition_by=(snapshots_table.c.id, pairs_table.c.id),
            order_by=prices_table.c.price.desc()
        ).label("rn_max")
        ).select_from(_join_builder()).where(snapshots_table.c.id == snapshot_id)
    ).cte("ranked")

    min_price = func.min(ranked.c.price).label("lowest_price")
    max_price = func.max(ranked.c.price).label("highest_price")

    stmt = select(
        ranked.c.time,
        ranked.c.pair,
        min_price,
        max_price,
        (max_price - min_price).label("abs_spread"),
        func.round(((max_price - min_price) / min_price * 100), 2).label("pct_spread"),
        func.max(ranked.c.exchange).filter(ranked.c.rn_min == 1).label("best_buy_on"),
        func.max(ranked.c.exchange).filter(ranked.c.rn_max == 1).label("best_sell_on")
    ).select_from(ranked).group_by(ranked.c.time, ranked.c.pair)

    return launcher(conn, stmt)


def get_errors(conn: Connection, mode: Literal["all", "missing_fields"] = 'all'):
    stmt = select(errors_table)
    if mode == "missing_fields":
        stmt = stmt.where(errors_table.c.source == "validation")
    
    return launcher(conn, stmt)

