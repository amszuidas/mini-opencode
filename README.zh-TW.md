<div align="center">

# mini-OpenCode

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Google](https://img.shields.io/badge/code%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html)

[English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md)

**mini-OpenCode** 是一個輕量級、實驗性的 AI 編程智能體，靈感源自 [Deer-Code](https://github.com/MagicCube/deer-code) 和 [OpenCode](https://github.com/anomalyco/opencode)。它展示了大語言模型（LLM）如何在極簡的基礎設施下進行規劃、推理並迭代編寫程式碼。本專案基於 [LangGraph](https://github.com/langchain-ai/langgraph) 建構，旨在為理解和建構智能體編程系統提供一個可擴展的基礎。

<br/>
<img src="docs/images/tui_light_theme.png" width="45%" alt="淺色主題"/>
<img src="docs/images/tui_dark_theme.png" width="45%" alt="深色主題"/>
<br/>

</div>

---

## ✨ 特性

- **🤖 DeepAgents 驅動**：基於 LangChain 生態的 `create_deep_agent` 建構，為智能體編程提供穩健基礎。
- **📝 集成任務管理**：內置 `write_todos` 工具，高效管理和追蹤複雜的多步任務。
- **🛠️ 核心工具集**：
    - **檔案操作**：內置 `ls`、`read_file`、`write_file`、`edit_file`、`glob` 和 `grep` 工具。
    - **Shell 執行**：內置 `execute` 工具，安全執行 Shell 命令。
    - **網路能力**：可配置的網路搜尋和爬取工具，支持 **MCP (Model Context Protocol)** 擴展。
- **🧩 子智能體機制**：包含默認的 `general-purpose` 子智能體，用於處理輔助任務。
- **🚀 技能系統**：自動識別並利用用戶定義的 Skills，增強智能體能力。
- **🧠 智能上下文管理**：
    - **AGENTS.md 注入**：自動檢測並將 `AGENTS.md` 內容注入上下文。
    - **SummarizationMiddleware**：當上下文達到限制時自動總結對話歷史。
    - **大輸出處理**：自動將大型工具輸出轉存至檔案系統，防止上下文窗口飽和。
    - **魯棒性**：包含 `PatchToolCallsMiddleware`，優雅處理懸空的工具調用。
- **🎨 精美 TUI**：基於 Textual 的精緻終端用戶界面，支持深淺色模式切換和串流輸出。
- **⚡️ 斜杠命令**：支持斜杠命令（如 `/clear`、`/exit`）以快速執行操作。
- **⚙️ 高度可配置**：通過 YAML 配置完全自定義模型、工具和行為。

## 📖 目錄

- [特性](#-特性)
- [環境準備](#-環境準備)
- [安裝指南](#-安裝指南)
- [配置說明](#-配置說明)
- [使用方法](#-使用方法)
- [專案結構](#-專案結構)
- [參與貢獻](#-參與貢獻)
- [致謝](#-致謝)
- [Star History](#-star-history)
- [開源協議](#-開源協議)

## 🚀 環境準備

- **Python 3.12** 或更高版本
- **[uv](https://github.com/astral-sh/uv)** 包管理器（強烈推薦用於依賴管理）
- LLM API 金鑰（如 DeepSeek, Doubao）及可選的網路工具金鑰（Tavily, Firecrawl）

## 📦 安裝指南

1.  **複製倉庫**
    ```bash
    git clone https://github.com/your-username/mini-opencode.git
    cd mini-opencode
    ```

2.  **安裝依賴**
    ```bash
    uv sync
    # 或者使用 make
    make install
    ```

## ⚙️ 配置說明

1.  **環境變數**
    複製示例環境檔案並填入你的 API 金鑰：
    ```bash
    cp .example.env .env
    ```
    編輯 `.env`：
    ```ini
    DEEPSEEK_API_KEY=your_key_here
    # 可選：
    KIMI_API_KEY=your_kimi_key
    TAVILY_API_KEY=your_tavily_key
    FIRECRAWL_API_KEY=your_firecrawl_key
    ```

2.  **應用配置**
    複製示例配置文件：
    ```bash
    cp config.example.yaml config.yaml
    ```
    編輯 `config.yaml` 以自定義啟用的工具、模型參數和 MCP 伺服器。

3.  **LangGraph 配置（可選）**
    如果你打算使用 LangGraph Studio 調試智能體，請複製示例 LangGraph 配置文件：
    ```bash
    cp langgraph.example.json langgraph.json
    ```

## 💻 使用方法

### CLI 模式
在目標專案目錄上直接運行智能體：
```bash
uv run -m mini_opencode /absolute/path/to/target/project
# 或者使用 python
python -m mini_opencode /absolute/path/to/target/project
```

### 開發模式 (LangGraph Studio)
啟動 LangGraph 開發伺服器以視覺化並與智能體交互：
```bash
make dev
```
然後在瀏覽器中打開 [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)。

## 🏗️ 專案結構

```text
mini-opencode/
├── src/mini_opencode/
│   ├── agents/           # 智能體創建邏輯 (基於 deepagents)
│   ├── cli/              # 終端 UI (Textual) 組件
│   ├── config/           # 配置載入與校驗
│   ├── models/           # LLM 模型工廠與設置
│   ├── prompts/          # 提示詞模板 (Jinja2)
│   ├── tools/            # 額外工具實現
│   │   ├── date/         # 日期工具
│   │   ├── mcp/          # MCP 工具集成
│   │   └── web/          # 網路搜尋與爬取
│   ├── main.py           # CLI 入口
│   └── project.py        # 專案上下文管理器
├── skills/               # 智能體技能（指令、腳本及參考資料）
├── config.example.yaml   # 示例配置模板
├── langgraph.example.json# 示例 LangGraph 配置模板
├── Makefile              # 建構與運行命令
└── pyproject.toml        # 專案依賴與元數據
```

## 🤝 參與貢獻

歡迎貢獻！請隨時提交 Pull Request。

1.  Fork 本專案
2.  建立特性分支 (`git checkout -b feature/AmazingFeature`)
3.  提交更改（遵循 [Semantic Commits](https://www.conventionalcommits.org/) 規範，例如 `git commit -m 'feat: Add some AmazingFeature'`)
4.  推送到分支 (`git push origin feature/AmazingFeature`)
5.  開啟一個 Pull Request

詳見 [CONTRIBUTING.md](CONTRIBUTING.md) 獲取詳細的開發準則。

## 🙏 致謝

特別感謝以下專案的開發者，為本專案提供了靈感和架構參考：

- **[Deer-Code](https://github.com/MagicCube/deer-code)**
- **[OpenCode](https://github.com/anomalyco/opencode)**

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=amszuidas/mini-opencode&type=Date)](https://star-history.com/#amszuidas/mini-opencode&Date)

## 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。

---
*Built with ❤️ using [LangGraph](https://langchain-ai.github.io/langgraph/) and [Textual](https://textual.textualize.io/).*
