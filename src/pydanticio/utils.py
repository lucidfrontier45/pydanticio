from contextlib import contextmanager
from io import TextIOWrapper
from typing import BinaryIO


@contextmanager
def managed_text_io(binary_io: BinaryIO, encoding: str = "utf-8", newline: str | None = None):
    wrapper = TextIOWrapper(binary_io, encoding=encoding, newline=newline)
    try:
        yield wrapper
    finally:
        if not wrapper.closed:
            wrapper.detach()
