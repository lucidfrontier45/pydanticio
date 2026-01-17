from io import BytesIO

from pydanticio import (
    read_record_from_reader,
    write_record_to_writer,
    read_records_from_reader,
    write_records_to_writer,
)
import cbor2

from . import SampleRecord, test_records


def test_read_record_from_reader():
    data = cbor2.dumps(test_records[0].model_dump(mode="json"), canonical=True)
    reader = BytesIO(data)  # type: ignore
    record = read_record_from_reader(reader, SampleRecord, "cbor")
    assert record == test_records[0]


def test_read_list_of_records_from_reader():
    data = cbor2.dumps([record.model_dump(mode="json") for record in test_records], canonical=True)
    reader = BytesIO(data)  # type: ignore
    records = read_records_from_reader(reader, SampleRecord, "cbor")
    assert records == test_records


def test_write_record_to_writer():
    data = cbor2.dumps(test_records[0].model_dump(mode="json"), canonical=True)
    writer = BytesIO()
    write_record_to_writer(writer, test_records[0], "cbor")
    assert writer.getvalue() == data


def test_write_list_of_records_to_writer():
    data = cbor2.dumps([record.model_dump(mode="json") for record in test_records], canonical=True)  # type: ignore
    writer = BytesIO()
    write_records_to_writer(writer, test_records, "cbor")
    assert writer.getvalue() == data
