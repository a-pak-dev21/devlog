import logging
from pathlib import Path
import sys


exercise_logger = logging.getLogger("exercises")
exercise_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s: %(message)s", datefmt="%d.%m.%Y %H:%M:%S"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)

log_folder_dir = Path(__file__).resolve().parent.parent / "logs"
log_folder_dir.mkdir(exist_ok=True)
logs_dir = log_folder_dir / "exercises.log"
file_handler = logging.FileHandler(logs_dir, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

exercise_logger.addHandler(console_handler)
exercise_logger.addHandler(file_handler)
exercise_logger.propagate = False
