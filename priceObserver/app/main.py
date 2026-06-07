'''
Project which in the end will ask for a product name
and will search for this product on 2 or more different webs
to compare its price afterwards will save results to a 
connected database and will analyze dynamic in changes
and compare side by side same product from different webs
'''
from logging import getLogger
import csv
from pathlib import Path
from datetime import datetime
from app.settings import BASE_DIR
from app.logging_config import root_logger_config
from pwdlib import PasswordHash


logger = getLogger()
    
def import_to_csv(records: list[dict] | None, filename: Path | str = BASE_DIR / 'artifacts/prices.csv'):
    if not records:
        logger.warning("Not received any data to save at CSV")
        return None
    
    file_path = Path(filename)
    file_exists = file_path.exists()
    file_empty = file_exists and file_path.stat().st_size == 0

    with file_path.open('a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if (not file_exists) or file_empty:
            header = list(records[0].keys())
            header.append('timestamp')
            writer.writerow(header)
        for record in records:
            record['timestamp'] = datetime.now().replace(microsecond=0)
            writer.writerow(list(record.values()))

    logger.info("Saved %d records into %s", len(records), file_path)
