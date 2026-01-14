from collections.abc import Iterable
from typing import BinaryIO

from pydantic import BaseModel

from ..utils import managed_text_io


def read_records[T: BaseModel](reader: BinaryIO, model: type[T]) -> list[T]:
    with managed_text_io(reader, encoding="utf-8") as text_reader:
        return [model.model_validate_json(line) for line in text_reader]


def write_records(writer: BinaryIO, records: Iterable[BaseModel]) -> None:
    with managed_text_io(writer, encoding="utf-8") as text_writer:
        for record in records:
            text_writer.write(record.model_dump_json())
            text_writer.write("\n")
