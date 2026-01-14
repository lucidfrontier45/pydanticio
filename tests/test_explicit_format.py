import tempfile
from pathlib import Path

from pydanticio import (
    read_record_from_file,
    read_records_from_file,
    write_record_to_file,
    write_records_to_file,
)

from . import SampleRecord, test_records


def test_read_record_from_file_explicit_format():
    """Test reading a single record with explicit format."""
    record = test_records[0]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(record.model_dump_json())
        temp_path = Path(f.name)

    try:
        # Test with explicit format
        result = read_record_from_file(temp_path, SampleRecord, data_format="json")
        assert result == record

        # Test that explicit format overrides file extension (wrong extension but correct format)
        wrong_ext_path = temp_path.with_suffix(".txt")
        temp_path.rename(wrong_ext_path)
        result = read_record_from_file(wrong_ext_path, SampleRecord, data_format="json")
        assert result == record
    finally:
        temp_path.unlink(missing_ok=True)
        wrong_ext_path.unlink(missing_ok=True)


def test_read_records_from_file_explicit_format():
    """Test reading multiple records with explicit format."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        records_json = "[" + ",".join(record.model_dump_json() for record in test_records) + "]"
        f.write(records_json)
        temp_path = Path(f.name)

    try:
        # Test with explicit format
        result = read_records_from_file(temp_path, SampleRecord, data_format="json")
        assert result == test_records

        # Test that explicit format overrides file extension
        wrong_ext_path = temp_path.with_suffix(".txt")
        temp_path.rename(wrong_ext_path)
        result = read_records_from_file(wrong_ext_path, SampleRecord, data_format="json")
        assert result == test_records
    finally:
        temp_path.unlink(missing_ok=True)
        wrong_ext_path.unlink(missing_ok=True)


def test_write_record_to_file_explicit_format():
    """Test writing a single record with explicit format."""
    record = test_records[0]

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        temp_path = Path(f.name)

    try:
        # Test with explicit format
        write_record_to_file(temp_path, record, data_format="json")

        # Read it back to verify
        result = read_record_from_file(temp_path, SampleRecord, data_format="json")
        assert result == record

        # Test that explicit format works with wrong extension
        wrong_ext_path = temp_path.with_suffix(".txt")
        write_record_to_file(wrong_ext_path, record, data_format="json")
        result = read_record_from_file(wrong_ext_path, SampleRecord, data_format="json")
        assert result == record
    finally:
        temp_path.unlink(missing_ok=True)
        wrong_ext_path.unlink(missing_ok=True)


def test_write_records_to_file_explicit_format():
    """Test writing multiple records with explicit format."""

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        temp_path = Path(f.name)

    try:
        # Test with explicit format
        write_records_to_file(temp_path, test_records, data_format="json")

        # Read it back to verify
        result = read_records_from_file(temp_path, SampleRecord, data_format="json")
        assert result == test_records

        # Test that explicit format works with wrong extension
        wrong_ext_path = temp_path.with_suffix(".txt")
        write_records_to_file(wrong_ext_path, test_records, data_format="json")
        result = read_records_from_file(wrong_ext_path, SampleRecord, data_format="json")
        assert result == test_records
    finally:
        temp_path.unlink(missing_ok=True)
        wrong_ext_path.unlink(missing_ok=True)


def test_backward_compatibility_no_format():
    """Test that functions still work when no format is specified (backward compatibility)."""
    record = test_records[0]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(record.model_dump_json())
        temp_path = Path(f.name)

    try:
        # Should work without explicit format (inferred from extension)
        result = read_record_from_file(temp_path, SampleRecord)
        assert result == record

        # Should work without explicit format for writing
        output_path = temp_path.with_suffix(".output.json")
        write_record_to_file(output_path, record)
        result = read_record_from_file(output_path, SampleRecord)
        assert result == record
    finally:
        temp_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)
