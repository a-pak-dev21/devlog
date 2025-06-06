# TODO: We need a function that can transform a string into a
# number. What ways of achieving this do you know?

def string_to_number(s: str):
    try:
        return int(s)
    except ValueError:
        return "Can't be transformed into a number!"
