<div align="center">

# mini-OpenCode

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Google](https://img.shields.io/badge/code%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html)

[English](./README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

**mini-OpenCode** は、[Deer-Code](https://github.com/MagicCube/deer-code) と [OpenCode](https://github.com/anomalyco/opencode) に触発された、軽量で実験的な AI コーディングエージェントです。大規模言語モデル（LLM）が、最小限のインフラでどのように計画、推論、そして反復的にコードを記述できるかを示しています。[LangGraph](https://github.com/langchain-ai/langgraph) をベースに構築されており、エージェント型コーディングシステムの理解と構築のためのハッカブルな基盤として機能します。

<br/>
<img src="docs/images/tui_light_theme.png" width="45%" alt="ライトテーマ"/>
<img src="docs/images/tui_dark_theme.png" width="45%" alt="ダークテーマ"/>
<br/>

</div>

---

## ✨ 特徴

- **🤖 DeepAgents 駆動**: LangChain エコシステムの `create_deep_agent` をベースに構築され、エージェント型コーディングの強固な基盤を提供。
- **📝 統合タスク管理**: 複雑な多段階タスクを効率的に管理・追跡する `write_todos` ツールを内蔵。
- **🛠️ 必須ツールセット**:
    - **ファイル操作**: `ls`、`read_file`、`write_file`、`edit_file`、`glob`、`grep` ツールを内蔵。
    - **シェル実行**: シェルコマンドを安全に実行する `execute` ツールを内蔵。
    - **ウェブ機能**: **MCP (Model Context Protocol)** 拡張をサポートする、設定可能なウェブ検索およびクローリングツール。
- **🧩 サブエージェントメカニズム**: 補助的なタスクを処理するデフォルトの `general-purpose` サブエージェントを搭載。
- **🚀 スキルシステム**: ユーザー定義のスキルを自動的に認識して利用し、エージェントの機能を拡張。
- **🧠 インテリジェントなコンテキスト管理**:
    - **AGENTS.md インジェクション**: `AGENTS.md` の内容を自動的に検出し、コンテキストに注入。
    - **SummarizationMiddleware**: コンテキスト制限に達した際に会話履歴を自動的に要約。
    - **大規模出力の処理**: コンテキストウィンドウの飽和を防ぐため、大規模なツール出力を自動的にファイルシステムに退避。
    - **堅牢性**: 宙に浮いたツール呼び出しを適切に処理する `PatchToolCallsMiddleware` を搭載。
- **🎨 美しい TUI**: Textual ベースの洗練されたターミナルユーザーインターフェース。ダーク/ライトモードの切り替えやストリーミング出力に対応。
- **⚡️ スラッシュコマンド**: `/clear` や `/exit` などのスラッシュコマンドをサポートし、素早い操作が可能。
- **⚙️ 高度なカスタマイズ性**: YAML 設定により、モデル、ツール、動作を完全にカスタマイズ可能。

## 📖 目次

- [特徴](#-特徴)
- [事前準備](#-事前準備)
- [インストール](#-インストール)
- [設定](#-設定)
- [使い方](#-使い方)
- [プロジェクト構造](#-プロジェクト構造)
- [貢献](#-貢献)
- [謝辞](#-謝辞)
- [スター履歴](#-star-history)
- [ライセンス](#-ライセンス)

## 🚀 事前準備

- **Python 3.12** 以上
- **[uv](https://github.com/astral-sh/uv)** パッケージマネージャー（依存関係管理に強く推奨）
- LLM 用の API キー（DeepSeek, Doubao など）およびオプションのウェブツール（Tavily, Firecrawl）のキー

## 📦 インストール

1.  **リポジトリをクローンする**
    ```bash
    git clone https://github.com/your-username/mini-opencode.git
    cd mini-opencode
    ```

2.  **依存関係をインストールする**
    ```bash
    uv sync
    # または make を使用
    make install
    ```

## ⚙️ 設定

1.  **環境変数**
    環境変数の例ファイルをコピーし、API キーを入力します：
    ```bash
    cp .example.env .env
    ```
    `.env` を編集：
    ```ini
    DEEPSEEK_API_KEY=your_key_here
    # オプション:
    KIMI_API_KEY=your_kimi_key
    TAVILY_API_KEY=your_tavily_key
    FIRECRAWL_API_KEY=your_firecrawl_key
    ```

2.  **アプリケーション設定**
    設定ファイルの例をコピーします：
    ```bash
    cp config.example.yaml config.yaml
    ```
    `config.yaml` を編集して、有効にするツール、モデルパラメータ、MCP サーバーをカスタマイズします。

3.  **LangGraph 設定（オプション）**
    LangGraph Studio を使用してエージェントをデバッグする場合は、LangGraph 設定ファイルの例をコピーします：
    ```bash
    cp langgraph.example.json langgraph.json
    ```

## 💻 使い方

### CLI モード
プロジェクトディレクトリでエージェントを直接実行します：
```bash
uv run -m mini_opencode /absolute/path/to/target/project
# または python を使用
python -m mini_opencode /absolute/path/to/target/project
```

### 開発モード (LangGraph Studio)
LangGraph 開発サーバーを起動して、エージェントを可視化し、対話します：
```bash
make dev
```
その後、ブラウザで [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024) を開きます。

## 🏗️ プロジェクト構造

```text
mini-opencode/
├── src/mini_opencode/
│   ├── agents/           # エージェント作成ロジック (deepagents ベース)
│   ├── cli/              # ターミナル UI (Textual) コンポーネント
│   ├── config/           # 設定のロードとバリデーション
│   ├── models/           # LLM モデルファクトリとセットアップ
│   ├── prompts/          # プロンプトテンプレート (Jinja2)
│   ├── tools/            # 追加ツールの実装
│   │   ├── date/         # 日付ツール
│   │   ├── mcp/          # MCP ツールの統合
│   │   └── web/          # ウェブ検索とクローリング
│   ├── main.py           # CLI エントリポイント
│   └── project.py        # プロジェクトコンテキストマネージャー
├── skills/               # エージェントスキル（指示、スクリプト、リファレンス）
├── config.example.yaml   # 設定テンプレート
├── langgraph.example.json# LangGraph 設定テンプレート
├── Makefile              # ビルドと実行コマンド
└── pyproject.toml        # プロジェクトの依存関係とメタデータ
```

## 🤝 貢献

貢献を歓迎します！プルリクエストを自由に送信してください。

1.  プロジェクトをフォークする
2.  機能ブランチを作成する (`git checkout -b feature/AmazingFeature`)
3.  変更をコミットする ([Semantic Commits](https://www.conventionalcommits.org/) に従ってください。例: `git commit -m 'feat: Add some AmazingFeature'`)
4.  ブランチをプッシュする (`git push origin feature/AmazingFeature`)
5.  プルリクエストを作成する

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) の開発ガイドラインを参照してください。

## 🙏 謝辞

インスピレーションとアーキテクチャのリファレンスを提供してくれた以下のプロジェクトの開発者に感謝します。

- **[Deer-Code](https://github.com/MagicCube/deer-code)**
- **[OpenCode](https://github.com/anomalyco/opencode)**

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=amszuidas/mini-opencode&type=Date)](https://star-history.com/#amszuidas/mini-opencode&Date)

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

---
*Built with ❤️ using [LangGraph](https://langchain-ai.github.io/langgraph/) and [Textual](https://textual.textualize.io/).*
