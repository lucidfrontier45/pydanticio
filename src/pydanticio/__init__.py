from collections.abc import Iterable
from pathlib import Path
from typing import BinaryIO

from pydantic import BaseModel

# Import backends - they register themselves
from .backends import csv, json, json_lines

# Optional dependencies with better error handling
try:
    from .backends import yaml
except ImportError:
    yaml = None

try:
    from .backends import messagepack
except ImportError:
    messagepack = None

try:
    from .backends import toml
except ImportError:
    toml = None

from .registry import REGISTRY
from .version import __version__

# Flexible string-based type system
DataFormat = str


def decide_data_format_from_path(file_path: Path) -> str:
    extension = file_path.suffix.lower()
    try:
        return REGISTRY.get_format_from_extension(extension)
    except ValueError as e:
        # Add installation suggestions for missing optional backends
        msg = str(e)
        if extension in [".yaml", ".yml"] and yaml is None:
            msg += " Install with: pip install pydanticio[yaml]"
        elif extension == ".msgpack" and messagepack is None:
            msg += " Install with: pip install pydanticio[msgpack]"
        elif extension == ".toml" and toml is None:
            msg += " Install with: pip install pydanticio[toml]"
        raise ValueError(msg) from e


def read_record_from_reader[T: BaseModel](reader: BinaryIO, model: type[T], data_format: str) -> T:
    backend = REGISTRY.get_backend(data_format)
    return backend.read_record(reader, model)


def read_record_from_file[T: BaseModel](
    file_path: str | Path,
    model: type[T],
    data_format: str | None = None,
) -> T:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)

    # Check backend capabilities by testing if it raises NotImplementedError
    backend = REGISTRY.get_backend(actual_data_format)
    if not hasattr(backend, "read_record"):
        raise ValueError(
            f"Backend '{actual_data_format}' does not support single record operations"
        ) from None

    with file_path.open("rb") as reader:
        return read_record_from_reader(reader, model, actual_data_format)


def read_records_from_reader[T: BaseModel](
    reader: BinaryIO,
    model: type[T],
    data_format: str,
) -> list[T]:
    backend = REGISTRY.get_backend(data_format)
    return backend.read_records(reader, model)


def read_records_from_file[T: BaseModel](
    file_path: str | Path,
    model: type[T],
    data_format: str | None = None,
) -> list[T]:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)

    # Check backend capabilities by testing if it raises NotImplementedError
    backend = REGISTRY.get_backend(actual_data_format)
    if not hasattr(backend, "read_records"):
        raise ValueError(
            f"Backend '{actual_data_format}' does not support multiple record operations"
        ) from None

    with file_path.open("rb") as reader:
        return read_records_from_reader(reader, model, actual_data_format)


def write_record_to_writer(writer: BinaryIO, record: BaseModel, data_format: str) -> None:
    backend = REGISTRY.get_backend(data_format)
    backend.write_record(writer, record)


def write_record_to_file(
    file_path: str | Path,
    record: BaseModel,
    data_format: str | None = None,
) -> None:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)

    # Check backend capabilities by testing if it raises NotImplementedError
    backend = REGISTRY.get_backend(actual_data_format)
    if not hasattr(backend, "write_record"):
        raise ValueError(
            f"Backend '{actual_data_format}' does not support single record operations"
        ) from None

    with file_path.open("wb") as writer:
        write_record_to_writer(writer, record, actual_data_format)


def write_records_to_writer[T: BaseModel](
    writer: BinaryIO,
    records: Iterable[T],
    data_format: str,
) -> None:
    backend = REGISTRY.get_backend(data_format)
    backend.write_records(writer, records)


def write_records_to_file(
    file_path: str | Path,
    records: Iterable[BaseModel],
    data_format: str | None = None,
) -> None:
    file_path = Path(file_path)
    actual_data_format = data_format or decide_data_format_from_path(file_path)

    # Check backend capabilities by testing if it raises NotImplementedError
    backend = REGISTRY.get_backend(actual_data_format)
    if not hasattr(backend, "write_records"):
        raise ValueError(
            f"Backend '{actual_data_format}' does not support multiple record operations"
        ) from None

    with file_path.open("wb") as writer:
        write_records_to_writer(writer, records, actual_data_format)
