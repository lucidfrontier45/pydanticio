<img src="logo.png" alt="PydanticIO Logo" width="500" />

[![PyPI Version](https://img.shields.io/pypi/v/pydanticio)](https://pypi.org/project/pydanticio/)
[![Python Versions](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/pypi/l/pydanticio)](https://github.com/lucidfrontier45/pydanticio/blob/main/LICENSE)

A tiny file IO utility library for Python powered by [Pydantic](https://docs.pydantic.dev/). This library is a port of the Rust library [SerdeIO](https://github.com/lucidfrontier45/serdeio).

## Features

- **Type-safe**: Read and write Pydantic models with full type inference
- **Format support**: CSV, JSON, JSON Lines, TOML, YAML, and MessagePack (optional)
- **Auto-detection**: Automatically detects format from file extension
- **Simple API**: Intuitive functions for single records and lists
- **Zero dependencies**: Core library only requires Pydantic

## Installation

```sh
# Standard distribution
pip install pydanticio

# With YAML support
pip install pydanticio[yaml]

# With MessagePack support
pip install pydanticio[messagepack]

# With TOML support
pip install pydanticio[toml]
```

## Quick Start

```python
from pydantic import BaseModel
from pydanticio import read_records_from_file, write_records_to_file

class User(BaseModel):
    name: str
    age: int

# Read from any supported format (auto-detected from extension)
users = read_records_from_file("users.csv", User)

# Write to any supported format
write_records_to_file("output.json", users)
```

## Supported Formats

| Format      | File Extensions                        | Single Record | List of Records |
| ----------- | -------------------------------------- | ------------- | --------------- |
| CSV         | `.csv`                                 | No            | Yes             |
| JSON        | `.json`                                | Yes           | Yes             |
| JSON Lines  | `.jsonl`, `.jl`, `.jsl`, `.json_lines` | No            | Yes             |
| MessagePack | `.msgpack`                             | Yes           | Yes             |
| TOML        | `.toml`                                | Yes           | No              |
| YAML        | `.yaml`, `.yml`                        | Yes           | Yes             |

All text-based formats use UTF-8 encoding.

### Newline Handling

Text-based formats handle newlines according to their respective specifications:

| Format      | Line Ending | Notes                              |
| ----------- | ----------- | ---------------------------------- |
| CSV         | `\r\n`      | Uses CRLF per RFC 4180             |
| JSON        | `\n`        | Uses LF line endings               |
| JSON Lines  | `\n`        | Uses LF line endings per RFC 7464  |
| TOML        | Platform    | Uses default TextIOWrapper behavior |
| YAML        | `\n`        | Uses LF line endings               |

## API Reference

### Reading

| Function                                          | Description                          | Supported Formats             |
| ------------------------------------------------- | ------------------------------------ | ----------------------------- |
| `read_record_from_reader(reader, model, format)`  | Read single record from `BinaryIO`   | JSON, MessagePack, TOML, YAML |
| `read_record_from_file(path, model)`              | Read single record from file path    | JSON, MessagePack, TOML, YAML |
| `read_records_from_reader(reader, model, format)` | Read list of records from `BinaryIO` | All formats except for TOML   |
| `read_records_from_file(path, model)`             | Read list of records from file path  | All formats except for TOML   |

### Writing

| Function                                           | Description                         | Supported Formats             |
| -------------------------------------------------- | ----------------------------------- | ----------------------------- |
| `write_record_to_writer(writer, record, format)`   | Write single record to `BinaryIO`   | JSON, MessagePack, TOML, YAML |
| `write_record_to_file(path, record)`               | Write single record to file path    | JSON, MessagePack, TOML, YAML |
| `write_records_to_writer(writer, records, format)` | Write list of records to `BinaryIO` | All formats except for TOML   |
| `write_records_to_file(path, records)`             | Write list of records to file path  | All formats except for TOML   |

### Format Detection

When using `*_from_file` or `*_to_file` functions, the data format is automatically detected from the file extension:

```python
from pydanticio import read_records_from_file, write_records_to_file

# Auto-detects CSV format from .csv extension
users = read_records_from_file("data/users.csv", User)

# Auto-detects JSON Lines format from .jsonl extension
write_records_to_file("data/output.jsonl", users)
```

## Examples

### Reading and Writing Lists

```python
from pydantic import BaseModel
from pydanticio import read_records_from_file, write_records_to_file

class User(BaseModel):
    name: str
    age: int

# Convert between formats
users = read_records_from_file("users.csv", User)
write_records_to_file("users.json", users)
```

### Reading Single Records

```python
from pydantic import BaseModel
from pydanticio import read_record_from_file

class Config(BaseModel):
    name: str
    version: int
    enabled: bool

config = read_record_from_file("config.toml", Config)
print(config.name, config.version)
```

### Using Streams

```python
from pydantic import BaseModel
from pydanticio import read_records_from_reader, write_records_to_writer

class Item(BaseModel):
    id: int
    value: str

# Read from a file stream
with open("data.json", "rb") as f:
    items = read_records_from_reader(f, Item)

# Write to a BytesIO stream
from io import BytesIO
buffer = BytesIO()
write_records_to_writer(buffer, items, "json")
```

### Converting Between Formats

```bash
# Command line usage example
python examples/convert_format.py input.csv output.json
```

See `examples/convert_format.py` for the full source code.

## Requirements

- Python 3.12+
- Pydantic 2.5.0+

## License

MIT License
