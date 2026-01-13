from io import BytesIO, StringIO

from pydanticio import (
    read_record_from_reader,
    write_record_to_writer,
    read_records_from_reader,
    write_records_to_writer,
)
from pydantic import RootModel

from . import TestClass, test_records


def test_read_record_from_reader():
    record_str = test_records[0].model_dump_json()
    reader = BytesIO(record_str.encode("utf-8"))
    record = read_record_from_reader(reader, TestClass, "json")
    assert record == test_records[0]


def test_read_list_of_records_from_reader():
    records_str = ",".join(record.model_dump_json() for record in test_records)
    records_str = f"[{records_str}]"
    reader = BytesIO(records_str.encode("utf-8"))
    records = read_records_from_reader(reader, TestClass, "json")
    assert records == test_records


def test_write_record_to_writer():
    record_str = test_records[0].model_dump_json()
    writer = BytesIO()
    write_record_to_writer(writer, test_records[0], "json")
    assert writer.getvalue() == record_str.encode("utf-8")


def test_write_list_of_records_to_writer():
    records_str = ",".join(record.model_dump_json() for record in test_records)
    records_str = f"[{records_str}]"
    writer = BytesIO()
    write_records_to_writer(writer, test_records, "json")
    assert writer.getvalue() == records_str.encode("utf-8")
