"""
Thread-safe backend registry with auto-registration and descriptive errors.
"""

import threading
from collections.abc import Iterable
from typing import BinaryIO, Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@runtime_checkable
class BackendProtocol(Protocol):
    """Common interface for all backend implementations."""

    def read_record(self, reader: BinaryIO, model: type[T]) -> T:
        """Read a single record from binary I/O."""
        ...

    def read_records(self, reader: BinaryIO, model: type[T]) -> list[T]:
        """Read multiple records from binary I/O."""
        ...

    def write_record(self, writer: BinaryIO, record: BaseModel) -> None:
        """Write a single record to binary I/O."""
        ...

    def write_records(self, writer: BinaryIO, records: Iterable[BaseModel]) -> None:
        """Write multiple records to binary I/O."""
        ...


class BackendRegistry:
    """Thread-safe registry for backend implementations."""

    def __init__(self):
        self._backends: dict[str, BackendProtocol] = {}
        self._extensions: dict[str, str] = {}
        self._lock = threading.RLock()

    def register(self, format_name: str, backend: BackendProtocol, extensions: list[str]) -> None:
        """Thread-safe backend registration with validation."""
        with self._lock:
            if format_name in self._backends:
                raise ValueError(f"Backend '{format_name}' is already registered")

            # Validate backend implements protocol
            if not isinstance(backend, BackendProtocol):
                raise ValueError(f"Backend '{format_name}' does not implement BackendProtocol")

            self._backends[format_name] = backend

            # Register extensions
            for ext in extensions:
                normalized_ext = ext.lower()
                if not normalized_ext.startswith("."):
                    normalized_ext = f".{normalized_ext}"

                if normalized_ext in self._extensions:
                    existing_format = self._extensions[normalized_ext]
                    raise ValueError(
                        f"Extension '{ext}' is already registered for format '{existing_format}'"
                    )
                self._extensions[normalized_ext] = format_name

    def get_backend(self, format_name: str) -> BackendProtocol:
        """Get backend with descriptive error if not found."""
        with self._lock:
            if format_name not in self._backends:
                available = ", ".join(sorted(self._backends.keys()))
                raise ValueError(
                    f"Unsupported backend type: '{format_name}'. Available formats: {available}"
                )
            return self._backends[format_name]

    def get_format_from_extension(self, extension: str) -> str:
        """Get format from extension with descriptive error."""
        with self._lock:
            normalized_ext = extension.lower()
            if not normalized_ext.startswith("."):
                normalized_ext = f".{normalized_ext}"

            if normalized_ext not in self._extensions:
                available = ", ".join(sorted(self._extensions.keys()))
                raise ValueError(
                    f"Unsupported file extension: '{extension}'. Available extensions: {available}"
                )
            return self._extensions[normalized_ext]

    def list_available_formats(self) -> list[str]:
        """List all registered formats."""
        with self._lock:
            return list(self._backends.keys())

    def list_available_extensions(self) -> list[str]:
        """List all registered extensions."""
        with self._lock:
            return list(self._extensions.keys())


def register_backend(format_name: str, extensions: list[str]):
    """Decorator for auto-registering backends."""

    def decorator(backend_class):
        instance = backend_class()
        REGISTRY.register(format_name, instance, extensions)
        return backend_class

    return decorator


# Global registry instance
REGISTRY = BackendRegistry()
