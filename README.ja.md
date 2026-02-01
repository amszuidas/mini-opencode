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

- **🤖 インテリジェント・コーディングエージェント**: LangGraph を活用し、状態を持つ多段階の推論と実行を実現。
- **📝 コンテキストを考慮したタスク管理**: 複雑な多段階タスクの進捗を追跡するための TODO システムを内蔵。
- **🛠️ 包括的なツールセット**: ファイル操作（`read`, `write`, `edit`）、ファイルシステムナビゲーション（`ls`, `tree`, `grep`）、ターミナルコマンド（`bash`）、ウェブ検索（`tavily`）、およびウェブクローリング（`firecrawl`）ツールを搭載。
- **🔌 拡張可能なアーキテクチャ**: [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) をサポートし、外部ツールやサーバーとの統合が可能。
- **🚀 エージェント・スキルシステム**: 特定のタスク（例：フロントエンドデザイン）のパフォーマンスを向上させるため、専門的な指示、スクリプト、およびリソース（スキル）を動的にロード。
- **🧠 インテリジェントなコンテキスト管理**: 会話履歴が長くなった場合にコンテキストを自動的に圧縮する要約（Summarization）ミドルウェアを内蔵し、長時間のセッションでもモデルのパフォーマンスを維持。
- **🎨 インタラクティブな UI**: [Textual](https://github.com/Textualize/textual) を使用したクリーンなターミナルベースのインターフェース。ダーク/ライトモードの自動切り替えやモデル応答のストリーミング表示に対応。
- **⚡️ スラッシュコマンド**: `/clear`（チャットのリセット）、`/resume`（セッションの復元）、`/exit`（終了）などのコマンドにより機能へ素早くアクセス。自動補完機能付き。
- **⚙️ 高度なカスタマイズ性**: モデル、ツール、API キーを柔軟に設定できる YAML ベースの構成。
- **🔒 型の安全性**: 完全に型定義されたコードベース（Python 3.12+）により、信頼性と開発体験を向上。

## 📖 目次

- [特徴](#-特徴)
- [事前準備](#-事前準備)
- [インストール](#-インストール)
- [設定](#-設定)
- [使い方](#-使い方)
- [プロジェクト構造](#-プロジェクト構造)
- [開発](#-開発)
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
    ARK_API_KEY=your_doubao_key
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
│   ├── agents/           # コアエージェントロジックと状態定義
│   ├── cli/              # ターミナル UI (Textual) コンポーネント
│   ├── config/           # 設定のロードとバリデーション
│   ├── middlewares/      # エージェントミドルウェア（例：要約）
│   ├── models/           # LLM モデルファクトリとセットアップ
│   ├── prompts/          # プロンプトテンプレート (Jinja2)
│   ├── skills/           # スキルシステムの実装（ローダー、パーサー、型）
│   ├── tools/            # ツールの実装
│   │   ├── file/         # ファイル I/O (read, write, edit)
│   │   ├── fs/           # ファイルシステム (ls, tree, grep)
│   │   ├── terminal/     # Bash 実行
│   │   ├── web/          # 検索とクローリング
│   │   ├── mcp/          # MCP ツールの統合
│   │   └── todo/         # タスク管理
│   ├── main.py           # CLI エントリポイント
│   └── project.py        # プロジェクトコンテキストマネージャー
├── skills/               # エージェントスキル（指示、スクリプト、リファレンス）
├── AGENTS.md             # エージェント向け開発ガイド
├── Makefile              # ビルドと実行コマンド
├── config.example.yaml   # 設定テンプレート
├── langgraph.example.json# LangGraph 設定テンプレート
└── pyproject.toml        # プロジェクトの依存関係とメタデータ
```

## 🔧 開発

### 新しいツールの追加
1.  `src/mini_opencode/tools/` に新しいファイルを作成します。
2.  `@tool` デコレータを使用し、`parse_docstring=True` を設定します。
3.  引数解析のために Google スタイルの docstring を追加します。
4.  `src/mini_opencode/agents/coding_agent.py` でツールを登録します。

### コードスタイル
- **型ヒント**: すべての関数で必須。
- **Docstrings**: Google スタイルが必須。
- **命名規則**: 関数/変数は `snake_case`、クラスは `PascalCase`。

詳細は [AGENTS.md](AGENTS.md) の開発ガイドラインを参照してください。

## 🤝 貢献

貢献を歓迎します！プルリクエストを自由に送信してください。

1.  プロジェクトをフォークする
2.  機能ブランチを作成する (`git checkout -b feature/AmazingFeature`)
3.  変更をコミットする ([Semantic Commits](https://www.conventionalcommits.org/) に従ってください。例: `git commit -m 'feat: Add some AmazingFeature'`)
4.  ブランチをプッシュする (`git push origin feature/AmazingFeature`)
5.  プルリクエストを作成する

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
