# File completely made for data analysis of 
# data received from csv
# Mainly analysed by using pandas module

import pandas as pd
from typing import Any
from pathlib import Path
from app.settings import BASE_DIR
import json
from sqlalchemy import Engine, select, literal
from logging import getLogger
from app.db.db import make_engine
from app.db.models import pairs_table, exchanges_table, prices_table, snapshots_table, errors_table

logger = getLogger(__name__)

def load_from_csv(csv_file: Path = BASE_DIR / 'prices.csv') -> pd.DataFrame | None:
    if not csv_file.exists():
        logger.error("CSV file %s isn't existing", csv_file)
        return None
    elif csv_file.stat().st_size == 0:
        logger.warning("CSV file %s is empty", csv_file)
        return pd.DataFrame()

    df = pd.read_csv(csv_file, sep=",", header=0)
    
    logger.debug("The origin version of df is:\n%s", df)

    # Transform str-type timestamp into pandas.timestamp object
    df['timestamp'] = pd.to_datetime(df['timestamp']) # , format="%Y.%m.%d - %H:%M:%S"

    # rounding column price
    df['price'] = df['price'].round(2)

    # Adding 2 columns base & quote for easier readability and better output
    df[['base', "quote"]] = df['pair'].str.split("-", n=1, expand=True)

    # Sort all columns in a right order
    right_order = ["timestamp","pair","base","quote","stock_exchange","price"]
    df = df[right_order]

    logger.debug("\n%s",df)
    return df


def load_from_db(engine: Engine) -> pd.DataFrame:

    pair_expr = (pairs_table.c.base + literal("-") + pairs_table.c.quote).label("pair")
    stmt = select(
        snapshots_table.c.snapshot_time, pair_expr, pairs_table.c.base,
        pairs_table.c.quote, exchanges_table.c.name,
        prices_table.c.price
        ).select_from(prices_table).join(
        pairs_table, prices_table.c.pair_id == pairs_table.c.id
        ).join(
            snapshots_table, prices_table.c.snapshot_id == snapshots_table.c.id
        ).join(
            exchanges_table, prices_table.c.exchange_id == exchanges_table.c.id
        )
    
    with engine.begin() as conn:
        df = pd.read_sql(stmt, conn)      
        ts = pd.to_datetime(df["snapshot_time"])
        df["snapshot_time"] = ts.dt.strftime("%Y-%m-%d %H:%M:%S")
        df = df.rename(columns={"snapshot_time": "timestamp", "name": "stock_exchange"})
        logger.debug("My dataframe is %s", df)
    return df


def get_latest_snapshot(df: pd.DataFrame | None, since: pd.Timestamp | None = None,
                        base: str | None = None, quote: str | None = None,
                        exchange: str | None = None) -> pd.DataFrame | None:
    if df is None:
        logger.error("Received None instead of DataFrame, cannot get latest snapshot")
        return None
    
    latest_snapshot = df.sort_values(by=["timestamp", "pair"], axis=0, ascending=False)
    latest_snapshot = latest_snapshot.drop_duplicates(["pair", "stock_exchange"], keep="first")

    if since is not None:
        latest_snapshot["timestamp"] = pd.to_datetime(latest_snapshot["timestamp"])
        latest_snapshot = latest_snapshot[latest_snapshot["timestamp"] >= since]
    
    if (base is not None) and (quote is not None):
        base, quote = base.upper().strip(), quote.upper().strip()
        latest_snapshot = latest_snapshot[(latest_snapshot["base"] == base) & (latest_snapshot["quote"] == quote)]
    elif base is not None:
        latest_snapshot = latest_snapshot[latest_snapshot["base"] == base.upper()]
    elif quote is not None:
        latest_snapshot = latest_snapshot[latest_snapshot["quote"] == quote.upper()]

    if exchange is not None:
        exchange = exchange.lower().strip()
        latest_snapshot = latest_snapshot[latest_snapshot["stock_exchange"] == exchange]
    
    if latest_snapshot.empty:
        logger.warning("Latest snapshot is empty after applying all filters")

    logger.debug("\n%s", latest_snapshot)
    return latest_snapshot


