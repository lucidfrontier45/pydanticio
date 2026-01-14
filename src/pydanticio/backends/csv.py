import csv
from collections.abc import Iterable
from typing import BinaryIO

from pydantic import BaseModel

from ..utils import managed_text_io


def read_records[T: BaseModel](reader: BinaryIO, model: type[T]) -> list[T]:
    with managed_text_io(reader, encoding="utf-8") as text_reader:
        csv_reader = csv.DictReader(text_reader)
        return [model.model_validate(row) for row in csv_reader]


def write_records(writer: BinaryIO, records: Iterable[BaseModel]) -> None:
    # Use newline='' so the csv module doesn't insert extra blank lines on Windows
    with managed_text_io(writer, encoding="utf-8", newline="") as text_writer:
        it = iter(records)
        first_record = next(it)
        fields = list(type(first_record).model_fields.keys())
        csv_writer = csv.DictWriter(text_writer, fieldnames=fields, lineterminator="\r\n")
        csv_writer.writeheader()
        csv_writer.writerow(first_record.model_dump(mode="json"))
        for record in it:
            csv_writer.writerow(record.model_dump(mode="json"))
