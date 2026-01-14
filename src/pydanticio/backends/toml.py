from typing import BinaryIO

import tomlkit
from pydantic import BaseModel

from ..utils import PLATFORM_NEWLINE, managed_text_io


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    with managed_text_io(reader, encoding="utf-8") as text_reader:
        data = tomlkit.load(text_reader)
        return model.model_validate(data)


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    # Use platform-specific newline to ensure compatibility
    with managed_text_io(writer, encoding="utf-8", newline=PLATFORM_NEWLINE) as text_writer:
        tomlkit.dump(record.model_dump(mode="json"), text_writer)
