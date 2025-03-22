# FAQ

## 目录

- [LangManus 支持哪些模型？](#langmanus-支持哪些模型)
- [如何部署 Web UI 前端项目？](#如何部署-web-ui-前端项目)
- [可以用本地的 Chrome 浏览器作为 Browser Tool 吗？](#可以用本地的-chrome-浏览器作为-browser-tool-吗)

## LangManus 支持哪些模型？

在 LangManus 中，我们将模型分为以下三类：

### 1. **Chat Model**（聊天模型）
- **用途**：用于对话场景，主要在 **Supervisor** 和 **Agent** 中被调用。
- **支持的模型**：`gpt-4o`、`qwen-max-latest`。

### 2. **Reasoning Model**（推理模型）
- **用途**：用于复杂推理任务，当 **“Deep Think”** 模式启用时，在 **Planner** 中被使用。
- **支持的模型**：`o1`、`o3-mini`、`QwQ-Plus`、`DeepSeek-R1`, `gemini-2.0-flash-thinking-exp`。

### 3. **VL Model**（视觉语言模型）
- **用途**：用于处理视觉和语言结合的任务，主要在 **Browser Tool** 中被调用。
- **支持的模型**：`gpt-4o`、`qwen2.5-vl-72b-instruct`。

### 如何切换模型？

您可以通过修改项目根目录下的 `conf.yaml` 文件使用litellm格式的配置来切换所使用的模型。具体配置方法请参考 [README.md](https://github.com/langmanus/langmanus/blob/main/README.md)。

---

### 如何使用 Ollama 模型？

LangManus 支持集成 Ollama 模型。您可以参考[litellm Ollama](https://docs.litellm.ai/docs/providers/ollama)。<br>
以下是使用 Ollama 模型的conf.yaml配置示例：

```yaml
REASONING_MODEL:
  model: "ollama/ollama-model-name"
  api_base: "http://localhost:11434" # ollama本地服务地址, 可以通过ollama serve启动/查看地址
```

### 如何使用 OpenRouter 模型？

LangManus 支持集成 OpenRouter 模型。你可以参考[litellm OpenRouter](https://docs.litellm.ai/docs/providers/openrouter)，要使用OpenRouter模型，您需要:
1. 从 OpenRouter 获取 OPENROUTER_API_KEY (https://openrouter.ai/) 并设置到环境变量中
2. 在模型名称前添加 `openrouter/` 前缀
3. 配置正确的 OpenRouter 基础 URL

以下是使用 OpenRouter 模型的配置示例：
1. 在环境变量（比如.env文件）中配置OPENROUTER_API_KEY
```ini
OPENROUTER_API_KEY=""
```
2. 在conf.yaml中配置模型
```yaml
REASONING_MODEL:
  model: "openrouter/google/palm-2-chat-bison"
```

注意：可用模型及其确切名称可能随时间变化。请在 [OpenRouter 的官方文档](https://openrouter.ai/docs) 上验证当前可用的模型及其正确标识符。

### 如何使用 Google Gemini 模型？

LangManus 支持集成 Google 的 Gemini 模型。您可以参考[litellm Gemini](https://docs.litellm.ai/docs/providers/gemini)，要使用 Gemini 模型，请按照以下步骤操作：

1. 从 Google AI Studio 获取 Gemini API 密钥 (https://makersuite.google.com/app/apikey)
2. 在环境变量（比如.env文件）中配置Gemini API 密钥
```ini
GEMINI_API_KEY="您的Gemini API密钥"
```
3. 在conf.yaml中配置模型
```yaml
REASONING_MODEL:
  model: "gemini/gemini-pro"
```

注意事项：
- 将 `YOUR_GEMINI_KEY` 替换为你实际的 Gemini API 密钥
- 基础 URL 专门配置为通过 LangManus 的 OpenAI 兼容接口使用 Gemini
- 可用模型包括用于聊天和视觉任务的 `gemini-2.0-flash`

### 如何使用 Azure 模型？

LangManus 支持集成 Azure 的模型。您可以参考[litellm Azure](https://docs.litellm.ai/docs/providers/azure)。conf.yaml配置示例：
```yaml
REASONING_MODEL:
  model: "azure/gpt-4o-2024-08-06"
  api_base: $AZURE_API_BASE
  api_version: $AZURE_API_VERSION
  api_key: $AZURE_API_KEY
```

---

## 如何部署 Web UI 前端项目？

LangManus 提供了一个开箱即用的 Web UI 前端项目，您可以通过以下步骤完成部署。请访问 [LangManus Web UI GitHub 仓库](https://github.com/langmanus/langmanus-web) 获取更多信息。

### 步骤 1：启动 LangManus 的后端服务

首先，确保您已经克隆并安装了 LangManus 的后端项目。进入后端项目目录并启动服务：

```bash
cd langmanus
make serve
```

默认情况下，LangManus 后端服务会运行在 `http://localhost:8000`。

---

### 步骤 2：安装 Web UI 前端项目及其依赖

接下来，克隆 LangManus 的 Web UI 前端项目并安装依赖：

```bash
git clone https://github.com/langmanus/langmanus-web.git
cd langmanus-web
pnpm install
```

> **注意**: 如果您尚未安装 `pnpm`，请先安装它。可以通过以下命令安装：
> ```bash
> npm install -g pnpm
> ```

---

### 步骤 3：启动 Web UI 服务

完成依赖安装后，启动 Web UI 的开发服务器：

```bash
pnpm dev
```

默认情况下，LangManus 的 Web UI 服务会运行在 `http://localhost:3000`。

---

## Browser Tool 无法正常启动？

LangManus 使用 [`browser-use`](https://github.com/browser-use/browser-use) 来实现浏览器相关功能，而 `browser-use` 是基于 [`Playwright`](https://playwright.dev/python) 构建的。因此，在首次使用前，需要安装 `Playwright` 的浏览器实例。

```bash
uv run playwright install
```

---

## 可以用本地的 Chrome 浏览器作为 Browser Tool 吗？

是的，LangManus 支持使用本地的 Chrome 浏览器作为 Browser Tool。LangManus 使用 [`browser-use`](https://github.com/browser-use/browser-use) 来实现浏览器相关功能，而 `browser-use` 是基于 [`Playwright`](https://playwright.dev/python) 实现的。通过配置 `.env` 文件中的 `CHROME_INSTANCE_PATH`，你可以指定本地 Chrome 浏览器的路径，从而实现使用本地浏览器实例的功能。

### 配置步骤

1. **退出所有 Chrome 浏览器进程**
   在使用本地 Chrome 浏览器之前，确保所有 Chrome 浏览器进程已完全退出。否则，`browser-use` 无法正常启动浏览器实例。

2. **设置 `CHROME_INSTANCE_PATH`**
   在项目的 `.env` 文件中，添加或修改以下配置项：
   ```plaintext
   CHROME_INSTANCE_PATH=/path/to/your/chrome
   ```
   将 `/path/to/your/chrome` 替换为本地 Chrome 浏览器的可执行文件路径。例如：
   - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
   - Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`
   - Linux: `/usr/bin/google-chrome`

3. **启动 LangManus**
   启动 LangManus 后，`browser-use` 将使用你指定的本地 Chrome 浏览器实例。

4. **访问 LangManus 的 Web UI**
   由于本地 Chrome 浏览器被 `browser-use` 占用，你需要使用其他浏览器（如 Safari、Mozilla Firefox）访问 LangManus 的 Web 界面，地址通常为 `http://localhost:3000`。或者，你也可以从另一台计算机上访问 LangManus 的 Web UI。
