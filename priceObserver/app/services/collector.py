from logging import getLogger
from datetime import datetime, timezone
from app.clients.all_clients_register import get_clients
from app.clients.base_client import BaseClient

logger = getLogger(__name__)

def clients_price(base: str, quote: str, clients: list[BaseClient] | None = None) -> list[dict] | None:
        
    if clients is None:
        clients = get_clients()
    clients_prices = []

    for client in clients:
        price = client.define_price(base, quote)
        if price is not None:
            clients_prices.append(price)
        else:
            logger.warning("%s client returned None for pair %s-%s",
                           client.name, base, quote)
    if not clients_prices:
        logger.warning("All clients returned None for pair %s-%s", base, quote)
        return None
    
    return clients_prices


def clients_prices(pairs: list[tuple[str, str]], clients: list[BaseClient] | None = None) -> list[dict] | None:
    if any(map(lambda x: len(x) != 2, pairs)):
        logger.error("All pairs given as (base, quote) tuples sohuld contain only 2 elements")
        return None
    
    all_prices = []

    for base, quote in pairs:
        pair_prices = clients_price(base, quote, clients=clients)
        if pair_prices:
            all_prices.extend(pair_prices)
    
    if not all_prices:
        return None
    
    return all_prices


def run_snapshot(pairs: list[tuple[str, str]],
                 clients: list[BaseClient] | None = None) -> tuple[list[dict], datetime] | None:
    snapshot_t = datetime.now(timezone.utc).replace(microsecond=0)
    records = clients_prices(pairs=pairs, clients=clients)
    if records is None:
        return None

    return records, snapshot_t