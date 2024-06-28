from io import StringIO

from pydanticio import json_lines as jsl_io

from . import TestClass, test_records

records_str = "\n".join(record.model_dump_json() for record in test_records)


def test_read_records_from_reader():
    reader = StringIO(records_str)
    records = jsl_io.read_records_from_reader(reader, TestClass)
    assert records == test_records


def test_write_records_to_writer():
    writer = StringIO()
    jsl_io.write_records_to_writer(writer, test_records)
    assert writer.getvalue().strip() == records_str
