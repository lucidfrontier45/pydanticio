from typing import TextIO

from pydantic import BaseModel

from .common import T


def read_record(reader: TextIO, model: type[T]) -> T:
    raise NotImplementedError("yaml backend is not available.")


def write_record(writer: TextIO, record: BaseModel) -> None:
    raise NotImplementedError("yaml backend is not available.")
