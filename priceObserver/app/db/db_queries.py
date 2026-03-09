# придумать функции которые будут реализованы в виде SQL запросов для взятия какого-то примитивного вида данных
# в analysis.py уже реализована только история по паре и то как вспомогательная функция так-что можно практически все

from app.db.models import pairs_table, exchanges_table, prices_table, snapshots_table, errors_table
from app.db.db import make_engine
from sqlalchemy import select, Select, func, Sequence, RowMapping
from datetime import datetime
from logging import getLogger
from typing import Literal
import json
from decimal import Decimal

logger = getLogger(__name__)

engine = make_engine()

def all_columns() -> tuple:
    return (
        snapshots_table.c.snapshot_time.label("time"),
        func.concat(pairs_table.c.base,"-",pairs_table.c.quote).label("pair"),
        pairs_table.c.base,
        pairs_table.c.quote,
        exchanges_table.c.name.label("exchange"),
        prices_table.c.price
        )


def launcher(stmt: Select, mode: Literal["mappings", "scalars", "rows"] = "mappings"):
    with engine.connect() as conn:
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


def _apply_filters(stmt: Select, start: datetime | None = None, end: datetime | None = None,
                  base: str | None = None, quote: str | None = None,
                  exchange: str | None = None):
    
    if start and end:
        stmt = stmt.where(snapshots_table.c.snapshot_time >= start,
                          snapshots_table.c.snapshot_time <= end)
    elif start:
        stmt = stmt.where(snapshots_table.c.snapshot_time >= start)
    elif end:
        stmt = stmt.where(snapshots_table.c.snapshot_time <= end)

    if base and quote:
        base = base.upper().strip()
        quote = quote.upper().strip()
        stmt = stmt.where(pairs_table.c.base == base,
                          pairs_table.c.quote == quote)
        
    if exchange:
        exchange = exchange.lower().strip()
        stmt = stmt.where(exchanges_table.c.name == exchange)
    
    return stmt

def get_all_pairs():
    stmt = select(pairs_table.c.base,
                  pairs_table.c.quote,
                  func.concat(pairs_table.c.base, "-", pairs_table.c.quote).label("pair")
                  ).select_from(pairs_table)
    
    return launcher(stmt)


def get_all_exchanges():
    stmt = select(exchanges_table.c.name.label("exchange")).select_from(exchanges_table)

    return launcher(stmt, mode="scalars")


def db_health_check():
    try:
        launcher(select(1))
        return True
    except:
        return False


def get_latest_snapshot():
    subquery = select(func.max(snapshots_table.c.id)).select_from(snapshots_table).scalar_subquery()
    stmt = select(
        *all_columns()
    ).select_from(_join_builder()).where(snapshots_table.c.id == subquery)
        
    return launcher(stmt)


def get_all_prices(base: str | None = None, quote: str | None = None, exchange: str | None = None,
                   start: datetime | None = None, end: datetime | None = None):
    
    stmt = select(prices_table.c.price).select_from(_join_builder())
   
    stmt = _apply_filters(stmt, start=start, end=end,
                   base=base, quote=quote,
                   exchange=exchange)
    
    return launcher(stmt, "scalars")


def get_snapshot(snapshot_id: int | None = None, snapshot_time: datetime | None = None):

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
    
    return launcher(stmt)


def get_pair_timeseries(base: str, quote: str,
                        start: datetime | None = None, end: datetime | None = None,
                        exchange: str | None = None):
    stmt = select(
        *all_columns()
    ).select_from(_join_builder())

    stmt = _apply_filters(stmt, base=base, quote=quote, start=start, end=end, exchange=exchange)

    return launcher(stmt)


def get_snapshot_spreads(snapshot_id: int):
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

    return launcher(stmt)


def get_errors(mode: Literal["all", "missing_fields"] = 'all'):
    stmt = select(errors_table)
    if mode == "missing_fields":
        stmt = stmt.where(errors_table.c.source == "validation")
    
    return launcher(stmt)


if __name__ == '__main__':

    # test1 = get_latest_snapshot()
    # print(test1)
    
    # test2 = get_all_prices(base="btc", quote="usdt", exchange="Binance.com",
    #                        start=datetime(2026,2,8,0,0,0), end=datetime(2026,2,14,0,0,0))
    # print(test2)

    # test3 = get_snapshot(snapshot_time=datetime(2026,2,15,20,6,59))
    # for row in test3:
    #     print(row)

    # test4 = get_pair_timeseries("btc", "usdt", exchange="Coinbase.com")
    # print(len(test4))
    # for row in test4:
    #     print(row, "\n")

    test5 = get_snapshot_spreads(3)
    test_list = []
    for row in test5:
        d = dict(row)
        d["time"] = d["time"].strftime("%Y-%m-%d %H:%M:%S")
        for k,v in d.items():
            if isinstance(v, Decimal):
                d[k] = float(v)
        print(json.dumps(d, indent=2))

