# Code Standards

## Backend Structure
Each backend implements:
- `read_record[T: BaseModel](reader: TextIO, model: type[T]) -> T` (single record formats)
- `read_records[T: BaseModel](reader: TextIO, model: type[T]) -> list[T]` (list formats)
- `write_record(writer: TextIO, record: BaseModel) -> None`
- `write_records(writer: TextIO, records: Iterable[BaseModel]) -> None`

## Stub Pattern
For optional backends (e.g., YAML), create a stub file that raises `NotImplementedError`:
```python
raise NotImplementedError("yaml backend is not available.")
```

## Error Handling
```python
raise ValueError(f"Unsupported backend type: {data_format}")
raise ValueError(f"Unsupported file extension: {file_path.suffix}")
```
