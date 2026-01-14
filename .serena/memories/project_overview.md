# PydanticIO Project Overview

## Format Constraints
- **CSV**: Lists only (no single record support)
- **JSON Lines**: Lists only (no single record support)
- **JSON**: Single records and lists
- **YAML**: Single records and lists (requires pyyaml)

## Format Auto-Detection
| Extension | Format |
|-----------|--------|
| .csv | csv |
| .json | json |
| .jsonl, .jsl, .jl, .json_lines | json_lines |
| .yaml, .yml | yaml |
