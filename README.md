# Python Rye Template
A Project Template of Python with Rye

# Install

Please first install the latest Rye.
https://rye-up.com/guide/installation/

Then run the following command to install runtime libraries.

```bash
rye sync --no-dev --no-lock
```

# Develop

```bash
rye sync
```

This installs the following tools in addition to runtime libraries.

- pyright
- pytest-cov

The settings of those linter and formatters are written in `pyproject.toml`

# VSCode Settings

Install/activate all extensions listed in `.vscode/extensions.json`

# Creating Console Script

```toml
[project.scripts]
app = "app.cli:main"
```

# Define Project Command

```toml
[tool.rye.scripts]
pyright_lint = "pyright ."
rye_format = "rye format ."
rye_lint = "rye lint ."
rye_fix = "rye lint --fix ."
test = "pytest tests --cov=app --cov-report=term --cov-report=xml"
format = { chain = ["rye_fix", "rye_format"] }
lint = { chain = ["rye_lint", "pyright_lint"] }
check = { chain = ["format", "lint", "test"] }
```

# Build Docker Image

Please check the `Dockerfile` for how to use multi-stage build with Rye.

# Where is Ruff?

When you develop on VSCode, the Ruff extention already contains a Ruff executable.
When you develop on terminal, Rye contains a Ruff and `rye format/lint` uses it.