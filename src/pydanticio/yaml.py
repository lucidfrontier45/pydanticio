from typing import TextIO

import yaml
from pydantic import BaseModel

from .common import T


def read_record(reader: TextIO, model: type[T]) -> T:
    data = yaml.safe_load(reader)
    return model.model_validate(data)


def write_record(writer: TextIO, record: BaseModel) -> None:
    yaml.safe_dump(record.model_dump(mode="json"), writer)
