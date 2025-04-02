.PHONY: help init pre-commit tests coverage lint

help:
	@echo "Available commands:"
	@echo "  init       - Install dependencies and pre-commit hooks"
	@echo "  pre-commit - Run pre-commit hooks on all files"
	@echo "  tests      - Run tests"
	@echo "  coverage   - Run tests with coverage"
	@echo "  lint       - Format and check code"

init:
	uv sync --all-extras
	uv run pre-commit install

pre-commit:
	uv run pre-commit run --all-files

tests:
	uv run pytest

coverage:
	uv run coverage run --source=src -m pytest
	uv run coverage report --show-missing
	uv run coverage html

lint:
	uv run ruff format
	uv run ruff check --fix || true
	uv run pyright
