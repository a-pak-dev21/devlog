from pathlib import Path


def solution(file_name):
    file_path = Path(file_name)
    if not file_path.exists():
        file_path.write_text("This is a test note.", encoding="utf-8")

    return file_path.read_text()