def get_pair_history(df: pd.DataFrame | None, base: str, quote: str,
                     exchange: str | list[str] | None = None, start: pd.Timestamp | None = None,
                     end: pd.Timestamp | None = None) -> pd.DataFrame| None:
    
    if df is None:
        logger.error("Received None instead of DataFrame, cannot get history")
        return None
    
    base, quote = base.upper(), quote.upper()
    pair_history = df.copy()

    if exchange is not None and isinstance(exchange, str):
        pair_history = pair_history[pair_history['stock_exchange'] == exchange]
    elif exchange is not None and isinstance(exchange, list):
        pair_history = pair_history[pair_history['stock_exchange'].isin(exchange)]
    

    if (start is not None) and (end is not None):
        pair_history = pair_history[(pair_history['timestamp'] >= start) & (pair_history['timestamp'] <= end)]
    elif start is not None:
        pair_history = pair_history[pair_history['timestamp'] >= start]
    elif end is not None:
        pair_history = pair_history[pair_history['timestamp'] <= end]

    pair_history = pair_history[(pair_history['base'] == base) & (pair_history['quote'] == quote)]
    if pair_history.empty:
        logger.warning("History for pair %s-%s is empty", base, quote)
        return pair_history
    pair_history = pair_history.sort_values('timestamp', axis=0, ascending=False)
    logger.debug("History for pair %s-%s:\n%s", base, quote, pair_history)
    
    return pair_history
    

def _get_pair_comparison_table(filtered_df: pd.DataFrame | None, clients: list[str] | None = None):

    if filtered_df is None or filtered_df.empty:
        logger.error("Function get_pair_history returned None or empty DataFrame")
        return filtered_df
    
    pivot_df = filtered_df.pivot(columns='stock_exchange', index='timestamp', values='price')
    
    if clients is None:
        client_cols = pivot_df.columns.to_list()
    else:
        client_cols = [client for client in clients if client in pivot_df.columns]
        missing_clients = list(set(clients) - set(pivot_df.columns))
        logger.warning("Clients which are missing in pivot df and hasn't been debugged: %s", missing_clients)
    logger.debug("Names of all current clients: %s", client_cols)

    if len(client_cols) < 2:
        logger.error("We can't compare anything, since only 1 client has been given or returned")
        return pivot_df
    
    pivot_df['price_difference'] = pivot_df[client_cols].max(axis=1) - pivot_df[client_cols].min(axis=1)
    pivot_df["better_buy_on"] = pivot_df[client_cols].idxmin(axis=1)
    equal_price_mask = pivot_df['price_difference'] == 0
    pivot_df.loc[equal_price_mask, 'better_buy_on'] = 'Both'
    pivot_df = pivot_df.sort_index(axis=0, inplace=False, ascending=False)
    logger.debug("Function get_pair_comparison_table, final table which returned:\n%s", pivot_df)

    return pivot_df



def get_pair_comparison_table(df: pd.DataFrame | None, base: str, quote: str,
                              exchange: str | list[str] | None = None, start: pd.Timestamp | None = None,
                              end: pd.Timestamp | None = None) -> pd.DataFrame | None:
    
    only_by_pair = get_pair_history(df, base, quote, exchange, start, end)
    logger.debug("Function get_pair_comparison_table, sorted by specific pair:\n%s", only_by_pair)

    pivot_df = _get_pair_comparison_table(only_by_pair)

    return pivot_df


