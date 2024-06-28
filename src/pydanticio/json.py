from typing import TextIO

from .common import T


def read_record_from_reader(reader: TextIO, model: type[T]) -> T:
    data = reader.read()
    return model.model_validate_json(data)


def read_records_from_reader(reader: TextIO, model: type[T]) -> list[T]:
    return [model.model_validate_json(line) for line in reader]
