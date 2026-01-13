# Task Completion Checklist for PydanticIO

## Before Committing Changes

### 1. Run Linting
```bash
ruff check . --fix
```
- Auto-fixes most linting issues
- Check for any remaining issues that require manual attention

### 2. Run Code Formatting
```bash
ruff format .
```
- Ensures consistent code style
- Run this after linting fixes

### 3. Run Type Checking
```bash
pyrefly check src
```
- Verifies type correctness
- Fix any type errors before proceeding

### 4. Run Tests
```bash
pytest
```
- Ensures all tests pass
- Add new tests for new functionality
- Verify coverage with `pytest --cov=pydanticio`

### 5. Verify Build
```bash
uv build
```
- Ensures the package builds correctly
- Check for any build errors

## Quality Gates

All changes should pass these checks before being considered complete:
- [ ] `ruff check .` passes with no errors
- [ ] `ruff format .` makes no changes (code is properly formatted)
- [ ] `pyrefly check src` passes with no errors
- [ ] `pytest` passes all tests
- [ ] `uv build` succeeds

## Code Review Checklist

- [ ] Code follows project conventions (no comments, type hints, generics)
- [ ] Changes are backward-compatible (or references are updated)
- [ ] New functionality has tests
- [ ] Documentation is updated if needed
- [ ] Commit message is clear and descriptive

## Common Commands Sequence

### Quick Check (before committing)
```bash
ruff check . --fix && ruff format . --check && pyrefly check src && pytest
```

### Full Quality Check
```bash
ruff check . --fix && ruff format . && pyrefly check src && pytest --cov=pydanticio && uv build
```

## When Adding New Features

1. **Add backend file** in `src/pydanticio/backends/` if new format
2. **Update main API** in `src/pydanticio/__init__.py`:
   - Add import for new backend
   - Add type aliases if needed
   - Add dispatch functions using match statements
3. **Update format detection** in `decide_data_format_from_path()` if new extension
4. **Add tests** in `tests/` directory
5. **Update README.md** if user-facing API changes
6. **Run all checks** before committing

## When Fixing Bugs

1. **Add regression test** that fails before the fix
2. **Implement fix**
3. **Verify test passes** with the fix
4. **Run full quality check** before committing

## Commit Message Style

Follow conventional commits:
- `feat: add new feature description`
- `fix: bug fix description`
- `docs: documentation updates`
- `refactor: code refactoring`
- `test: adding or updating tests`
- `chore: maintenance tasks`

Keep messages concise but descriptive. Focus on the "why" rather than the "what".
