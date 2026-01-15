import csv
from collections.abc import Iterable
from typing import BinaryIO

from pydantic import BaseModel

from ..registry import register_backend
from ..utils import managed_text_io


@register_backend("csv", [".csv"])
class CSVBackend:
    def read_record(self, reader: BinaryIO, model: type[BaseModel]) -> BaseModel:
        """CSV only supports multiple records."""
        raise NotImplementedError(
            "CSV format only supports reading/writing multiple records. "
            "Use read_records() instead of read_record()."
        )

    def write_record(self, writer: BinaryIO, record: BaseModel) -> None:
        """CSV only supports multiple records."""
        raise NotImplementedError(
            "CSV format only supports reading/writing multiple records. "
            "Use write_records() instead of write_record()."
        )

    def read_records(self, reader: BinaryIO, model: type[BaseModel]) -> list[BaseModel]:
        with managed_text_io(reader, encoding="utf-8") as text_reader:
            csv_reader = csv.DictReader(text_reader)
            return [model.model_validate(row) for row in csv_reader]

    def write_records(self, writer: BinaryIO, records: Iterable[BaseModel]) -> None:
        # Use newline='' so as csv module doesn't insert extra blank lines on Windows
        with managed_text_io(writer, encoding="utf-8", newline="") as text_writer:
            it = iter(records)
            try:
                first_record = next(it)
            except StopIteration:
                return  # Empty records

            fields = list(type(first_record).model_fields.keys())
            csv_writer = csv.DictWriter(text_writer, fieldnames=fields, lineterminator="\r\n")
            csv_writer.writeheader()
            csv_writer.writerow(first_record.model_dump(mode="json"))
            for record in it:
                csv_writer.writerow(record.model_dump(mode="json"))