def get_pair_stats(df: pd.DataFrame | None, base: str, quote: str,
                   exchange: str| list[str] | None = None,
                   start: pd.Timestamp | None = None,
                   end: pd.Timestamp | None = None):
    stats = {}
    only_by_pair = get_pair_history(df, base, quote, exchange=exchange, start=start, end=end)
    logger.debug("Function get_pair_stats filtered by pair %s-%s:\n%s", base, quote, only_by_pair)

    if only_by_pair is None or only_by_pair.empty:
        logger.error("Function get_pair_history returned None or empty DataFrame")
        return only_by_pair
    
    meta = {}
    meta["pair"] = f"{base.upper()}-{quote.upper()}"
    meta["stock_exchanges"] = only_by_pair["stock_exchange"].unique().tolist()
    meta["total_logs"] = len(only_by_pair)

    stats["meta"] = meta

    time_stats = {}
    time_stats["first_timestamp"] = str(pd.to_datetime(only_by_pair['timestamp']).min())
    time_stats["last_timestamp"] = str(pd.to_datetime(only_by_pair['timestamp']).max())
    time_stats["period_length"] = str(pd.to_datetime(only_by_pair['timestamp']).max() - pd.to_datetime(only_by_pair['timestamp']).min())

    stats['time_stats'] = time_stats

    price_stats = {}
    price_stats["lowest_price"] = float(only_by_pair["price"].min())
    price_stats["highest_price"] = float(only_by_pair["price"].max())
    price_stats["average_price"] = float(only_by_pair["price"].mean())
    price_stats["median_price"] = float(only_by_pair["price"].median())
    price_stats["price_range"] = round(price_stats["highest_price"] - price_stats["lowest_price"], 3)
    try:
        price_stats["price_percent_range"] = round((price_stats["price_range"] / price_stats["average_price"]) * 100, 3)
    except ZeroDivisionError:
        logger.error("average_price is equal to zero, we can not divide to zero")
        return None
    price_stats["std_deviation"] = round(float(only_by_pair["price"].std()), 3) # return standard deviation from mean price

    stats["price_stats"] = price_stats

    spread_stats = {}
    pivot_df = _get_pair_comparison_table(only_by_pair)
    if pivot_df is None or pivot_df.empty:
        logger.error("Function get_pair_comparison_table returned None or empty DataFrame")
        return pivot_df
    logger.debug("\nPivot DataFrame for our pair is:\n%s", pivot_df)
    spread_stats["average_spread"] = round(float(pivot_df["price_difference"].mean()),2)
    max_spread = pivot_df[pivot_df["price_difference"] == pivot_df["price_difference"].max()]
    #max_spread = pivot_df.idxmax()
    logger.info("MAX SPREAD IS: %s", max_spread)
    logger.debug("\n%s", max_spread)
    spread_stats["max_price_spread"] = round(float(max_spread['price_difference'].iloc[0]),2)
    spread_stats["max_spread_timestamp"] = pd.to_datetime(max_spread.index, errors="coerce").strftime("%Y-%m-%d %H:%M:%S").tolist()

    stats["spread_stats"] = spread_stats

    grouped_by_exchange = only_by_pair.groupby("stock_exchange")["price"].agg(
        min_price="min",
        max_price="max",
        mean_price="mean",
        median_price="median",
        price_deviation="std"
        ).round(2)
    
    grouped_by_exchange = grouped_by_exchange.to_dict("index") #type: ignore
    
    stats["by_exchange"] = grouped_by_exchange
    logger.debug(stats)
    logger.debug(json.dumps(stats, indent=4))

    return stats




if __name__ == "__main__":
    #load_from_csv()
    engine = make_engine()
    my_df = load_from_db(engine)
    print(my_df)
    since = pd.Timestamp("2026-01-05 23:41:24")
    print(get_latest_snapshot(my_df, since=since, exchange='Coinbase.com', base="btc", quote="usdt"))
    # get_pair_history(my_df, "eth","usdt")
    # get_pair_comparison_table(my_df, 'eth', 'usdt')
    # get_pair_stats(my_df, 'eth', 'usdt')

