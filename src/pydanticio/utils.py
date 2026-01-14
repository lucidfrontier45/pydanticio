import os
from contextlib import contextmanager
from io import TextIOWrapper
from typing import BinaryIO

PLATFORM_NEWLINE = "\r\n" if os.name == "nt" else "\n"


@contextmanager
def managed_text_io(binary_io: BinaryIO, encoding: str = "utf-8", newline: str | None = None):
    wrapper = TextIOWrapper(binary_io, encoding=encoding, newline=newline)
    try:
        yield wrapper
    finally:
        if not wrapper.closed:
            wrapper.detach()
