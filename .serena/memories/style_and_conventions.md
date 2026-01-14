# PydanticIO Style and Conventions

## Conventions
- Uses Pydantic v2 with `model_validate` and `model_dump`
- Type hints with generics for type safety
- Match statements for format dispatching
- RootModel for list serialization in JSON/YAML formats
- File extensions determine format automatically via `decide_data_format_from_path`
- Backends follow consistent `read_record`/`write_record` or `read_records`/`write_records` patterns

## Code Style

### General Principles
- **Minimal Code**: Follow the "simple and minimal" principle from the Rust SerdeIO library
- **No Comments**: Do NOT add any comments unless explicitly requested by the user
- **Type Hints**: Always use type hints for function signatures
- **Generics**: Use Python generics (`T: BaseModel`) for type-safe record handling

### Naming Conventions
- **Functions**: snake_case for function names (e.g., `read_record_from_file`, `write_records_to_writer`)
- **Variables**: snake_case for variable names
- **Constants**: UPPER_SNAKE_CASE for constants
- **Classes**: PascalCase for class names (e.g., `TestClass`, `RootModel`)
- **Type Aliases**: PascalCase for type aliases (e.g., `DataFormat`, `GenericDataFormat`)

### Import Style
- Use absolute imports from the package root
- Group imports: standard library, third-party, local
- Use aliases for backend modules (e.g., `from .backends import json as json_backend`)

## Pydantic Patterns

### Model Validation
- Use `model_validate()` for parsing data into models (Pydantic v2)
- Use `model_validate_json()` for parsing JSON strings directly
- Use `model_dump()` for converting models to dictionaries
- Use `model_dump_json()` for converting models to JSON strings

### RootModel for Lists
- Use `RootModel[list[T]]` when serializing/deserializing lists of records
- Access the list via `.root` attribute (e.g., `list_model(root=records)`)

### Model Configuration
- Use `model_config = ConfigDict(frozen=True)` for immutable models
- Access model fields via `model.model_fields.keys()`

## Backend Pattern

### Structure
Each backend should implement:
- `read_record[T: BaseModel](reader: TextIO, model: type[T]) -> T` (for single record formats)
- `read_records[T: BaseModel](reader: TextIO, model: type[T]) -> list[T]` (for list formats)
- `write_record(writer: TextIO, record: BaseModel) -> None` (for single record formats)
- `write_records(writer: TextIO, records: Iterable[BaseModel]) -> None` (for list formats)

### File Naming
- Backend files should be named after their format (e.g., `json.py`, `csv.py`, `yaml.py`)
- Stub files should be named `<format>_stub.py` (e.g., `yaml_stub.py`)

### Stub Pattern
For optional backends (like YAML), create a stub that raises `NotImplementedError` when the dependency is not available.

## Format Dispatching

### Using Match Statements
Use Python match statements for format dispatching:
```python
match data_format:
    case "json":
        return json_backend.read_record(reader, model)
    case "yaml":
        return yaml_backend.read_record(reader, model)
    case _:
        raise ValueError(f"Unsupported backend type: {data_format}")
```

### Auto-detection from Path
Use `decide_data_format_from_path()` to determine format from file extension:
- `.csv` -> "csv"
- `.jsonl`, `.jsl`, `.jl`, `.json_lines` -> "json_lines"
- `.json` -> "json"
- `.yaml`, `.yml` -> "yaml"

## Error Handling

### Value Errors
Raise `ValueError` for unsupported formats or types:
```python
raise ValueError(f"Unsupported backend type: {data_format}")
raise ValueError(f"Unsupported file extension: {file_path.suffix}")
```

### Not Implemented
Raise `NotImplementedError` for stubs:
```python
raise NotImplementedError("yaml backend is not available.")
```

## Testing Patterns

### Test Fixtures
- Use `TestClass` as the standard test model (defined in `tests/__init__.py`)
- Use `test_records` list for testing multiple records
- Use `StringIO` for testing TextIO operations

### Test Structure
- One test file per backend (e.g., `test_json.py`, `test_csv.py`)
- Tests for reader functions: `test_read_*`
- Tests for writer functions: `test_write_*`
- Tests for both single records and lists

## File Structure

```
src/pydanticio/
├── __init__.py          # Main API with public functions
├── backends/
│   ├── __init__.py      # Backend exports and utilities
│   ├── csv.py           # CSV backend (lists only)
│   ├── json.py          # JSON backend (single + lists)
│   ├── json_lines.py    # JSON Lines backend (lists only)
│   ├── yaml.py          # YAML backend (single + lists)
│   └── yaml_stub.py     # YAML stub when pyyaml unavailable
└── version.py           # Version info
```

## Configuration Files

### pyproject.toml
- Python 3.12+ target
- ruff linting with specific rule sets
- pyrefly type checking configuration
- pytest configuration to ignore FutureWarning

### Ruff Configuration
- Target Python version: 3.12
- Extensive rule set: E, F, W, I, B, RUF, UP, N, SIM, A, S, DTZ, PIE, PLE
- Exclude directories: tests/**/*, deps/**/*
- Per-file ignores: `__init__.py` can have unused imports (F401)
