# Development Workflow

## Quality Gates
Before committing:
- [ ] `uv run poe check` passes (linting + type checking)
- [ ] `uv run pytest` passes (all tests)
- [ ] `uv build` succeeds

## Quick Check
```bash
uv run poe check && uv run pytest
```

## Adding Features
1. Add backend file in `src/pydanticio/backends/` if new format
2. Update main API in `src/pydanticio/__init__.py`
3. Update format detection in `decide_data_format_from_path()` if new extension
4. Add tests in `tests/`
5. Run quality gates

## Fixing Bugs
1. Add regression test that fails before fix
2. Implement fix
3. Verify test passes
4. Run quality gates

## Commit Style
- `feat: description`
- `fix: description`
- `docs: description`
- `refactor: description`
- `test: description`
- `chore: description`
