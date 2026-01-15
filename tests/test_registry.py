"""Tests for the new registry system."""

import threading
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from pydantic import BaseModel
from pydanticio.registry import REGISTRY, BackendProtocol, register_backend
from pydanticio import decide_data_format_from_path


class TestModel(BaseModel):
    name: str
    value: int


class MockBackend:
    """Mock backend for testing registry functionality."""

    def __init__(self, supports_single=True, supports_multiple=True):
        self.supports_single = supports_single
        self.supports_multiple = supports_multiple
        self.read_record_call_count = 0
        self.write_record_call_count = 0
        self.read_records_call_count = 0
        self.write_records_call_count = 0

    def read_record(self, reader, model):
        self.read_record_call_count += 1
        if not self.supports_single:
            raise NotImplementedError("Single record not supported")
        return model(name="test", value=1)

    def write_record(self, writer, record):
        self.write_record_call_count += 1
        if not self.supports_single:
            raise NotImplementedError("Single record not supported")

    def read_records(self, reader, model):
        self.read_records_call_count += 1
        if not self.supports_multiple:
            raise NotImplementedError("Multiple records not supported")
        return [model(name="test", value=1)]

    def write_records(self, writer, records):
        self.write_records_call_count += 1
        if not self.supports_multiple:
            raise NotImplementedError("Multiple records not supported")


def test_register_backend():
    """Test backend registration and retrieval."""
    mock_backend = MockBackend()

    @register_backend("test_format", [".test", ".tst"])
    class TestBackend:
        def read_record(self, reader, model):
            return mock_backend.read_record(reader, model)

        def write_record(self, writer, record):
            mock_backend.write_record(writer, record)

        def read_records(self, reader, model):
            return mock_backend.read_records(reader, model)

        def write_records(self, writer, records):
            mock_backend.write_records(writer, records)

    # Test backend retrieval
    backend = REGISTRY.get_backend("test_format")
    assert backend is not None
    assert hasattr(backend, "read_record")
    assert hasattr(backend, "write_record")
    assert hasattr(backend, "read_records")
    assert hasattr(backend, "write_records")

    # Test extension mapping
    format_name = REGISTRY.get_format_from_extension(".test")
    assert format_name == "test_format"

    format_name = REGISTRY.get_format_from_extension("tst")
    assert format_name == "test_format"


def test_register_backend_validation():
    """Test validation during backend registration."""
    # Test duplicate extension registration by directly using registry
    with pytest.raises(ValueError, match="Extension '.json' is already registered"):
        REGISTRY.register("another_format", MockBackend(), [".json"])

    # Test invalid backend (doesn't implement protocol)
    class InvalidBackend:
        pass  # Missing required methods

    # Direct call to test runtime validation
    invalid_backend = InvalidBackend()
    with pytest.raises(ValueError, match="does not implement BackendProtocol"):
        # Cast to Any to bypass type checking for test purposes
        REGISTRY.register("invalid", invalid_backend, [".inv"])  # type: ignore


def test_registry_error_messages():
    """Test descriptive error messages from registry."""
    # Test non-existent format
    with pytest.raises(
        ValueError, match="Unsupported backend type: 'nonexistent'. Available formats:"
    ):
        REGISTRY.get_backend("nonexistent")

    # Test non-existent extension
    with pytest.raises(
        ValueError, match="Unsupported file extension: '.nonexistent'. Available extensions:"
    ):
        REGISTRY.get_format_from_extension(".nonexistent")


def test_thread_safety():
    """Test registry thread safety."""
    results = []
    errors = []

    def register_backend_thread(thread_id):
        try:

            @register_backend(f"thread_format_{thread_id}", [f".thread{thread_id}"])
            class ThreadBackend:
                def read_record(self, reader, model):
                    pass

                def write_record(self, writer, record):
                    pass

                def read_records(self, reader, model):
                    pass

                def write_records(self, writer, records):
                    pass

            backend = REGISTRY.get_backend(f"thread_format_{thread_id}")
            results.append(f"Thread {thread_id} succeeded: {backend is not None}")
        except Exception as e:
            errors.append(f"Thread {thread_id} failed: {e}")

    # Create multiple threads that register backends simultaneously
    threads = []
    for i in range(10):
        thread = threading.Thread(target=register_backend_thread, args=(i,))
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Verify no errors occurred
    assert len(errors) == 0, f"Thread safety errors: {errors}"
    assert len(results) == 10, f"Expected 10 results, got {len(results)}"

    # Verify all backends are registered
    available_formats = REGISTRY.list_available_formats()
    for i in range(10):
        assert f"thread_format_{i}" in available_formats


def test_backend_capability_errors():
    """Test descriptive errors when backend doesn't support specific operations."""
    import tempfile

    # Test CSV backend (only supports multiple records)
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        from pydanticio import read_record_from_file

        with pytest.raises(
            NotImplementedError, match="CSV format only supports reading/writing multiple records"
        ):
            read_record_from_file(tmp_path, TestModel, data_format="csv")
    finally:
        os.unlink(tmp_path)

    # Test CSV backend (only supports multiple records)
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        from pydanticio import write_record_to_file

        with pytest.raises(
            NotImplementedError, match="CSV format only supports reading/writing multiple records"
        ):
            write_record_to_file(tmp_path, TestModel(name="test", value=1), data_format="csv")
    finally:
        os.unlink(tmp_path)


def test_list_available_formats():
    """Test listing available formats."""
    formats = REGISTRY.list_available_formats()

    # Should include core backends (may vary depending on installed dependencies)
    core_formats = {"json", "csv", "json_lines"}
    for fmt in core_formats:
        assert fmt in formats, f"Core format '{fmt}' missing from available formats: {formats}"

    # Check optional formats only if dependencies are available
    optional_formats = {"yaml", "messagepack", "toml"}
    for fmt in optional_formats:
        if fmt in formats:
            # If present, should work
            backend = REGISTRY.get_backend(fmt)
            assert backend is not None


def test_list_available_extensions():
    """Test listing available extensions."""
    extensions = REGISTRY.list_available_extensions()

    # Should include core extensions
    core_extensions = {".json", ".csv", ".jsonl"}
    for ext in core_extensions:
        assert ext in extensions, (
            f"Core extension '{ext}' missing from available extensions: {extensions}"
        )

    # Test that all extensions start with '.'
    for ext in extensions:
        assert ext.startswith("."), f"Extension '{ext}' should start with '.'"


def test_registration_decorator_preserves_class():
    """Test that registration decorator preserves original class."""

    @register_backend("decorator_test", [".decor"])
    class DecoratorTestBackend:
        def read_record(self, reader, model):
            pass

        def write_record(self, writer, record):
            pass

        def read_records(self, reader, model):
            pass

        def write_records(self, writer, records):
            pass

    # Class should be preserved and work normally
    assert DecoratorTestBackend is not None
    instance = DecoratorTestBackend()
    assert hasattr(instance, "read_record")

    # Should be registered
    backend = REGISTRY.get_backend("decorator_test")
    assert backend is not None
