from collections.abc import Iterable
from typing import TextIO

from .common import T


def read(reader: TextIO, model: type[T]) -> list[T]:
    return [model.model_validate_json(line) for line in reader]


def write(writer: TextIO, records: Iterable[T]) -> None:
    for record in records:
        writer.write(record.model_dump_json())
        writer.write("\n")
