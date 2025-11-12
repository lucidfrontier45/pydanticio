from collections.abc import Iterable
from typing import TextIO

from pydantic import BaseModel


def read_records[T: BaseModel](reader: TextIO, model: type[T]) -> list[T]:
    return [model.model_validate_json(line) for line in reader]


def write_records(writer: TextIO, records: Iterable[BaseModel]) -> None:
    for record in records:
        writer.write(record.model_dump_json())
        writer.write("\n")
