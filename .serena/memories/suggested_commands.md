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
uv run pytest

# Run tests with coverage
uv run pytest --cov=pydanticio

# Run specific test file
uv run pytest tests/test_json.py

# Run tests in verbose mode
uv run pytest -v
```

## Linting and Type Checking

```bash
# Linting and type checking (auto-fix linting errors)
uv run poe check
```

## Formatting

```bash
# Format code
uv run poe format
```

## Combined Quality Checks

```bash
# Run linting, formatting check, and type checking
uv run poe check

# Run all checks and tests
uv run poe check && uv run pytest
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
2. Run `uv run poe check` to auto-fix linting and formatting issues
3. Run `uv run poe check` to verify types
4. Run `uv run pytest` to ensure tests pass
5. Commit changes with clear commit messages
