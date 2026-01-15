
import yaml

from ..adapters import ListFormatAdapter
from ..registry import register_backend
from ..utils import managed_text_io


@register_backend("yaml", [".yaml", ".yml"])
class YAMLBackend(ListFormatAdapter):
    def __init__(self):
        super().__init__(self._read_record_impl, self._write_record_impl)

    def _read_record_impl(self, reader, model):
        with managed_text_io(reader, encoding="utf-8") as text_reader:
            data = yaml.safe_load(text_reader)
            return model.model_validate(data)

    def _write_record_impl(self, writer, record):
        with managed_text_io(writer, encoding="utf-8", newline="") as text_writer:
            yaml.safe_dump(record.model_dump(mode="json"), text_writer, line_break="\n")
