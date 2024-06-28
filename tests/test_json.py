from io import StringIO

from pydanticio import json as json_io
from pydantic import RootModel

from . import TestClass, test_records


def test_read_record_from_reader():
    record_str = test_records[0].model_dump_json()
    reader = StringIO(record_str)
    record = json_io.read_record_from_reader(reader, TestClass)
    assert record == test_records[0]


def test_read_records_from_reader():
    records_str = ",".join(record.model_dump_json() for record in test_records)
    records_str = f"[{records_str}]"
    reader = StringIO(records_str)
    records = json_io.read_records_from_reader(reader, TestClass)
    assert records == test_records


def test_read_list_of_records_from_reader():
    records_str = ",".join(record.model_dump_json() for record in test_records)
    records_str = f"[{records_str}]"
    reader = StringIO(records_str)
    record = json_io.read_record_from_reader(reader, RootModel[list[TestClass]]).root
    assert record == test_records


def test_write_record_to_writer():
    record_str = test_records[0].model_dump_json()
    writer = StringIO()
    json_io.write_record_to_writer(writer, test_records[0])
    assert writer.getvalue() == record_str


def test_write_records_to_writer():
    records_str = ",".join(record.model_dump_json() for record in test_records)
    records_str = f"[{records_str}]"
    writer = StringIO()
    json_io.write_records_to_writer(writer, test_records)
    assert writer.getvalue() == records_str


def test_write_list_of_records_to_writer():
    records_str = ",".join(record.model_dump_json() for record in test_records)
    records_str = f"[{records_str}]"
    writer = StringIO()
    json_io.write_record_to_writer(
        writer, RootModel[list[TestClass]](root=test_records)
    )
    assert writer.getvalue() == records_str
