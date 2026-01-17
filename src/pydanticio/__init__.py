from collections.abc import Iterable
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

try:
    from .backends import toml as toml_backend
except ImportError:
    from .backends import toml_stub as toml_backend

try:
    from .backends import cbor as cbor_backend
except ImportError:
    from .backends import cbor_stub as cbor_backend

from .version import __version__

GenericDataFormat = Literal["json", "yaml", "messagepack", "cbor"]
SingleOnlyDataFormat = Literal["toml"]
LinesOnlyDataFormat = Literal["csv", "json_lines"]


def decide_data_format_from_path(
    file_path: Path,
) -> GenericDataFormat | SingleOnlyDataFormat | LinesOnlyDataFormat:
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
        case ".cbor":
            return "cbor"
        case ".toml":
            return "toml"
        case _:
            raise ValueError(f"Unsupported file extension: {file_path.suffix}")


def read_record_from_reader[T: BaseModel](
    reader: BinaryIO, model: type[T], data_format: GenericDataFormat | SingleOnlyDataFormat
) -> T:
    match data_format:
        case "json":
            return json_backend.read_record(reader, model)
        case "yaml":
            return yaml_backend.read_record(reader, model)
        case "toml":
            return toml_backend.read_record(reader, model)
        case "messagepack":
            return messagepack_backend.read_record(reader, model)
        case "cbor":
            return cbor_backend.read_record(reader, model)
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def read_record_from_file[T: BaseModel](
    file_path: str | Path,
    model: type[T],
    data_format: GenericDataFormat | SingleOnlyDataFormat | None = None,
) -> T:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)
    if actual_data_format in ("csv", "json_lines"):
        raise ValueError(
            f"Data format {actual_data_format} is not supported for single record reading"
        )
    with file_path.open("rb") as reader:
        return read_record_from_reader(reader, model, actual_data_format)


def read_records_from_reader[T: BaseModel](
    reader: BinaryIO,
    model: type[T],
    data_format: GenericDataFormat | LinesOnlyDataFormat,
) -> list[T]:
    list_model = RootModel[list[model]]
    match data_format:
        case "csv":
            return csv_backend.read_records(reader, model)
        case "json_lines":
            return jsl_backend.read_records(reader, model)
        case "json":
            return json_backend.read_record(reader, list_model).root
        case "yaml":
            return yaml_backend.read_record(reader, list_model).root
        case "messagepack":
            return messagepack_backend.read_records(reader, model)
        case "cbor":
            return cbor_backend.read_records(reader, model)
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def read_records_from_file[T: BaseModel](
    file_path: str | Path,
    model: type[T],
    data_format: GenericDataFormat | LinesOnlyDataFormat | None = None,
) -> list[T]:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)
    if actual_data_format in ("toml",):
        raise ValueError(
            f"Data format {actual_data_format} is not supported for multiple record reading"
        )
    with file_path.open("rb") as reader:
        return read_records_from_reader(reader, model, actual_data_format)


def write_record_to_writer(
    writer: BinaryIO, record: BaseModel, data_format: GenericDataFormat | SingleOnlyDataFormat
) -> None:
    match data_format:
        case "json":
            json_backend.write_record(writer, record)
        case "yaml":
            yaml_backend.write_record(writer, record)
        case "toml":
            toml_backend.write_record(writer, record)
        case "messagepack":
            messagepack_backend.write_record(writer, record)
        case "cbor":
            cbor_backend.write_record(writer, record)
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def write_record_to_file(
    file_path: str | Path,
    record: BaseModel,
    data_format: GenericDataFormat | SingleOnlyDataFormat | None = None,
) -> None:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)
    if actual_data_format in ("csv", "json_lines"):
        raise ValueError(
            f"Data format {actual_data_format} is not supported for single record writing"
        )
    with file_path.open("wb") as writer:
        write_record_to_writer(writer, record, actual_data_format)


def write_records_to_writer[T: BaseModel](
    writer: BinaryIO,
    records: Iterable[T],
    data_format: GenericDataFormat | LinesOnlyDataFormat,
) -> None:
    list_model = RootModel[Iterable[T]]

    match data_format:
        case "csv":
            csv_backend.write_records(writer, records)
        case "json_lines":
            jsl_backend.write_records(writer, records)
        case "json":
            json_backend.write_record(writer, list_model(root=records))
        case "yaml":
            yaml_backend.write_record(writer, list_model(root=records))
        case "messagepack":
            messagepack_backend.write_records(writer, list(records))
        case "cbor":
            cbor_backend.write_records(writer, list(records))
        case _:
            raise ValueError(f"Unsupported backend type: {data_format}")


def write_records_to_file(
    file_path: str | Path,
    records: Iterable[BaseModel],
    data_format: GenericDataFormat | LinesOnlyDataFormat | None = None,
) -> None:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)
    if actual_data_format in ("toml",):
        raise ValueError(
            f"Data format {actual_data_format} is not supported for multiple record writing"
        )
    with file_path.open("wb") as writer:
        write_records_to_writer(writer, records, actual_data_format)
