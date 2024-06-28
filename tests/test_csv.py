from io import StringIO

from pydanticio import read_records_from_reader, write_records_to_writer

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
    records = read_records_from_reader(reader, TestClass, "csv")
    assert records == test_records


def test_write_records_to_writer():
    writer = StringIO()
    write_records_to_writer(writer, test_records, "csv")
    assert writer.getvalue().strip() == records_str.strip()
