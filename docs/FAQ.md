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
You can switch the model in use by modifying the `conf.yaml` file in the root directory of the project, using the configuration in the litellm format. For the specific configuration method, please refer to [README.md](https://github.com/langmanus/langmanus/blob/main/README.md).

---

### How to use Ollama models?

LangManus supports the integration of Ollama models. You can refer to [litellm Ollama](https://docs.litellm.ai/docs/providers/ollama). <br>
The following is a configuration example of `conf.yaml` for using Ollama models:

```yaml
REASONING_MODEL:
  model: "ollama/ollama-model-name"
  api_base: "http://localhost:11434" # Local service address of Ollama, which can be started/viewed via ollama serve
```

### How to use OpenRouter models?

LangManus supports the integration of OpenRouter models. You can refer to [litellm OpenRouter](https://docs.litellm.ai/docs/providers/openrouter). To use OpenRouter models, you need to:
1. Obtain the OPENROUTER_API_KEY from OpenRouter (https://openrouter.ai/) and set it in the environment variable.
2. Add the `openrouter/` prefix before the model name.
3. Configure the correct OpenRouter base URL.

The following is a configuration example for using OpenRouter models:
1. Configure OPENROUTER_API_KEY in the environment variable (such as the `.env` file)
```ini
OPENROUTER_API_KEY=""
```
2. Configure the model in `conf.yaml`
```yaml
REASONING_MODEL:
  model: "openrouter/google/palm-2-chat-bison"
```

Note: The available models and their exact names may change over time. Please verify the currently available models and their correct identifiers in [OpenRouter's official documentation](https://openrouter.ai/docs).

### How to use Google Gemini models?

LangManus supports the integration of Google's Gemini models. You can refer to [litellm Gemini](https://docs.litellm.ai/docs/providers/gemini). To use Gemini models, please follow these steps:

1. Obtain the Gemini API key from Google AI Studio (https://makersuite.google.com/app/apikey).
2. Configure the Gemini API key in the environment variable (such as the `.env` file)
```ini
GEMINI_API_KEY="Your Gemini API key"
```
3. Configure the model in `conf.yaml`
```yaml
REASONING_MODEL:
  model: "gemini/gemini-pro"
```

Notes:
- Replace `YOUR_GEMINI_KEY` with your actual Gemini API key.
- The base URL is specifically configured to use Gemini through LangManus' OpenAI-compatible interface.
- The available models include `gemini-2.0-flash` for chat and visual tasks.

### How to use Azure models?

LangManus supports the integration of Azure models. You can refer to [litellm Azure](https://docs.litellm.ai/docs/providers/azure). Configuration example of `conf.yaml`:
```yaml
REASONING_MODEL:
  model: "azure/gpt-4o-2024-08-06"
  api_base: $AZURE_API_BASE
  api_version: $AZURE_API_VERSION
  api_key: $AZURE_API_KEY
``` 

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
