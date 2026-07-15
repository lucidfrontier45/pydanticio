---
name: pydanticio-api
description: Use the `pydanticio` library to read and write Pydantic `BaseModel` instances from/to files. Triggers when the user mentions pydanticio, wants to serialize/deserialize Pydantic models to disk, convert between CSV/JSON/JSONL/YAML/TOML/MessagePack/CBOR, read structured config files into typed models, or build ETL over typed records. Use this skill even when the user doesn't name pydanticio explicitly but clearly wants type-safe Pydantic file I/O or format conversion between structured file formats. Do NOT use for raw dict I/O without models, pandas DataFrames, or general JSON/dict manipulation unrelated to Pydantic.
---

# pydanticio API

`tiny Python lib for reading/writing Pydantic models to files`. Supports CSV, JSON, JSON Lines, YAML, TOML, MessagePack, CBOR. Format auto-detected from file extension, overridable via `data_format=`. Optional deps per backend (see Backend section).

## Public API (8 functions)

All take a `model: type[T]` (or `record: T`) plus either a file path (`str | Path`) or a `BinaryIO` stream + explicit `data_format`. Always returns/writes UTF-8 binary streams internally.

| Function | Reads/Writes | Supports |
|---|---|---|
| `read_record_from_file(path, Model, data_format=None)` | one record | json, yaml, toml, messagepack, cbor |
| `read_records_from_file(path, Model, data_format=None)` | list of records | json, yaml, csv, json_lines, messagepack, cbor |
| `read_record_from_reader(BinaryIO, Model, format)` | one record | json, yaml, toml, messagepack, cbor |
| `read_records_from_reader(BinaryIO, Model, format)` | list of records | json, yaml, csv, json_lines, messagepack, cbor |
| `write_record_to_file(path, record, data_format=None)` | one record | json, yaml, toml, messagepack, cbor |
| `write_records_to_file(path, records, data_format=None)` | list | json, yaml, csv, json_lines, messagepack, cbor |
| `write_record_to_writer(BinaryIO, record, format)` | one record | json, yaml, toml, messagepack, cbor |
| `write_records_to_writer(BinaryIO, records, format)` | list | json, yaml, csv, json_lines, messagepack, cbor |

## Format support matrix

| format value | extensions | single | list | dep |
|---|---|---|---|---|
| `"json"` | `.json` | yes | yes | builtin |
| `"yaml"` | `.yaml`, `.yml` | yes | yes | `pyyaml` |
| `"toml"` | `.toml` | yes | **no** | `tomlkit` |
| `"csv"` | `.csv` | **no** | yes | builtin |
| `"json_lines"` | `.jsonl`, `.jl`, `.jsl`, `.json_lines` | **no** | yes | builtin |
| `"messagepack"` | `.msgpack` | yes | yes | `msgpack` |
| `"cbor"` | `.cbor` | yes | yes | `cbor2` |

Mismatching single↔list with an incompatible format raises `ValueError` (e.g., `read_records_from_file(..., data_format="toml")` or `read_record_from_file(..., data_format="csv")`).

## Patterns

### Auto-detect from extension (default)

```python
from pydanticio import read_records_from_file, write_records_to_file

class User(BaseModel):
    name: str
    age: int

users = read_records_from_file("users.csv", User)
write_records_to_file("users.json", users)
```

### Override extension with `data_format=`

```python
# read CSV from a .txt file
users = read_records_from_file("users.txt", User, data_format="csv")
# write JSON to a non-standard extension
write_records_to_file("export.xyz", users, data_format="json")
```

### Stream I/O with explicit format

`read_*_from_reader` / `write_*_to_writer` require `data_format` (no path to inspect).

```python
from io import BytesIO
from pydanticio import read_records_from_reader, write_records_to_writer

with open("data.json", "rb") as f:
    items = read_records_from_reader(f, Item, data_format="json")

buf = BytesIO()
write_records_to_writer(buf, items, data_format="json")
```

### Single record (config-style)

```python
from pydanticio import read_record_from_file, write_record_to_file

class Config(BaseModel):
    name: str
    version: int
    enabled: bool

config = read_record_from_file("config.toml", Config)
write_record_to_file("config.yaml", config)
```

## Decision rules

- **Have a path?** Use `read_*_from_file` / `write_*_to_file` — let extension drive format. Pass `data_format=` only to override.
- **Have a stream?** Use `read_*_from_reader` / `write_*_to_writer` — must pass `data_format`.
- **List or single?** Pick API accordingly. Single + list-incompatible format (toml/csv/json_lines) raises.
- **Iterables for write**: `write_records_*` accepts any `Iterable[BaseModel]` — materializes via `list()` for binary formats, wraps in `RootModel[Iterable[T]]` for JSON/YAML.

## Pitfalls

- Optional backends (`yaml`, `toml`, `messagepack`, `cbor`) raise `ImportError` on import if extra not installed. Suggest `pip install pydanticio[yaml]` etc., or check `pip show`.
- `RootModel[list[T]]` is used internally for JSON/YAML lists — fields are dumped with `model_dump(mode="json")`, so non-JSON-native types (datetimes, enums, decimals) serialize via their JSON representation. Add custom serializers if format fidelity matters.
- File paths are opened in binary mode (`"rb"`/`"wb"`) — text decoding is backend's job.
- Newline conventions: CSV → `\r\n` (RFC 4180), JSONL → `\n` (RFC 7464), JSON/YAML → `\n`, TOML → platform default.
- No `csv` backend for single record (CSV is inherently tabular). No `toml` for list of records (TOML is single-document).

## Format conversion

The whole point — read in one format, write in another. Model defines the target shape; backends handle format quirks.

```python
users = read_records_from_file("input.csv", User)
write_records_to_file("output.json", users)
write_records_to_file("output.yaml", users)
write_records_to_file("output.msgpack", users)
```

CLI usage mirrors `examples/convert_format.py`:

```bash
python examples/convert_format.py input.csv output.json
```

## Verification

After reading/writing, round-trip the data: read the produced file back into a fresh list of models and compare key fields. If a custom serializer/deserializer is needed for a field type, test it through the actual backend before relying on it.