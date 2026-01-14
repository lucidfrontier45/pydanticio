from typing import TextIO

import tomlkit
from pydantic import BaseModel


def read_record[T: BaseModel](reader: TextIO, model: type[T]) -> T:
    data = tomlkit.load(reader)
    return model.model_validate(data)


def write_record(writer: TextIO, record: BaseModel) -> None:
    tomlkit.dump(record.model_dump(mode="json"), writer)
