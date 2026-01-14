# AGENTS.md

## Project Overview
PydanticIO is a tiny file IO utility library for Python powered by Pydantic. It provides functions to read and write Pydantic models from/to CSV, JSON, JSON Lines, and YAML.

## Code and Command Execution
The Project is managed by `uv`. Run tools via `uv run`.

- Linting + Type checking: `uv run poe check`
- Formatting: `uv run poe format`
- Testing: `uv run pytest`

## Coding Standards

### General
- Do NOT add comments unless explicitly requested
- Always use type hints for function signatures
- Use Python generics (`T: BaseModel`) for type-safe record handling

### Naming
- snake_case for functions and variables
- UPPER_SNAKE_CASE for constants
- PascalCase for classes and type aliases

### Pydantic Patterns
- Use `model_validate()` for parsing data into models
- Use `model_dump()` for converting models to dictionaries
- Use `model_dump_json()` for converting models to JSON strings

### Backend Pattern
- Use match statements for format dispatching
- Use `RootModel[list[T]]` for list serialization in JSON/YAML
- Backends follow consistent `read_record`/`write_record` or `read_records`/`write_records` patterns
