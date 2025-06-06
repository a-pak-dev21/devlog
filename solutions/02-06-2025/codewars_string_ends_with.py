# TODO: Complete the solution so that it returns true if the first
#  argument(string) passed in ends with the 2nd argument
# (also a string).

def string_ends_with(text: str, ending: str):
    starting_point: int = len(text) - len(ending)
    return text[starting_point:] == ending
