# LangManus

LangManus is an AI-powered automation framework that combines language models with specialized tools for tasks like web search, crawling, and Python code execution.

## Features

- 🤖 LLM-powered automation using Qwen/OpenAI
- 🔍 Web search capabilities via Tavily
- 🕷️ Web crawling support through Jina
- 🐍 Python code execution and REPL integration
- 📊 Workflow graph visualization and management

## Setup

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install Dependencies

LangManus leverages [uv](https://github.com/astral-sh/uv) as its package manager to streamline dependency management.
Follow the steps below to set up a virtual environment and install the necessary dependencies:

```bash
# Step 1: Create and activate a virtual environment
python -m venv .venv

# On Unix/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Step 2: Install project dependencies
uv sync
```

By completing these steps, you'll ensure your environment is properly configured and ready for development.

### Configure Environment Variables

LangManus uses a two-tier LLM system with separate configurations for supervisor and agent roles. Create a `.env` file in the project root and configure the following environment variables:

```ini
# Supervisor LLM Configuration (defaults to qwen-max-latest)
SUPERVISOR_MODEL=qwen-max-latest
SUPERVISOR_API_KEY=your_supervisor_api_key
SUPERVISOR_BASE_URL=your_custom_base_url  # Optional

# Agent LLM Configuration (defaults to qwen2.5-vl-72b-instruct)
AGENT_MODEL=qwen2.5-vl-72b-instruct
AGENT_API_KEY=your_agent_api_key
AGENT_BASE_URL=your_custom_base_url  # Optional

# Tool API Keys
TAVILY_API_KEY=your_tavily_api_key
JINA_API_KEY=your_jina_api_key  # Optional
```

> **Note:**
>
> - The system uses different models for supervision (Qwen-max by default) and agent tasks (Qwen-VL by default)
> - You can customize the base URLs for both supervisor and agent LLMs independently
> - Supervisor and agent can use different API keys if needed
> - Jina API key is optional. Provide your own key to access a higher rate limit
> - Tavily search is configured to return a maximum of 5 results by default

You can copy the `.env.example` file as a template to get started:

```bash
cp .env.example .env
```

## Usage

### Basic Execution

To run LangManus with default settings:

```bash
uv run main.py
```

### Advanced Configuration

LangManus can be customized through various configuration files in the `src/config` directory:
- `env.py`: Configure LLM models, API keys, and base URLs
- `tools.py`: Adjust tool-specific settings (e.g., Tavily search results limit)
- `agents.py`: Modify team composition and agent system prompts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
