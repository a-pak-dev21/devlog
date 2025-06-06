from pathlib import Path


def solution(folder_name):
    folder_path = Path(folder_name)
    files = [file.name for file in folder_path.glob("*txt") if "Python" in file.read_text().lower()]
    return files

