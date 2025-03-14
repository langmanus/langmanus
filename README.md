# LangManus

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](./README.md) | [简体中文](./README_zh.md)

> Come From Open Source, Back to Open Source

LangManus is a community-driven AI automation framework that builds upon the incredible work of the open source community. Our goal is to combine language models with specialized tools for tasks like web search, crawling, and Python code execution, while giving back to the community that made this possible.

## Table of Contents
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Features](#features)
- [Why LangManus?](#why-langmanus)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/langmanus/langmanus.git
cd langmanus

# Create and activate virtual environment through uv
uv python install 3.12
uv venv --python 3.12

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the project
uv run main.py
```

## Architecture

LangManus implements a hierarchical multi-agent system where a supervisor coordinates specialized agents to accomplish complex tasks:

![LangManus Architecture](./assets/architecture.jpeg)

The system consists of:
- **Supervisor**: Orchestrates the workflow and delegates tasks
- **Researcher**: Handles web searches and information gathering
- **Coder**: Manages code generation and modification
- **File Manager**: Handles file system operations
- **Browser**: Performs web crawling and interaction

## Features

### Core Capabilities
- 🤖 **LLM Integration**
  - Support for open source models like Qwen
  - OpenAI-compatible API interface
  - Multi-tier LLM system for different task complexities

### Tools and Integrations
- 🔍 **Search and Retrieval**
  - Web search via Tavily API
  - Neural search with Jina
  - Advanced content extraction

### Development Features
- 🐍 **Python Integration**
  - Built-in Python REPL
  - Code execution environment
  - Package management with uv

### Workflow Management
- 📊 **Visualization and Control**
  - Workflow graph visualization
  - Multi-agent orchestration
  - Task delegation and monitoring

## Why LangManus?

We believe in the power of open source collaboration. This project wouldn't be possible without the amazing work of projects like:
- [Qwen](https://github.com/QwenLM/Qwen) for their open source LLMs
- [Tavily](https://tavily.com/) for search capabilities
- [Jina](https://jina.ai/) for neural search technology
- And many other open source contributors

We're committed to giving back to the community and welcome contributions of all kinds - whether it's code, documentation, bug reports, or feature suggestions.

## Setup

### Prerequisites

- [uv](https://github.com/astral-sh/uv) package manager

### Installation

LangManus leverages [uv](https://github.com/astral-sh/uv) as its package manager to streamline dependency management.
Follow the steps below to set up a virtual environment and install the necessary dependencies:

```bash
# Step 1: Create and activate a virtual environment through uv
uv python install 3.12
uv venv --python 3.12

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Step 2: Install project dependencies
uv sync
```

By completing these steps, you'll ensure your environment is properly configured and ready for development.

### Configuration

LangManus uses a three-tier LLM system with separate configurations for reasoning, basic tasks, and vision-language tasks. Create a `.env` file in the project root and configure the following environment variables:

```ini
# Reasoning LLM Configuration (for complex reasoning tasks)
REASONING_MODEL=your_reasoning_model
REASONING_API_KEY=your_reasoning_api_key
REASONING_BASE_URL=your_custom_base_url  # Optional

# Basic LLM Configuration (for simpler tasks)
BASIC_MODEL=your_basic_model
BASIC_API_KEY=your_basic_api_key
BASIC_BASE_URL=your_custom_base_url  # Optional

# Vision-Language LLM Configuration (for tasks involving images)
VL_MODEL=your_vl_model
VL_API_KEY=your_vl_api_key
VL_BASE_URL=your_custom_base_url  # Optional

# Tool API Keys
TAVILY_API_KEY=your_tavily_api_key
JINA_API_KEY=your_jina_api_key  # Optional

# Browser Configuration
CHROME_INSTANCE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome  # Optional, path to Chrome executable
```

> **Note:**
>
> - The system uses different models for different types of tasks:
>   - Reasoning LLM for complex decision-making and analysis
>   - Basic LLM for simpler text-based tasks
>   - Vision-Language LLM for tasks involving image understanding
> - You can customize the base URLs for all LLMs independently
> - Each LLM can use different API keys if needed
> - Jina API key is optional. Provide your own key to access a higher rate limit
> - Tavily search is configured to return a maximum of 5 results by default

You can copy the `.env.example` file as a template to get started:

```bash
cp .env.example .env
```

### Configure Pre-commit Hook
LangManus includes a pre-commit hook that runs linting and formatting checks before each commit. To set it up:

1. Make the pre-commit script executable:
```bash
chmod +x pre-commit
```

2. Install the pre-commit hook:
```bash
ln -s ../../pre-commit .git/hooks/pre-commit
```

The pre-commit hook will automatically:
- Run linting checks (`make lint`)
- Run code formatting (`make format`)
- Add any reformatted files back to staging
- Prevent commits if there are any linting or formatting errors

## Usage

### Basic Execution

To run LangManus with default settings:

```bash
uv run main.py
```

### API Server

LangManus provides a FastAPI-based API server with streaming support:

```bash
# Start the API server
make serve

# Or run directly
uv run server.py
```

The API server exposes the following endpoints:

- `POST /api/chat/stream`: Chat endpoint for LangGraph invoke with streaming support
  - Request body:
    ```json
    {
      "messages": [
        {"role": "user", "content": "Your query here"}
      ],
      "debug": false
    }
    ```
  - Returns a Server-Sent Events (SSE) stream with the agent's responses

### Advanced Configuration

LangManus can be customized through various configuration files in the `src/config` directory:
- `env.py`: Configure LLM models, API keys, and base URLs
- `tools.py`: Adjust tool-specific settings (e.g., Tavily search results limit)
- `agents.py`: Modify team composition and agent system prompts

### Agent Prompts System

LangManus uses a sophisticated prompting system in the `src/prompts` directory to define agent behaviors and responsibilities:

#### Core Agent Roles

- **Supervisor ([`src/prompts/supervisor.md`](src/prompts/supervisor.md))**: Coordinates the team and delegates tasks by analyzing requests and determining which specialist should handle them. Makes decisions about task completion and workflow transitions.

- **Researcher ([`src/prompts/researcher.md`](src/prompts/researcher.md))**: Specializes in information gathering through web searches and data collection. Uses Tavily search and web crawling capabilities while avoiding mathematical computations or file operations.

- **Coder ([`src/prompts/coder.md`](src/prompts/coder.md))**: Professional software engineer role focused on Python and bash scripting. Handles:
  - Python code execution and analysis
  - Shell command execution
  - Technical problem-solving and implementation

- **File Manager ([`src/prompts/file_manager.md`](src/prompts/file_manager.md))**: Handles all file system operations with a focus on properly formatting and saving content in markdown format.

- **Browser ([`src/prompts/browser.md`](src/prompts/browser.md))**: Web interaction specialist that handles:
  - Website navigation
  - Page interaction (clicking, typing, scrolling)
  - Content extraction from web pages

#### Prompt System Architecture

The prompts system uses a template engine ([`src/prompts/template.py`](src/prompts/template.py)) that:
- Loads role-specific markdown templates
- Handles variable substitution (e.g., current time, team member information)
- Formats system prompts for each agent

Each agent's prompt is defined in a separate markdown file, making it easy to modify behavior and responsibilities without changing the underlying code.

## Development

### Testing

Run the test suite:

```bash
# Run all tests
make test

# Run specific test file
pytest tests/integration/test_workflow.py

# Run with coverage
make coverage
```

### Code Quality

```bash
# Run linting
make lint

# Format code
make format
```

## Contributing

We welcome contributions of all kinds! Whether you're fixing a typo, improving documentation, or adding a new feature, your help is appreciated. Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to all the open source projects and contributors that make LangManus possible. We stand on the shoulders of giants.
