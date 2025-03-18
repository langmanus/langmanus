.PHONY: lint format install-dev serve test coverage

install-dev:
	pip install -e ".[dev]"

format:
	black --preview .

lint:
	black --check .

serve:
	uv run server.py

test:
	pytest tests/

coverage:
	pytest --cov=src tests/ --cov-report=term-missing
