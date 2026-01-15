"""
Backend adapters to wrap existing functions into protocol-compliant classes.
"""

from collections.abc import Iterable
from typing import BinaryIO

from pydantic import BaseModel, RootModel


class SingleRecordAdapter:
    """Adapter for backends that only support single records."""

    def __init__(self, read_func, write_func):
        self._read_record = read_func
        self._write_record = write_func

    def read_record(self, reader: BinaryIO, model: type[BaseModel]) -> BaseModel:
        return self._read_record(reader, model)

    def write_record(self, writer: BinaryIO, record: BaseModel) -> None:
        self._write_record(writer, record)

    def read_records(self, reader: BinaryIO, model: type[BaseModel]) -> list[BaseModel]:
        raise NotImplementedError(
            "This backend only supports single record operations. "
            "Use read_record() instead of read_records()."
        )

    def write_records(self, writer: BinaryIO, records: Iterable[BaseModel]) -> None:
        raise NotImplementedError(
            "This backend only supports single record operations. "
            "Use write_record() instead of write_records()."
        )


class ListFormatAdapter:
    """Adapter for backends that work with RootModel for lists."""

    def __init__(self, read_func, write_func):
        self._read_record = read_func
        self._write_record = write_func

    def read_record(self, reader: BinaryIO, model: type[BaseModel]) -> BaseModel:
        return self._read_record(reader, model)

    def write_record(self, writer: BinaryIO, record: BaseModel) -> None:
        self._write_record(writer, record)

    def read_records(self, reader: BinaryIO, model: type[BaseModel]) -> list[BaseModel]:
        list_model = RootModel[list[model]]
        return self._read_record(reader, list_model).root

    def write_records(self, writer: BinaryIO, records: Iterable[BaseModel]) -> None:
        # Convert to list for RootModel
        records_list = list(records)
        if not records_list:
            return  # Don't write empty lists

        list_model = RootModel[list[type(records_list[0])]]
        wrapped_records = list_model(root=records_list)
        self._write_record(writer, wrapped_records)
