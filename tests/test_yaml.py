from io import BytesIO

from pydanticio import (
    read_record_from_reader,
    write_record_to_writer,
    read_records_from_reader,
    write_records_to_writer,
)
import yaml

from . import SampleRecord, test_records


def test_read_record_from_reader():
    data = yaml.safe_dump(test_records[0].model_dump()).encode("utf-8")
    reader = BytesIO(data)
    record = read_record_from_reader(reader, SampleRecord, "yaml")
    assert record == test_records[0]


def test_read_list_of_records_from_reader():
    data = yaml.safe_dump([record.model_dump() for record in test_records]).encode("utf-8")
    reader = BytesIO(data)
    records = read_records_from_reader(reader, SampleRecord, "yaml")
    assert records == test_records


def test_write_record_to_writer():
    data = yaml.safe_dump(test_records[0].model_dump()).encode("utf-8")
    writer = BytesIO()
    write_record_to_writer(writer, test_records[0], "yaml")
    assert writer.getvalue() == data


def test_write_list_of_records_to_writer():
    data = yaml.safe_dump([record.model_dump() for record in test_records]).encode("utf-8")
    writer = BytesIO()
    write_records_to_writer(writer, test_records, "yaml")
    assert writer.getvalue() == data
