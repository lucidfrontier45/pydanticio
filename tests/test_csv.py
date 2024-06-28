import csv
from io import StringIO

from pydanticio.csv import read, write

from . import TestClass, test_records


records_str = "\r\n".join(
    [
        test_records[0].get_csv_header(),
        test_records[0].to_csv_row(),
        test_records[1].to_csv_row(),
    ]
)


def test_read_records_from_reader():
    reader = StringIO(records_str)
    records = read(reader, TestClass)
    assert records == test_records


def test_write_records_to_writer():
    writer = StringIO()
    write(writer, test_records)
    assert writer.getvalue().strip() == records_str.strip()
