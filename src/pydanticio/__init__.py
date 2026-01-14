from collections.abc import Iterable
from contextlib import contextmanager
from io import TextIOWrapper
from pathlib import Path
from typing import BinaryIO, Literal

from pydantic import BaseModel, RootModel

from .backends import csv as csv_backend
from .backends import json as json_backend
from .backends import json_lines as jsl_backend

try:
    from .backends import messagepack as messagepack_backend
except ImportError:
    from .backends import messagepack_stub as messagepack_backend

try:
    from .backends import yaml as yaml_backend
except ImportError:
    from .backends import yaml_stub as yaml_backend

GenericDataFormat = Literal["json", "yaml", "messagepack"]
LinesOnlyDataFormat = Literal["csv", "json_lines"]
DataFormat = GenericDataFormat | LinesOnlyDataFormat


@contextmanager
def detach_on_exit(wrapper: TextIOWrapper):
    try:
        yield wrapper
    finally:
        if not wrapper.closed:
            wrapper.detach()


def decide_data_format_from_path(
    file_path: Path,
) -> DataFormat:
    match file_path.suffix.lower():
        case ".csv":
            return "csv"
        case ".jsonl" | ".jsl" | ".jl" | ".json_lines":
            return "json_lines"
        case ".json":
            return "json"
        case ".yaml" | ".yml":
            return "yaml"
        case ".msgpack":
            return "messagepack"
        case _:
            raise ValueError(f"Unsupported file extension: {file_path.suffix}")


def read_record_from_reader[T: BaseModel](
    reader: BinaryIO, model: type[T], data_format: GenericDataFormat
) -> T:
    match data_format:
        case "json" | "yaml":
            with detach_on_exit(TextIOWrapper(reader, encoding="utf-8")) as text_reader:
                match data_format:
                    case "json":
                        return json_backend.read_record(text_reader, model)
                    case "yaml":
                        return yaml_backend.read_record(text_reader, model)
                    case _:
                        raise ValueError(
                            f"Unreachable: invalid data_format {data_format}"
                        )
        case "messagepack":
            return messagepack_backend.read_record(reader, model)
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def read_record_from_file[T: BaseModel](file_path: str | Path, model: type[T]) -> T:
    file_path = Path(file_path)
    data_format: GenericDataFormat = decide_data_format_from_path(file_path)  # type: ignore
    with file_path.open("rb") as reader:
        return read_record_from_reader(reader, model, data_format)


def read_records_from_reader[T: BaseModel](
    reader: BinaryIO,
    model: type[T],
    data_format: DataFormat,
) -> list[T]:
    list_model = RootModel[list[model]]
    match data_format:
        case "csv" | "json_lines" | "json" | "yaml":
            with detach_on_exit(TextIOWrapper(reader, encoding="utf-8")) as text_reader:
                match data_format:
                    case "csv":
                        return csv_backend.read_records(text_reader, model)
                    case "json_lines":
                        return jsl_backend.read_records(text_reader, model)
                    case "json":
                        return json_backend.read_record(text_reader, list_model).root
                    case "yaml":
                        return yaml_backend.read_record(text_reader, list_model).root
                    case _:
                        raise ValueError(
                            f"Unreachable: invalid data_format {data_format}"
                        )
        case "messagepack":
            return messagepack_backend.read_records(reader, model)
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def read_records_from_file[T: BaseModel](
    file_path: str | Path, model: type[T]
) -> list[T]:
    file_path = Path(file_path)
    data_format = decide_data_format_from_path(file_path)
    with file_path.open("rb") as reader:
        return read_records_from_reader(reader, model, data_format)


def write_record_to_writer(
    writer: BinaryIO, record: BaseModel, data_format: GenericDataFormat
) -> None:
    match data_format:
        case "json" | "yaml":
            with detach_on_exit(TextIOWrapper(writer, encoding="utf-8")) as text_writer:
                match data_format:
                    case "json":
                        json_backend.write_record(text_writer, record)
                    case "yaml":
                        yaml_backend.write_record(text_writer, record)
                    case _:
                        raise ValueError(
                            f"Unreachable: invalid data_format {data_format}"
                        )
        case "messagepack":
            messagepack_backend.write_record(writer, record)
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def write_record_to_file(file_path: str | Path, record: BaseModel) -> None:
    file_path = Path(file_path)
    data_format: GenericDataFormat = decide_data_format_from_path(file_path)  # type: ignore
    with file_path.open("wb") as writer:
        write_record_to_writer(writer, record, data_format)


def write_records_to_writer[T: BaseModel](
    writer: BinaryIO,
    records: Iterable[T],
    data_format: DataFormat,
) -> None:
    list_model = RootModel[Iterable[T]]

    match data_format:
        case "csv" | "json_lines" | "json" | "yaml":
            with detach_on_exit(TextIOWrapper(writer, encoding="utf-8")) as text_writer:
                match data_format:
                    case "csv":
                        csv_backend.write_records(text_writer, records)
                    case "json_lines":
                        jsl_backend.write_records(text_writer, records)
                    case "json":
                        json_backend.write_record(text_writer, list_model(root=records))
                    case "yaml":
                        yaml_backend.write_record(text_writer, list_model(root=records))
                    case _:
                        raise ValueError(
                            f"Unreachable: invalid data_format {data_format}"
                        )
        case "messagepack":
            messagepack_backend.write_records(writer, list(records))
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def write_records_to_file(file_path: str | Path, records: Iterable[BaseModel]) -> None:
    file_path = Path(file_path)
    data_format = decide_data_format_from_path(file_path)
    with file_path.open("wb") as writer:
        write_records_to_writer(writer, records, data_format)
