from io import StringIO

from pydanticio import json as json_io
from pydantic import RootModel

from . import TestClass, test_records


def test_read_record_from_reader():
    record_str = test_records[0].model_dump_json()
    rdr = StringIO(record_str)
    record = json_io.read_record_from_reader(rdr, TestClass)
    assert record == test_records[0]


def test_read_records_from_reader():
    records_str = "\n".join(record.model_dump_json() for record in test_records)
    rdr = StringIO(records_str)
    records = json_io.read_records_from_reader(rdr, TestClass)
    assert records == test_records


def test_read_list_of_records_from_reader():
    records_str = f"[{', '.join(record.model_dump_json() for record in test_records)}]"
    rdr = StringIO(records_str)
    record = json_io.read_record_from_reader(rdr, RootModel[list[TestClass]]).root
    assert record == test_records
