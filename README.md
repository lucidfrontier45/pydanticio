# PydanticIO

PydanticIO (pronounce pidantisio) is a tiny file IO utility library for Python powered by Pydantic.
This library is a port of the Rust library [SerdeIO](https://github.com/lucidfrontier45/serdeio)

# Install

```sh
# standard distribution
pip install pydanticio

# with YAML backend
pip install pydanticio[yaml]
```

# Supported Formats

- CSV by stdlib `csv` module
- JSON by stdlib `json` module
- JSON Lines by stdlib `json` module
- YAML by `pyyaml` library (optional feature)

# Usage

- `read_record_from_reader` reads a single `T` (subclass of `pydantic.BaseModel`) from `BinaryIO`. Data format must be `json` or `yaml`.
- `read_records_from_reader` reads `list[T]` from `BinaryIO`. Supports all formats: `csv`, `json_lines`, `json`, `yaml`.
- `read_record_from_file` and `read_records_from_file` accept a `Path`. Data format is auto-detected from file extension.
- `write_*` functions follow the same rules as `read_*`.

Note: CSV and JSON Lines only support lists of records, not single records.

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
