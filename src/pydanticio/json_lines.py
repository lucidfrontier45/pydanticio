from collections.abc import Iterable
from typing import TextIO

from .common import T


def read_records_from_reader(reader: TextIO, model: type[T]) -> list[T]:
    return [model.model_validate_json(line) for line in reader]


def write_records_to_writer(writer: TextIO, records: Iterable[T]) -> None:
    for record in records:
        writer.write(record.model_dump_json() + "\n")
