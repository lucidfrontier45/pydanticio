from collections.abc import Iterable
from typing import BinaryIO

import msgpack
from pydantic import BaseModel

from ..registry import register_backend


@register_backend("messagepack", [".msgpack"])
class MessagePackBackend:
    def read_record(self, reader: BinaryIO, model: type[BaseModel]) -> BaseModel:
        data = reader.read()
        unpacked = msgpack.unpackb(data)
        return model.model_validate(unpacked)

    def write_record(self, writer: BinaryIO, record: BaseModel) -> None:
        data = msgpack.packb(record.model_dump())
        writer.write(data)  # type: ignore

    def read_records(self, reader: BinaryIO, model: type[BaseModel]) -> list[BaseModel]:
        data = reader.read()
        unpacked = msgpack.unpackb(data)
        return [model.model_validate(item) for item in unpacked]

    def write_records(self, writer: BinaryIO, records: Iterable[BaseModel]) -> None:
        records_list = list(records)
        data = msgpack.packb([record.model_dump() for record in records_list])
        writer.write(data)  # type: ignore
