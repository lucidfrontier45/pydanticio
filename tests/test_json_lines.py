from io import StringIO

from pydanticio import read_records_from_reader, write_records_to_writer

from . import TestClass, test_records

record_lines = [record.model_dump_json() for record in test_records]


def test_read_records_from_reader():
    reader = StringIO("\n".join(record_lines))
    records = read_records_from_reader(reader, TestClass, "json_lines")
    assert records == test_records


def test_write_records_to_writer():
    writer = StringIO()
    write_records_to_writer(writer, test_records, "json_lines")
    assert writer.getvalue().strip().splitlines() == record_lines
