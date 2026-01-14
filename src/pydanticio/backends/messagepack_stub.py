from typing import BinaryIO

from pydantic import BaseModel


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    raise NotImplementedError("messagepack backend is not available.")


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    raise NotImplementedError("messagepack backend is not available.")


def read_records[T: BaseModel](reader: BinaryIO, model: type[T]) -> list[T]:
    raise NotImplementedError("messagepack backend is not available.")


def write_records[T: BaseModel](writer: BinaryIO, records: list[T]) -> None:
    raise NotImplementedError("messagepack backend is not available.")
