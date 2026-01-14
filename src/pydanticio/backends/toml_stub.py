from typing import TextIO

from pydantic import BaseModel


def read_record[T: BaseModel](reader: TextIO, model: type[T]) -> T:
    raise NotImplementedError("toml backend is not available.")


def write_record(writer: TextIO, record: BaseModel) -> None:
    raise NotImplementedError("toml backend is not available.")
