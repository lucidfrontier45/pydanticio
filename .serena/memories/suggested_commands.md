# Suggested Commands for PydanticIO Development

## Package Management (uv)

```bash
# Install project with dependencies
uv sync

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Remove a dependency
uv remove <package>

# Build the package
uv build

# Run a command in the project environment
uv run <command>
```

## Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=pydanticio

# Run specific test file
pytest tests/test_json.py

# Run tests in verbose mode
pytest -v
```

## Linting

```bash
# Check for linting errors
ruff check .

# Auto-fix linting errors
ruff check . --fix

# Check specific file
ruff check src/pydanticio/__init__.py
```

## Formatting

```bash
# Format code
ruff format .

# Check formatting without changes
ruff format . --check
```

## Type Checking

```bash
# Type check source and tests
pyrefly check src

# Type check specific directory
pyrefly check src/pydanticio/
```

## Combined Quality Checks

```bash
# Run linting, formatting check, and type checking
ruff check . && ruff format . --check && pyrefly check src

# Run all checks and tests
ruff check . && ruff format . --check && pyrefly check src && pytest
```

## Running Examples

```bash
# Run example scripts
uv run python examples/example.py
```

## Git Commands

```bash
# Check git status
git status

# View staged and unstaged changes
git diff

# View recent commits
git log --oneline -10

# Create a new branch
git checkout -b <branch-name>

# Stage changes
git add <file>

# Commit changes
git commit -m "message"
```

## File Operations

```bash
# List files in directory
ls -la

# Find files by pattern
find . -name "*.py"

# Search for pattern in files
grep -r "pattern" --include="*.py"
```

## Development Workflow

1. Make changes to the code
2. Run `ruff check . --fix` to auto-fix linting issues
3. Run `ruff format .` to format code
4. Run `pyrefly check src` to verify types
5. Run `pytest` to ensure tests pass
6. Commit changes with clear commit messages
