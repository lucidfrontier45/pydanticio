from io import BytesIO

from pydanticio import (
    read_record_from_reader,
    write_record_to_writer,
    read_records_from_reader,
    write_records_to_writer,
)
import msgpack

from . import SampleRecord, test_records


def test_read_record_from_reader():
    data = msgpack.packb(test_records[0].model_dump())
    if data is None:
        data = b""
    reader = BytesIO(data)
    record = read_record_from_reader(reader, SampleRecord, "messagepack")
    assert record == test_records[0]


def test_read_list_of_records_from_reader():
    data = msgpack.packb([record.model_dump() for record in test_records])
    if data is None:
        data = b""
    reader = BytesIO(data)
    records = read_records_from_reader(reader, SampleRecord, "messagepack")
    assert records == test_records


def test_write_record_to_writer():
    data = msgpack.packb(test_records[0].model_dump())
    if data is None:
        data = b""
    writer = BytesIO()
    write_record_to_writer(writer, test_records[0], "messagepack")
    assert writer.getvalue() == data


def test_write_list_of_records_to_writer():
    data = msgpack.packb([record.model_dump() for record in test_records])
    if data is None:
        data = b""
    writer = BytesIO()
    write_records_to_writer(writer, test_records, "messagepack")
    assert writer.getvalue() == data
