from io import BytesIO

from pydanticio import (
    read_record_from_reader,
    write_record_to_writer,
)
import tomlkit

from . import SampleRecord, test_records


def test_read_record_from_reader():
    data = tomlkit.dumps(test_records[0].model_dump()).encode("utf-8")
    reader = BytesIO(data)
    record = read_record_from_reader(reader, SampleRecord, "toml")
    assert record == test_records[0]


def test_write_record_to_writer():
    data = tomlkit.dumps(test_records[0].model_dump()).encode("utf-8")
    writer = BytesIO()
    write_record_to_writer(writer, test_records[0], "toml")
    assert writer.getvalue() == data
