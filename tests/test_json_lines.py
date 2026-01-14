from io import BytesIO

from pydanticio import read_records_from_reader, write_records_to_writer

from . import SampleRecord, test_records

record_lines = [record.model_dump_json() for record in test_records]


def test_read_records_from_reader():
    reader = BytesIO("\n".join(record_lines).encode("utf-8"))
    records = read_records_from_reader(reader, SampleRecord, "json_lines")
    assert records == test_records


def test_write_records_to_writer():
    writer = BytesIO()
    write_records_to_writer(writer, test_records, "json_lines")
    assert writer.getvalue().decode("utf-8").strip().splitlines() == record_lines
