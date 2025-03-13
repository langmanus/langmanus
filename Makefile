.PHONY: lint format install-dev serve

install-dev:
	pip install -e ".[dev]"

format:
	black --preview .

lint:
	black --check .

serve:
	python server.py
