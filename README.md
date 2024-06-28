# PydanticIO

PydanticIO (pronounce pidantisio) is a tiny file IO utility library for Python powered by Pydantic.
This library is a port of the Rust library [SerdeIO](https://github.com/lucidfrontier45/serdeio)

# Install

`pip install pydanticio`

# Supported Formats

- CSV by stdlib `csv` module
- JSON by stdlib `json` module
- JSON Lines by stdlib `json` module

# Usage

- `read_record_from_reader` is used to read a type `T` which is a subclass of `pydantic.BaseModel` from `TextIO`. Data format must be specified by `DataFormat` literals.
- `read_records_from_reader` always tries to deserialize the data as `list[T]`.
- `read_record_from_file` and `read_records_from_file` accepts a `Path`. Data format is automatically determined by file extension.
- `write_*` functions follow the same rules as `read_*`.

Note that some data format like CSV and JSON Lines support only reading records `list[T]`.

# Examples

```py
from pydantic import BaseModel
from pydanticio import read_records_from_file, write_records_to_file

class User(BaseModel):
    name: str
    age: int


users = read_records_from_file("users.csv", User)
write_records_to_file("users.json", users)
```