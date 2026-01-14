# PydanticIO Project Overview

## Purpose
PydanticIO (pronounce pidantisio) is a tiny file IO utility library for Python powered by Pydantic. This library is a port of the Rust library [SerdeIO](https://github.com/lucidfrontier45/serdeio). It provides functions to read and write Pydantic models from/to various data formats: CSV, JSON, JSON Lines, and YAML.

## Tech Stack
- **Language**: Python 3.12+
- **Core Dependencies**: pydantic>=2.5.0
- **Optional Dependencies**: pyyaml>=5.1.0 (for YAML support)
- **Package Manager**: uv
- **Testing Framework**: pytest with pytest-cov
- **Linting**: ruff>=0.14.4
- **Type Checking**: pyrefly>=0.46.0
- **Build System**: uv_build

## Supported Formats
- **CSV**: By stdlib `csv` module (lists only)
- **JSON**: By stdlib `json` module (single records and lists)
- **JSON Lines**: By stdlib `json` module (lists only)
- **YAML**: By `pyyaml` library (optional feature)

## Key Design Patterns
- **Format Auto-detection**: File extensions determine format automatically via `decide_data_format_from_path`
- **Generic Type Safety**: Uses Python generics for type-safe record handling
- **Match Statements**: Format dispatching using Python match statements
- **RootModel**: Used for list serialization in JSON/YAML formats
- **Backend Pattern**: Format-specific implementations in `backends/` directory
- **Stub Pattern**: YAML stub for graceful handling when pyyaml is not installed

## File Structure
```
src/pydanticio/
├── __init__.py          # Main API with public functions
├── backends/
│   ├── __init__.py      # Backend exports and utilities
│   ├── csv.py           # CSV backend (lists only)
│   ├── json.py          # JSON backend (single + lists)
│   ├── json_lines.py    # JSON Lines backend (lists only)
│   ├── yaml.py          # YAML backend (single + lists, requires pyyaml)
│   └── yaml_stub.py     # YAML stub when pyyaml unavailable
└── version.py           # Version info
```

## API Functions
- `read_record_from_reader`: Read single record from TextIO
- `read_records_from_reader`: Read list of records from TextIO
- `read_record_from_file`: Read single record from file path
- `read_records_from_file`: Read list of records from file path
- `write_record_to_writer`: Write single record to TextIO
- `write_records_to_writer`: Write list of records to TextIO
- `write_record_to_file`: Write single record to file path
- `write_records_to_file`: Write list of records to file path

## Important Notes
- CSV and JSON Lines formats only support reading/writing lists of records, not single records
- JSON and YAML support both single records and lists
- Format can be specified explicitly or auto-detected from path
- All backends use Pydantic's `model_validate` and `model_dump`/`model_dump_json` methods
- Reader/writer functions work with `BinaryIO`, file path functions auto-handle opening/closing
- Format auto-detection from file extension (.csv, .json, .jsonl/.jsl/.jl/.json_lines, .yaml/.yml)

## Common Patterns
- For single records: use `read_record_from_file` / `write_record_to_file`
- For lists: use `read_records_from_file` / `write_records_to_file`
- Format can be specified explicitly or auto-detected from path
