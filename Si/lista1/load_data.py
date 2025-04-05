import csv
import numpy as np


def load_data(file_path) -> list[list[str]]:
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
    return data


def remove_duplicates(data: list[list[str]]) -> list[list[str]]:
    unique_rows = []
    seen = set()

    for row in data:
        row_tuple = tuple(row)
        if row_tuple[1:] not in seen:
            seen.add(row_tuple[1:])
            unique_rows.append(row)

    return unique_rows


if __name__ == "__main__":

    data = load_data("./connection_graph.csv")
    print(len(data))
    data = remove_duplicates(data)
    print(len(data))
    # np.savetxt('./test_graph.csv', data[:100_000], delimiter=',', fmt='%s')
