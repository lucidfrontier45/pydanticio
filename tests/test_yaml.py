from io import StringIO

from pydanticio import (
    read_record_from_reader,
    write_record_to_writer,
    read_records_from_reader,
    write_records_to_writer,
)
import yaml

from . import TestClass, test_records


def test_read_record_from_reader():
    buffer = StringIO()
    yaml.safe_dump(test_records[0].model_dump(), buffer)
    record_str = buffer.getvalue()
    reader = StringIO(record_str)
    record = read_record_from_reader(reader, TestClass, "yaml")
    assert record == test_records[0]


def test_read_list_of_records_from_reader():
    buffer = StringIO()
    yaml.safe_dump([record.model_dump() for record in test_records], buffer)
    records_str = buffer.getvalue()
    reader = StringIO(records_str)
    records = read_records_from_reader(reader, TestClass, "yaml")
    assert records == test_records


def test_write_record_to_writer():
    buffer = StringIO()
    yaml.safe_dump(test_records[0].model_dump(), buffer)
    record_str = buffer.getvalue()
    writer = StringIO()
    write_record_to_writer(writer, test_records[0], "yaml")
    assert writer.getvalue() == record_str


def test_write_list_of_records_to_writer():
    buffer = StringIO()
    yaml.safe_dump([record.model_dump() for record in test_records], buffer)
    records_str = buffer.getvalue()
    writer = StringIO()
    write_records_to_writer(writer, test_records, "yaml")
    assert writer.getvalue() == records_str
