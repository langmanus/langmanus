FROM ghcr.io/astral-sh/uv:python3.12-bookworm
WORKDIR /app
ENV CHROME_HEADLESS=True
COPY pyproject.toml uv.lock /app/

RUN touch README.md
RUN uv sync

RUN uv run playwright install chromium --only-shell --with-deps

COPY . /app

CMD ["uv", "run", "python", "server.py"]

