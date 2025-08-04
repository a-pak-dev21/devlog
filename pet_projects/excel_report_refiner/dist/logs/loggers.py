import logging
from pathlib import Path


log_dir = Path(__file__).resolve().parent / "missing_countries.log"
print(log_dir)
countries_logger = logging.getLogger("missing_countries")
countries_logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(name)s - %(message)s", datefmt="%d.%m.%Y %H:%M:%S")

file_handler = logging.FileHandler(log_dir)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

countries_logger.addHandler(file_handler)

