from typing import Annotated

sample: Annotated[str, "first letter is capital"] = "john"

print(type(sample))
