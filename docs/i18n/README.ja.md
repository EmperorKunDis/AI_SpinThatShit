---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**ソフトウェア開発のための自律型AIエージェントオーケストレーション**

ソフトウェア開発で協力する複数のAIエージェント(Claude Code CLI)を管理するシステム。各エージェントは特定の役割を持ち、コンテキスト制限に達した場合でも作業の継続性を保証します。

---

## 🚀 クイックスタート

```bash
# インストール
chmod +x install.sh
./install.sh

# 実行
spinthatshit
# または短縮形
sts
```

---

## 📋 機能

### マルチエージェントワークフロー
- **Planner** - ドキュメントを分析し、計画を作成
- **Designer** - UI/UXコンポーネントを設計
- **Engineer** - インフラストラクチャとアーキテクチャを構築
- **Developer** - 機能を実装
- **Reviewer** - コード品質をレビュー
- **Tester** - 機能をテスト
- **Supervisor** - 競合と問題を特定
- **Evolver** - システム自体を改善

### コンテキスト管理
- コンテキスト使用状況の自動追跡
- 50%制限で引き継ぎ
- エージェント間での作業継続性

### Git統合
- 変更後の自動コミット
- フェーズのタグ付け
- GitHubへの自動プッシュ

### 自己進化
- システムがエラーから学習
- プロンプトを自動的に改善
- 新しいチェックを追加

---

## 📁 プロジェクト構造

実行後、開発フォルダに以下の構造が作成されます:

```
your-project/
├── .spinstate/
│   ├── state.json          # オーケストレーション状態
│   ├── journal.md          # 全エージェントのジャーナル
│   ├── plan.md             # プロジェクト計画
│   ├── checklist.md        # タスクリスト
│   ├── architecture.md     # アーキテクチャ
│   ├── handoff.md          # 引き継ぎノート
│   ├── status.txt          # 現在のステータス
│   ├── review.md           # レビュー結果
│   ├── test_report.md      # テスト結果
│   └── logs/               # 全エージェントのログ
├── CLAUDE.md               # Claudeへの指示
└── ... (あなたのコード)
```

---

## 🎯 使用方法

### 対話モード
```bash
spinthatshit
```

システムは以下を尋ねます:
1. ドキュメントのパス
2. 開発フォルダのパス

### パラメータ付き
```bash
spinthatshit --docs ./docs --dev ./src
```

### 再開
```bash
spinthatshit --resume
```

---

## ⚙️ 設定

設定ファイル: `~/.spinthatshit/config.json`

```json
{
    "context_limit_percent": 50,
    "max_retries": 3,
    "agent_timeout_minutes": 30,
    "auto_push": true,
    "agents": {
        "workflow_order": ["planner", "designer", "engineer", ...],
        "enabled": {
            "designer": true,
            "tester": true
        }
    }
}
```

---

## 🔧 要件

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOSまたはLinux**

---

## 📖 動作方法

### 1. 初期化
システムはドキュメントと既存のコードを読み込み、計画を作成します。

### 2. フェーズ実行
各エージェントは順次実行されます:
1. journal.mdからコンテキストを読み込む
2. 作業を実行
3. 変更をコミット
4. チェックリストに書き込む
5. 次のエージェントに引き継ぐ

### 3. コンテキスト引き継ぎ
エージェントがコンテキストの50%に達したとき:
1. handoff.mdに状態を書き込む
2. すべてをコミット
3. 終了
4. 新しいエージェントが続行

### 4. リカバリ
失敗時:
1. Supervisorが問題を分析
2. Orchestratorがルールを調整
3. エージェントが再起動

### 5. 進化
プロジェクト完了後:
1. Evolverが何が機能したかを分析
2. エージェントのプロンプトを調整
3. 新しいチェックを追加

---

## 🎬 実行例

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] フェーズ: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner 完了 (コンテキスト: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] フェーズ: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] コンテキスト52% - 次のエージェントに引き継ぎ
[14:35:48] [INFO] エージェントdeveloperを再起動 (試行 1/3)
...
```

---

## 🛑 停止

- **Ctrl+C** - 安全な停止、状態は保存されます
- 続行するには `--resume` を使用

---

## 🐛 トラブルシューティング

### エージェントが停止している
```bash
# ログを確認
cat your-project/.spinstate/logs/agent_*.log
```

### コードエラー
システムには自動リカバリがありますが、以下も可能です:
1. `.spinstate/checklist.md` を編集
2. `.spinstate/journal.md` にメモを追加
3. 再実行

### コンテキストオーバーフロー
- config.jsonで `context_limit_percent` を増やす
- プロジェクトをより小さなフェーズに分割

---

## 📝 ヒント

1. **ドキュメントが鍵** - より良いドキュメント、より良い結果
2. **小さなプロジェクトから始める** - シンプルなプロジェクトでシステムを学ぶ
3. **各ステップを確認しない** - エージェントに作業させる
4. **引き継ぎを信頼する** - システムはコンテキストを記憶します

---

## 🗑️ アンインストール

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 ライセンス

MITライセンス - 自由に使用可能

---

## 🤝 作成者

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*「AIに働かせて、私たちはケーキを食べる。」* 🍰
