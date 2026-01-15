from collections.abc import Iterable
from typing import BinaryIO

from pydantic import BaseModel

from ..registry import register_backend
from ..utils import managed_text_io


@register_backend("json_lines", [".jsonl", ".jsl", ".jl", ".json_lines"])
class JSONLinesBackend:
    def read_record(self, reader: BinaryIO, model: type[BaseModel]) -> BaseModel:
        """JSON Lines only supports multiple records."""
        raise NotImplementedError(
            "JSON Lines format only supports reading/writing multiple records. "
            "Use read_records() instead of read_record()."
        )

    def write_record(self, writer: BinaryIO, record: BaseModel) -> None:
        """JSON Lines only supports multiple records."""
        raise NotImplementedError(
            "JSON Lines format only supports reading/writing multiple records. "
            "Use write_records() instead of write_record()."
        )

    def read_records(self, reader: BinaryIO, model: type[BaseModel]) -> list[BaseModel]:
        with managed_text_io(reader, encoding="utf-8") as text_reader:
            return [model.model_validate_json(line) for line in text_reader]

    def write_records(self, writer: BinaryIO, records: Iterable[BaseModel]) -> None:
        with managed_text_io(writer, encoding="utf-8", newline="") as text_writer:
            for record in records:
                text_writer.write(record.model_dump_json())
                text_writer.write("\n")
