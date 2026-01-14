from typing import BinaryIO

import yaml
from pydantic import BaseModel

from ..utils import managed_text_io


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    with managed_text_io(reader, encoding="utf-8", newline="\n") as text_reader:
        data = yaml.safe_load(text_reader)
        return model.model_validate(data)


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    with managed_text_io(writer, encoding="utf-8", newline="\n") as text_writer:
        yaml.safe_dump(record.model_dump(mode="json"), text_writer, line_break="\n")
