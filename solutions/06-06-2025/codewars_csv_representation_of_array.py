# Create a function that returns the CSV representation of a two-dimensional numeric array.
import csv
import io


def solution(my_array: list[list[int]]):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(my_array)
    return output.getvalue()
