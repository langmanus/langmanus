# FAQ

## Table of Contents

- [Which models does LangManus support?](#which-models-does-langmanus-support)
- [How to deploy the Web UI frontend project?](#how-to-deploy-the-web-ui-frontend-project)
- [Can I use my local Chrome browser as the Browser Tool?](#can-i-use-my-local-chrome-browser-as-the-browser-tool)

## Which models does LangManus support?

In LangManus, we categorize models into three types:

### 1. **Chat Model**
- **Usage**: For conversation scenarios, mainly called in **Supervisor** and **Agent**.
- **Supported Models**: `gpt-4o`, `qwen-max-latest`, `gemini-2.0-flash`, `deepseek-v3`.

### 2. **Reasoning Model**
- **Usage**: For complex reasoning tasks, used in **Planner** when **"Deep Think"** mode is enabled.
- **Supported Models**: `o1`, `o3-mini`, `QwQ-Plus`, `DeepSeek-R1`, `gemini-2.0-flash-thinking-exp`.

### 3. **VL Model** (Vision-Language Model)
- **Usage**: For handling tasks combining vision and language, mainly called in **Browser Tool**.
- **Supported Models**: `gpt-4o`, `qwen2.5-vl-72b-instruct`, `gemini-2.0-flash`.

### How to switch models?

You can switch models by modifying the `.env` file in the project root directory. For specific configuration methods, please refer to [README.md](https://github.com/langmanus/langmanus/blob/main/README.md).

### How to use Ollama models in LangManus?

LangManus supports integration with Ollama models. To use an Ollama model, you need to:
1. Prefix the model name with `ollama_chat/`
2. Configure the correct base URL for your Ollama server

Here's an example of the environment configuration for using Ollama models:

```
BASIC_API_KEY=
BASIC_BASE_URL=http://localhost:11434
BASIC_MODEL=ollama_chat/qwen2.5:0.5b
```

### How to use OpenRouter models in LangManus?

LangManus supports integration with OpenRouter models. To use an OpenRouter model, you need to:
1. Obtain your OPENROUTER_API_KEY from OpenRouter (https://openrouter.ai/)
2. Prefix the model name with `openrouter/`
3. Configure the correct base URL for OpenRouter

Here's an example of the environment configuration for using OpenRouter models:

```
BASIC_API_KEY=OPENROUTER_API_KEY
BASIC_BASE_URL=https://openrouter.ai/api/v1
BASIC_MODEL=openrouter/anthropic/claude-3-opus
```

Note: Available models and their exact names may change over time. Please verify the current model offerings and their correct identifiers at [OpenRouter's website](https://openrouter.ai/docs).

### How to use Google Gemini models in LangManus?

LangManus supports integration with Google's Gemini models. To use a Gemini model, follow these steps:

1. Obtain your Gemini API key from Google AI Studio (https://makersuite.google.com/app/apikey)
2. Configure your environment variables as follows:

```
BASIC_API_KEY=YOUR_GEMINI_KEY
BASIC_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
BASIC_MODEL=gemini-2.0-flash
```

Note:
- Replace `YOUR_GEMINI_KEY` with your actual Gemini API key
- The base URL is specifically configured to use Gemini through LangManus's OpenAI-compatible interface
- Available models include `gemini-2.0-flash` for chat and vision tasks

---

## How to deploy the Web UI frontend project?

LangManus provides an out-of-the-box Web UI frontend project. You can complete the deployment through the following steps. Please visit the [LangManus Web UI GitHub repository](https://github.com/langmanus/langmanus-web) for more information.

### Step 1: Start the LangManus backend service

First, ensure you have cloned and installed the LangManus backend project. Enter the backend project directory and start the service:

```bash
cd langmanus
make serve
```

By default, the LangManus backend service will run on `http://localhost:8000`.

---

### Step 2: Install the Web UI frontend project and its dependencies

Next, clone the LangManus Web UI frontend project and install dependencies:

```bash
git clone https://github.com/langmanus/langmanus-web.git
cd langmanus-web
pnpm install
```

> **Note**: If you haven't installed `pnpm` yet, please install it first. You can install it using the following command:
> ```bash
> npm install -g pnpm
> ```

---

### Step 3: Start the Web UI service

After completing the dependency installation, start the Web UI development server:

```bash
pnpm dev
```

By default, the LangManus Web UI service will run on `http://localhost:3000`.

---

## Browser Tool not starting properly?

LangManus uses [`browser-use`](https://github.com/browser-use/browser-use) to implement browser-related functionality, and `browser-use` is built on [`Playwright`](https://playwright.dev/python). Therefore, you need to install Playwright's browser instance before first use.

```bash
uv run playwright install
```

---

## Can I use my local Chrome browser as the Browser Tool?

Yes. LangManus uses [`browser-use`](https://github.com/browser-use/browser-use) to implement browser-related functionality, and `browser-use` is based on [`Playwright`](https://playwright.dev/python). By configuring the `CHROME_INSTANCE_PATH` in the `.env` file, you can specify the path to your local Chrome browser to use the local browser instance.

### Configuration Steps

1. **Exit all Chrome browser processes**
   Before using the local Chrome browser, ensure all Chrome browser processes are completely closed. Otherwise, `browser-use` cannot start the browser instance properly.

2. **Set `CHROME_INSTANCE_PATH`**
   In the project's `.env` file, add or modify the following configuration item:
   ```plaintext
   CHROME_INSTANCE_PATH=/path/to/your/chrome
   ```
   Replace `/path/to/your/chrome` with the executable file path of your local Chrome browser. For example:
   - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
   - Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`
   - Linux: `/usr/bin/google-chrome`

3. **Start LangManus**
   After starting LangManus, `browser-use` will use your specified local Chrome browser instance.

4. **Access LangManus Web UI**
   Since now your local Chrome browser is being controlled by `browser-use`, you need to use another browser (such as Safari, Mozilla Firefox) to access LangManus's Web interface, which is typically at `http://localhost:3000`. Alternatively, you can access the LangManus Web UI from another device.
