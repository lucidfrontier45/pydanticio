from typing import BinaryIO

from pydantic import BaseModel


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    raise NotImplementedError("toml backend is not available.")


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    raise NotImplementedError("toml backend is not available.")
