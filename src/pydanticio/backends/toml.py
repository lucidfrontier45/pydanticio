
import tomlkit

from ..adapters import SingleRecordAdapter
from ..registry import register_backend
from ..utils import PLATFORM_NEWLINE, managed_text_io


@register_backend("toml", [".toml"])
class TOMLBackend(SingleRecordAdapter):
    def __init__(self):
        super().__init__(self._read_record_impl, self._write_record_impl)

    def _read_record_impl(self, reader, model):
        with managed_text_io(reader, encoding="utf-8") as text_reader:
            data = tomlkit.load(text_reader)
            return model.model_validate(data)

    def _write_record_impl(self, writer, record):
        # Use platform-specific newline to ensure compatibility
        with managed_text_io(writer, encoding="utf-8", newline=PLATFORM_NEWLINE) as text_writer:
            tomlkit.dump(record.model_dump(mode="json"), text_writer)
