from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Literal, TextIO, TypeAlias

from pydantic import BaseModel, RootModel

from . import csv as csv_backend
from . import json as json_backend
from . import json_lines as jsl_backend
from .common import T
from .version import __version__

GenericBackendType = Literal["json"]
LinesOnlyBackendType = Literal["csv", "json_lines"]


def _decide_backend_type_from_path(
    file_path: Path,
) -> GenericBackendType | LinesOnlyBackendType:
    match file_path.suffix.lower():
        case ".csv":
            return "csv"
        case ".jsonl" | ".jsl" | ".jl" | ".json_lines":
            return "json_lines"
        case ".json":
            return "json"
        case _:
            raise ValueError(f"Unsupported file extension: {file_path.suffix}")


def read_record_from_reader(
    reader: TextIO, model: type[T], backend_type: GenericBackendType
) -> T:
    match backend_type:
        case "json":
            return json_backend.read_record(reader, model)
        case _:
            raise ValueError(f"Unsupported backend type: {backend_type}")


def read_record_from_file(file_path: str | Path, model: type[T]) -> T:
    file_path = Path(file_path)
    backend_type: GenericBackendType = _decide_backend_type_from_path(file_path)  # type: ignore
    with file_path.open() as reader:
        return read_record_from_reader(reader, model, backend_type)


def read_records_from_reader(
    reader: TextIO,
    model: type[T],
    backend_type: LinesOnlyBackendType | GenericBackendType,
) -> list[T]:
    list_model = RootModel[list[model]]
    match backend_type:
        case "csv":
            return csv_backend.read_records(reader, model)
        case "json_lines":
            return jsl_backend.read_records(reader, model)
        case "json":
            return json_backend.read_record(reader, list_model).root
        case _:
            raise ValueError(f"Unsupported backend type: {backend_type}")


def read_records_from_file(file_path: str | Path, model: type[T]) -> list[T]:
    file_path = Path(file_path)
    backend_type = _decide_backend_type_from_path(file_path)
    with file_path.open() as reader:
        return read_records_from_reader(reader, model, backend_type)


def write_record_to_writer(
    writer: TextIO, record: BaseModel, backend_type: GenericBackendType
) -> None:
    match backend_type:
        case "json":
            json_backend.write_record(writer, record)
        case _:
            raise ValueError(f"Unsupported backend type: {backend_type}")


def write_record_to_file(file_path: str | Path, record: BaseModel) -> None:
    file_path = Path(file_path)
    backend_type: GenericBackendType = _decide_backend_type_from_path(file_path)  # type: ignore
    with file_path.open("w") as writer:
        write_record_to_writer(writer, record, backend_type)


def write_records_to_writer(
    writer: TextIO,
    records: Iterable[T],
    backend_type: LinesOnlyBackendType | GenericBackendType,
) -> None:
    list_model = RootModel[Iterable[T]]
    match backend_type:
        case "csv":
            csv_backend.write_records(writer, records)
        case "json_lines":
            jsl_backend.write_records(writer, records)
        case "json":
            json_backend.write_record(writer, list_model(root=records))
        case _:
            raise ValueError(f"Unsupported backend type: {backend_type}")


def write_records_to_file(file_path: str | Path, records: Iterable[T]) -> None:
    file_path = Path(file_path)
    backend_type = _decide_backend_type_from_path(file_path)
    with file_path.open("w") as writer:
        write_records_to_writer(writer, records, backend_type)
