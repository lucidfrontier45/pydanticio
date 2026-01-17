from typing import BinaryIO

import cbor2
from pydantic import BaseModel


def read_record[T: BaseModel](reader: BinaryIO, model: type[T]) -> T:
    data = reader.read()
    unpacked = cbor2.loads(data)
    return model.model_validate(unpacked)


def write_record(writer: BinaryIO, record: BaseModel) -> None:
    data = cbor2.dumps(record.model_dump(mode="json"), canonical=True)
    writer.write(data)  # type: ignore


def read_records[T: BaseModel](reader: BinaryIO, model: type[T]) -> list[T]:
    data = reader.read()
    unpacked = cbor2.loads(data)
    return [model.model_validate(item) for item in unpacked]


def write_records[T: BaseModel](writer: BinaryIO, records: list[T]) -> None:
    data = cbor2.dumps([record.model_dump(mode="json") for record in records], canonical=True)
    writer.write(data)  # type: ignore
