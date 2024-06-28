from collections.abc import Iterable
from typing import TextIO

from pydantic import BaseModel, RootModel

from .common import T


def read_record_from_reader(reader: TextIO, model: type[T]) -> T:
    data = reader.read()
    return model.model_validate_json(data)


def read_records_from_reader(reader: TextIO, model: type[T]) -> list[T]:
    list_of_model = RootModel[list[model]]
    return read_record_from_reader(reader, list_of_model).root


def write_record_to_writer(writer: TextIO, record: BaseModel) -> None:
    writer.write(record.model_dump_json())


def write_records_to_writer(writer: TextIO, records: Iterable[T]) -> None:
    list_of_model = RootModel[Iterable[T]]
    record = list_of_model(root=records)
    write_record_to_writer(writer, record)
