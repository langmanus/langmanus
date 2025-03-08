# Manus

## Setup

### Install Dependencies

Manus utilizes [uv](https://github.com/astral-sh/uv) as its package manager. To get started, set up a virtual environment and install the required dependencies using `uv`:

```bash
uv sync
```

### Configure Environment Variables

Manus relies on the following APIs by default:
- [**OpenAI**](https://platform.openai.com/api-keys): Serves as the LLM (Large Language Model) provider.
- [**Tavily**](https://tavily.com/): Facilitates web search functionality.
- [**Jina**](https://jina.ai/): Enables web crawling capabilities.

To ensure proper functionality, you need to define the following environment variables:

```plaintext
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
JINA_API_KEY=your_jina_api_key
```

> If you wish to use a custom OpenAI API provider, you can specify the base URL by setting the `OPENAI_BASE_URL` environment variable.
> Jina API key is optional. Provide your Jina API key to access a higher rate limit.

---

## Usage

To execute the script, simply run:

```bash
uv run main.py
```
