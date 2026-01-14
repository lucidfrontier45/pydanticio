# AGENTS.md

## Project Overview
PydanticIO is a tiny file IO utility library for Python powered by Pydantic. It provides functions to read and write Pydantic models from/to various data formats: CSV, JSON, JSON Lines, and YAML.

## Code and Command Execution
The Project is managed by `uv`. Scripts and tools including `ruff`, `pytest`, and `pyrefly` should be invoked by `uv`.
Example: `uv run poe check`, `uv run poe test`

## Code Structure
- `src/pydanticio/`: Main package
  - `__init__.py`: Main API functions (`read_record_from_*`, `read_records_from_*`, `write_record_to_*`, `write_records_to_*`)
  - `backends/`: Format-specific implementations
    - `__init__.py`: Backend exports and utilities
    - `csv.py`: CSV handling (only supports lists of records)
    - `json.py`: JSON handling for single records and lists
    - `json_lines.py`: JSON Lines handling (only supports lists of records)
    - `yaml.py`: YAML handling (requires pyyaml)
    - `yaml_stub.py`: Stub for when YAML is not installed
  - `version.py`: Version info

## Conventions
- Uses Pydantic v2 with `model_validate` and `model_dump`
- Type hints with generics for type safety
- Match statements for format dispatching
- RootModel for list serialization in JSON/YAML formats
- File extensions determine format automatically via `decide_data_format_from_path`
- Backends follow consistent `read_record`/`write_record` or `read_records`/`write_records` patterns

## Testing
Run tests with: `uv run poe test`
- Tests in `tests/` directory
- Each backend has its own test file
- Uses pytest fixtures and BytesIO for testing

## Linting and Type Checking
- Linting: `uv run poe check` (it also tries to auto-fix issues)
- Type checking: `uv run poe pyrefly_check`
- Configuration in `pyproject.toml`

## Code Formatting
- Formatting: `uv run poe format`
- Configuration in `pyproject.toml`

## Dependencies
- Python: >=3.12
- Core: pydantic>=2.5.0
- Optional: pyyaml>=5.1.0 for YAML support
- Dev: pyrefly>=0.46.0, pytest-cov>=7.0.0, ruff>=0.14.4

## Build System
Uses uv for building and dependency management. Build with `uv build`.

## Important Notes
- CSV and JSON Lines formats only support reading/writing lists of records, not single records
- JSON and YAML support both single records and lists
- Format auto-detection from file extension (.csv, .json, .jsonl/.jsl/.jl/.json_lines, .yaml/.yml)
- All backends use Pydantic's validation and serialization methods
- Library is designed to be simple and minimal, following the pattern of the Rust SerdeIO library
- Reader/writer functions work with `BinaryIO`, file path functions auto-handle opening/closing

## Common Patterns
- For single records: use `read_record_from_file` / `write_record_to_file`
- For lists: use `read_records_from_file` / `write_records_to_file`
- Format can be specified explicitly or auto-detected from path
