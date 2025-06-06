# TODO: Script which will:
#   by launching, will create folder results/
#   ask for the user_name through input
#   save it into results/user.json
#   process it and return as "Hello, <name>!"

import json
import pathlib


def solution():
    pathlib.Path("results").mkdir(exist_ok=True)
    user_name: str = input("Enter your name: ")
    with open(Path("results") / "user_names.json", 'w') as f:
        json.dump(user_name, f)

    with open(Path("results") / "user_names.json", 'r') as r:
        data = json.load(r)

    return f"Hello {data}"

