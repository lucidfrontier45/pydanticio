from typing import BinaryIO

import msgpack
from pydantic import BaseModel


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    data = reader.read()
    unpacked = msgpack.unpackb(data)
    return model.model_validate(unpacked)


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    data = msgpack.packb(record.model_dump())
    if data is not None:
        writer.write(data)


def read_records[T: BaseModel](reader: BinaryIO, model: type[T]) -> list[T]:
    data = reader.read()
    unpacked = msgpack.unpackb(data)
    return [model.model_validate(item) for item in unpacked]


def write_records[T: BaseModel](writer: BinaryIO, records: list[T]) -> None:
    data = msgpack.packb([record.model_dump() for record in records])
    if data is not None:
        writer.write(data)
