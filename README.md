# Manus

Manus is an AI-powered automation framework that combines language models with specialized tools for tasks like web search, crawling, and Python code execution.

## Features

- 🤖 LLM-powered automation using OpenAI
- 🔍 Web search capabilities via Tavily
- 🕷️ Web crawling support through Jina
- 🐍 Python code execution and REPL integration
- 📊 Workflow graph visualization and management

## Setup

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install Dependencies

Manus utilizes [uv](https://github.com/astral-sh/uv) as its package manager. To get started, set up a virtual environment and install the required dependencies:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# OR
.venv\Scripts\activate     # On Windows

# Install dependencies
uv sync
```

### Configure Environment Variables

Manus relies on the following APIs by default:
<<<<<<< HEAD
- [**OpenAI**](https://platform.openai.com/api-keys): Serves as the LLM (Large Language Model) provider.
- [**Tavily**](https://tavily.com/): Facilitates web search functionality.
- [**Jina**](https://jina.ai/): Enables web crawling capabilities.
=======
- **OpenAI**: Serves as the LLM (Large Language Model) provider
- **Tavily**: Facilitates web search functionality
- **Jina**: Enables web crawling capabilities
>>>>>>> feat: refactor the project structure

Create a `.env` file in the project root and configure the following environment variables:

```plaintext
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
JINA_API_KEY=your_jina_api_key

<<<<<<< HEAD
> If you wish to use a custom OpenAI API provider, you can specify the base URL by setting the `OPENAI_BASE_URL` environment variable.
> Jina API key is optional. Provide your Jina API key to access a higher rate limit.
=======
# Optional: Custom OpenAI API base URL
OPENAI_BASE_URL=your_custom_openai_endpoint  # Optional
```
>>>>>>> feat: refactor the project structure

You can copy the `.env.example` file as a template:
```bash
cp .env.example .env
```

## Usage

### Basic Execution

To run Manus with default settings:

```bash
uv run main.py
```

### Advanced Configuration

Manus can be customized through various configuration options in the `src/config` directory:
- `tools.py`: Configure available tools and their settings
- `env.py`: Manage environment variables and API configurations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
