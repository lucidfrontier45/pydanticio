from typing import BinaryIO

import tomlkit
from pydantic import BaseModel

from ..utils import managed_text_io


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    # Use newline='\n' to normalize to LF when reading textual formats
    with managed_text_io(reader, encoding="utf-8", newline="") as text_reader:
        data = tomlkit.load(text_reader)
        return model.model_validate(data)


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    # Use newline='\n' so output uses LF line endings regardless of platform
    with managed_text_io(writer, encoding="utf-8", newline="") as text_writer:
        tomlkit.dump(record.model_dump(mode="json"), text_writer)
