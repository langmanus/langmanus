.PHONY: lint format install-dev serve test coverage

install-dev:
	uv pip install -e ".[dev]" && uv pip install -e ".[test]"

format:
	black --preview .

lint:
	black --check .

serve:
	uv run server.py

test:
	uv run pytest tests/

coverage:
	uv run pytest --cov=src tests/ --cov-report=term-missing
