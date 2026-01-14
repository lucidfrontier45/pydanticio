from typing import BinaryIO

from pydantic import BaseModel

from ..utils import managed_text_io


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    with managed_text_io(reader, encoding="utf-8") as text_reader:
        data = text_reader.read()
        return model.model_validate_json(data)


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    with managed_text_io(writer, encoding="utf-8", newline="") as text_writer:
        text_writer.write(record.model_dump_json())
