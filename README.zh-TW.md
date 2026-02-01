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

- **🤖 智能編程智能體**：利用 LangGraph 實現有狀態的多步推理與執行。
- **📝 上下文感知任務管理**：內置 TODO 系統，用於跟蹤複雜多步任務的進度。
- **🛠️ 完善的工具集**：包含檔案操作（`read`, `write`, `edit`）、檔案系統導航（`ls`, `tree`, `grep`）、終端命令（`bash`）、網路搜尋（`tavily`）以及網頁爬取（`firecrawl`）。
- **🔌 可擴展架構**：支持 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)，可輕鬆集成外部工具和伺服器。
- **🚀 智能體技能系統**：動態載入特定的指令、腳本和資源（Skills），以提升在特定任務（如前端設計）上的表現。
- **🧠 智能上下文管理**：內置總結（Summarization）中間件，在對話歷史過長時自動壓縮上下文，確保模型在長會話中的指令遵循能力。
- **🎨 交互式 UI**：使用 [Textual](https://github.com/Textualize/textual) 建構的整潔終端界面，支持深淺色模式自動切換及模型響應串流輸出。
- **⚡️ 斜杠命令**：通過 `/clear`（重置聊天）、`/resume`（恢復會話）和 `/exit`（退出）等命令快速訪問功能，支持自動補全建議。
- **⚙️ 高度可配置**：靈活的 YAML 配置文件，支持自定義模型參數、工具及 API 金鑰。
- **🔒 類型安全**：全量類型提示（Python 3.12+），確保程式碼可靠性及開發體驗。

## 📖 目錄

- [特性](#-特性)
- [環境準備](#-環境準備)
- [安裝指南](#-安裝指南)
- [配置說明](#-配置說明)
- [使用方法](#-使用方法)
- [專案結構](#-專案結構)
- [開發指南](#-開發指南)
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
    ARK_API_KEY=your_doubao_key
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
│   ├── agents/           # 核心智能體邏輯與狀態定義
│   ├── cli/              # 終端 UI (Textual) 組件
│   ├── config/           # 配置載入與校驗
│   ├── middlewares/      # 智能體中間件（如總結中間件）
│   ├── models/           # LLM 模型工廠與設置
│   ├── prompts/          # 提示詞模板 (Jinja2)
│   ├── skills/           # 技能系統實現（載入器、解析器、類型）
│   ├── tools/            # 工具實現
│   │   ├── file/         # 檔案 I/O (read, write, edit)
│   │   ├── fs/           # 檔案系統 (ls, tree, grep)
│   │   ├── terminal/     # Bash 執行
│   │   ├── web/          # 搜尋與爬取
│   │   ├── mcp/          # MCP 工具集成
│   │   └── todo/         # 任務管理
│   ├── main.py           # CLI 入口
│   └── project.py        # 專案上下文管理器
├── skills/               # 智能體技能（指令、腳本及參考資料）
├── AGENTS.md             # 智能體開發指南
├── Makefile              # 建構與運行命令
├── config.example.yaml   # 示例配置模板
├── langgraph.example.json# 示例 LangGraph 配置模板
└── pyproject.toml        # 專案依賴與元數據
```

## 🔧 開發指南

### 添加新工具
1.  在 `src/mini_opencode/tools/` 中建立一個新檔案。
2.  使用 `@tool` 裝飾器並設置 `parse_docstring=True`。
3.  添加 Google 風格的 docstrings 以進行參數解析。
4.  在 `src/mini_opencode/agents/coding_agent.py` 中註冊該工具。

### 程式碼風格
- **類型提示**：所有函數必須包含類型提示。
- **Docstrings**：要求使用 Google 風格。
- **命名規範**：函數/變數使用 `snake_case`，類名使用 `PascalCase`。

詳見 [AGENTS.md](AGENTS.md) 獲取詳細的開發準則。

## 🤝 參與貢獻

歡迎貢獻！請隨時提交 Pull Request。

1.  Fork 本專案
2.  建立特性分支 (`git checkout -b feature/AmazingFeature`)
3.  提交更改（遵循 [Semantic Commits](https://www.conventionalcommits.org/) 規範，例如 `git commit -m 'feat: Add some AmazingFeature'`)
4.  推送到分支 (`git push origin feature/AmazingFeature`)
5.  開啟一個 Pull Request

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
