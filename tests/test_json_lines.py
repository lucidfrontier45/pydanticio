from io import StringIO

from pydanticio.json_lines import read, write

from . import TestClass, test_records

record_lines = [record.model_dump_json() for record in test_records]


def test_read_records_from_reader():
    reader = StringIO("\n".join(record_lines))
    records = read(reader, TestClass)
    assert records == test_records


def test_write_records_to_writer():
    writer = StringIO()
    write(writer, test_records)
    assert writer.getvalue().strip().splitlines() == record_lines
