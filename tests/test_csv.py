import os
from io import BytesIO

from pydanticio import read_records_from_reader, write_records_to_writer

from . import SampleRecord, test_records


records_str = (
    "\r\n".join(
        [
            test_records[0].get_csv_header(),
            test_records[0].to_csv_row(),
            test_records[1].to_csv_row(),
        ]
    )
    + "\r\n"
)


def test_read_records_from_reader():
    reader = BytesIO(records_str.encode("utf-8"))
    records = read_records_from_reader(reader, SampleRecord, "csv")
    assert records == test_records


def test_write_records_to_writer():
    writer = BytesIO()
    write_records_to_writer(writer, test_records, "csv")
    assert writer.getvalue().decode("utf-8").strip() == records_str.strip()
