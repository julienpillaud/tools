.PHONY: help init check test cov lint

help:
	@echo "Available targets:"
	@echo "  init    - Set up dependencies and pre-commit hooks."
	@echo "  check   - Check outdated dependencies and update hooks."
	@echo "  test    - Run tests with pytest."
	@echo "  cov     - Run tests and generate coverage reports"
	@echo "  lint    - Format and check code with ruff and mypy."


init:
	uv sync --all-extras
	uv run pre-commit install

check:
	uv tree -d 1 --outdated
	uv run pre-commit autoupdate

test:
	uv run coverage run --source=src -m pytest

cov: test
	uv run coverage report --show-missing
	uv run coverage html

lint:
	uv run ruff format
	uv run ruff check
	uv run mypy .
