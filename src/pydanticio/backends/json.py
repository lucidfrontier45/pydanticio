

from ..adapters import ListFormatAdapter
from ..registry import register_backend
from ..utils import managed_text_io


@register_backend("json", [".json"])
class JSONBackend(ListFormatAdapter):
    def __init__(self):
        super().__init__(self._read_record_impl, self._write_record_impl)

    def _read_record_impl(self, reader, model):
        with managed_text_io(reader, encoding="utf-8") as text_reader:
            data = text_reader.read()
            return model.model_validate_json(data)

    def _write_record_impl(self, writer, record):
        with managed_text_io(writer, encoding="utf-8", newline="") as text_writer:
            text_writer.write(record.model_dump_json())
