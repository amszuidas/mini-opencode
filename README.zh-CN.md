<div align="center">

# mini-OpenCode

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Google](https://img.shields.io/badge/code%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html)

[English](./README.md) | [繁體中文](./README.zh-TW.md) | [日本語](./README.ja.md)

**mini-OpenCode** 是一个轻量级、实验性的 AI 编程智能体，灵感源自 [Deer-Code](https://github.com/MagicCube/deer-code) 和 [OpenCode](https://github.com/anomalyco/opencode)。它展示了大语言模型（LLM）如何在极简的基础设施下进行规划、推理并迭代编写代码。本项目基于 [LangGraph](https://github.com/langchain-ai/langgraph) 构建，旨在为理解和构建智能体编程系统提供一个可扩展的基础。

<br/>
<img src="docs/images/tui_light_theme.png" width="45%" alt="浅色主题"/>
<img src="docs/images/tui_dark_theme.png" width="45%" alt="深色主题"/>
<br/>

</div>

---

## ✨ 特性

- **🤖 DeepAgents 驱动**：基于 LangChain 生态的 `create_deep_agent` 构建，为智能体编程提供稳健基础。
- **📝 集成任务管理**：内置 `write_todos` 工具，高效管理和追踪复杂的多步任务。
- **🛠️ 核心工具集**：
    - **文件操作**：内置 `ls`、`read_file`、`write_file`、`edit_file`、`glob` 和 `grep` 工具。
    - **Shell 执行**：内置 `execute` 工具，安全执行 Shell 命令。
    - **网络能力**：可配置的网络搜索和爬取工具，支持 **MCP (Model Context Protocol)** 扩展。
- **🧩 子智能体机制**：包含默认的 `general-purpose` 子智能体，用于处理辅助任务。
- **🚀 技能系统**：自动识别并利用用户定义的 Skills，增强智能体能力。
- **🧠 智能上下文管理**：
    - **AGENTS.md 注入**：自动检测并将 `AGENTS.md` 内容注入上下文。
    - **SummarizationMiddleware**：当上下文达到限制时自动总结对话历史。
    - **大输出处理**：自动将大型工具输出转存至文件系统，防止上下文窗口饱和。
    - **鲁棒性**：包含 `PatchToolCallsMiddleware`，优雅处理悬空的工具调用。
- **🎨 精美 TUI**：基于 Textual 的精致终端用户界面，支持深浅色模式切换和流式输出。
- **⚡️ 斜杠命令**：支持斜杠命令（如 `/clear`、`/exit`）以快速执行操作。
- **⚙️ 高度可配置**：通过 YAML 配置完全自定义模型、工具和行为。

## 📖 目录

- [特性](#-特性)
- [环境准备](#-环境准备)
- [安装指南](#-安装指南)
- [配置说明](#-配置说明)
- [使用方法](#-使用方法)
- [项目结构](#-项目结构)
- [参与贡献](#-参与贡献)
- [致谢](#-致谢)
- [Star History](#-star-history)
- [开源协议](#-开源协议)

## 🚀 环境准备

- **Python 3.12** 或更高版本
- **[uv](https://github.com/astral-sh/uv)** 包管理器（强烈推荐用于依赖管理）
- LLM API 密钥（如 DeepSeek, Doubao）及可选的网络工具密钥（Tavily, Firecrawl）

## 📦 安装指南

1.  **克隆仓库**
    ```bash
    git clone https://github.com/your-username/mini-opencode.git
    cd mini-opencode
    ```

2.  **安装依赖**
    ```bash
    uv sync
    # 或者使用 make
    make install
    ```

## ⚙️ 配置说明

1.  **环境变量**
    复制示例环境文件并填入你的 API 密钥：
    ```bash
    cp .example.env .env
    ```
    编辑 `.env`：
    ```ini
    DEEPSEEK_API_KEY=your_key_here
    # 可选：
    KIMI_API_KEY=your_kimi_key
    TAVILY_API_KEY=your_tavily_key
    FIRECRAWL_API_KEY=your_firecrawl_key
    ```

2.  **应用配置**
    复制示例配置文件：
    ```bash
    cp config.example.yaml config.yaml
    ```
    编辑 `config.yaml` 以自定义启用的工具、模型参数和 MCP 服务器。

3.  **LangGraph 配置（可选）**
    如果你打算使用 LangGraph Studio 调试智能体，请复制示例 LangGraph 配置文件：
    ```bash
    cp langgraph.example.json langgraph.json
    ```

## 💻 使用方法

### CLI 模式
在目标项目目录上直接运行智能体：
```bash
uv run -m mini_opencode /absolute/path/to/target/project
# 或者使用 python
python -m mini_opencode /absolute/path/to/target/project
```

### 开发模式 (LangGraph Studio)
启动 LangGraph 开发服务器以可视化并与智能体交互：
```bash
make dev
```
然后在浏览器中打开 [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)。

## 🏗️ 项目结构

```text
mini-opencode/
├── src/mini_opencode/
│   ├── agents/           # 智能体创建逻辑 (基于 deepagents)
│   ├── cli/              # 终端 UI (Textual) 组件
│   ├── config/           # 配置加载与校验
│   ├── models/           # LLM 模型工厂与设置
│   ├── prompts/          # 提示词模板 (Jinja2)
│   ├── tools/            # 额外工具实现
│   │   ├── date/         # 日期工具
│   │   ├── mcp/          # MCP 工具集成
│   │   └── web/          # 网络搜索与爬取
│   ├── main.py           # CLI 入口
│   └── project.py        # 项目上下文管理器
├── skills/               # 智能体技能（指令、脚本及参考资料）
├── config.example.yaml   # 示例配置模板
├── langgraph.example.json# 示例 LangGraph 配置模板
├── Makefile              # 构建与运行命令
└── pyproject.toml        # 项目依赖与元数据
```

## 🤝 参与贡献

欢迎贡献！请随时提交 Pull Request。

1.  Fork 本项目
2.  创建特性分支 (`git checkout -b feature/AmazingFeature`)
3.  提交更改（遵循 [Semantic Commits](https://www.conventionalcommits.org/) 规范，例如 `git commit -m 'feat: Add some AmazingFeature'`)
4.  推送到分支 (`git push origin feature/AmazingFeature`)
5.  开启一个 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md) 获取详细的开发准则。

## 🙏 致谢

特别感谢以下项目的开发者，为本项目提供了灵感和架构参考：

- **[Deer-Code](https://github.com/MagicCube/deer-code)**
- **[OpenCode](https://github.com/anomalyco/opencode)**

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=amszuidas/mini-opencode&type=Date)](https://star-history.com/#amszuidas/mini-opencode&Date)

## 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---
*Built with ❤️ using [LangGraph](https://langchain-ai.github.io/langgraph/) and [Textual](https://textual.textualize.io/).*
