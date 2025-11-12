from typing import TextIO

from pydantic import BaseModel


def read_record[T: BaseModel](reader: TextIO, model: type[T]) -> T:
    data = reader.read()
    return model.model_validate_json(data)


def write_record(writer: TextIO, record: BaseModel) -> None:
    writer.write(record.model_dump_json())
