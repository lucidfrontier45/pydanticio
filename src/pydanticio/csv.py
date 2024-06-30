import csv
from collections.abc import Iterable
from typing import TextIO

from .common import T


def read_records(reader: TextIO, model: type[T]) -> list[T]:
    csv_reader = csv.DictReader(reader)
    return [model.model_validate(row) for row in csv_reader]


def write_records(writer: TextIO, records: Iterable[T]) -> None:
    it = iter(records)
    first_record = next(it)
    fields = list(first_record.model_fields.keys())
    csv_writer = csv.DictWriter(writer, fieldnames=fields)
    csv_writer.writeheader()
    csv_writer.writerow(first_record.model_dump(mode="json"))
    for record in it:
        csv_writer.writerow(record.model_dump(mode="json"))
