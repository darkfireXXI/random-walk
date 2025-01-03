import csv
from datetime import UTC, datetime
from uuid import UUID


def aware_utcnow():
    return datetime.now(UTC)


def naive_utcnow():
    return datetime.now(UTC).replace(tzinfo=None)


def read_csv(file_path):
    with open(file_path, "r") as file:
        data = csv.reader(file, delimiter=",")
        data = [row for row in data]
    return data


def write_csv(file_path, data):
    with open(file_path, "w") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def custom_dict_factory(dictionary):
    result = {}
    for key, value in dictionary:
        if isinstance(value, UUID):
            result[key] = str(value)
        elif isinstance(value, datetime):
            # I find str more readable that .isoformat()
            result[key] = str(value)
        else:
            result[key] = value
    return result
