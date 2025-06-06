from pathlib import Path

# Task: script which will:
#   looking for all .log files in /logs folder
#   move them into logs/archived/, if it's not exist, create it
#   rename each file by adding suffix "_archived"
#   ex: server.log --> server_archived.log


def solution() -> None:
    logs_dir = Path("logs")
    archived_dir = logs_dir / "archived"
    archived_dir.mkdir(exist_ok=True)

    for log_file in logs_dir.glob("*.log"):
        new_name = log_file.stem + "_archived" + log_file.suffix
        archived_file_dir = archived_dir / new_name
        log_file.rename(archived_file_dir)


