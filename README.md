# 🔄 SpinThatShit

**Autonomous AI Agent Orchestration for Software Development**

A system for managing multiple AI agents (Claude Code CLI) that collaborate on software development. Each agent has a specific role and the system ensures work continuity even when context limits are reached.

> **🌍 Available in 32 languages:** [English](docs/i18n/README.en.md) • [Čeština](docs/i18n/README.cs.md) • [Español](docs/i18n/README.es.md) • [简体中文](docs/i18n/README.zh-CN.md) • [Deutsch](docs/i18n/README.de.md) • [Français](docs/i18n/README.fr.md) • [日本語](docs/i18n/README.ja.md) • [한국어](docs/i18n/README.ko.md) • [Русский](docs/i18n/README.ru.md) • [Português](docs/i18n/README.pt.md) • [हिन्दी](docs/i18n/README.hi.md) • [العربية](docs/i18n/README.ar.md) • [বাংলা](docs/i18n/README.bn.md) • [Italiano](docs/i18n/README.it.md) • [Türkçe](docs/i18n/README.tr.md) • [Tiếng Việt](docs/i18n/README.vi.md) • [Polski](docs/i18n/README.pl.md) • [Українська](docs/i18n/README.uk.md) • [Nederlands](docs/i18n/README.nl.md) • [ไทย](docs/i18n/README.th.md) • [Română](docs/i18n/README.ro.md) • [Ελληνικά](docs/i18n/README.el.md) • [Magyar](docs/i18n/README.hu.md) • [Svenska](docs/i18n/README.sv.md) • [Bahasa Indonesia](docs/i18n/README.id.md) • [فارسی](docs/i18n/README.fa.md) • [עברית](docs/i18n/README.he.md) • [Bahasa Melayu](docs/i18n/README.ms.md) • [Norsk](docs/i18n/README.no.md) • [Slovenčina](docs/i18n/README.sk.md) • [Suomi](docs/i18n/README.fi.md) • [Dansk](docs/i18n/README.da.md)

---

## 🚀 Quick Start

```bash
# Installation
chmod +x install.sh
./install.sh

# Run
spinthatshit
# or shorter
sts
```

---

## 📋 Features

### Multi-Agent Workflow
- **Planner** - Analyzes documentation, creates plan
- **Designer** - Designs UI/UX components
- **Engineer** - Builds infrastructure and architecture
- **Developer** - Implements features
- **Reviewer** - Reviews code quality
- **Tester** - Tests functionality
- **Supervisor** - Detects conflicts and issues
- **Evolver** - Improves the system itself

### Context Management
- Automatic context usage tracking
- Handoff at 50% limit threshold
- Work continuity between agents

### Git Integration
- Automatic commit after every change
- Phase tagging
- Auto-push to GitHub

### Self-Evolution
- System learns from mistakes
- Automatically improves prompts
- Adds new checks

---

## 📁 Project Structure

After running, the following structure is created in the development folder:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orchestration state
│   ├── journal.md          # Journal of all agents
│   ├── plan.md             # Project plan
│   ├── checklist.md        # Task list
│   ├── architecture.md     # Architecture
│   ├── handoff.md          # Handoff notes
│   ├── status.txt          # Current status
│   ├── review.md           # Review results
│   ├── test_report.md      # Test results
│   └── logs/               # Logs of all agents
├── CLAUDE.md               # Instructions for Claude
└── ... (your code)
```

---

## 🎯 Usage

### Interactive Mode
```bash
spinthatshit
```

The system will ask you for:
1. Path to documentation
2. Path to development folder

### With Parameters
```bash
spinthatshit --docs ./docs --dev ./src
```

### Resume
```bash
spinthatshit --resume
```

---

## ⚙️ Configuration

Configuration file: `~/.spinthatshit/config.json`

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

## 🔧 Requirements

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS or Linux**

---

## 📖 How It Works

### 1. Initialization
The system loads documentation and existing code, creates a plan.

### 2. Phase Execution
Each agent runs sequentially:
1. Loads context from journal.md
2. Performs its work
3. Commits changes
4. Updates the checklist
5. Hands off to the next agent

### 3. Context Handoff
When an agent reaches 50% context:
1. Writes state to handoff.md
2. Commits everything
3. Terminates
4. New agent continues

### 4. Recovery
On failure:
1. Supervisor analyzes the problem
2. Orchestrator adjusts rules
3. Agent restarts

### 5. Evolution
After project completion:
1. Evolver analyzes what worked
2. Adjusts agent prompts
3. Adds new checks

---

## 🎬 Example Run

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] PHASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner completed (context: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] PHASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Context at 52% - handing off to next agent
[14:35:48] [INFO] Restarting developer agent (attempt 1/3)
...
```

---

## 🛑 Stopping

- **Ctrl+C** - Safe stop, state is saved
- Use `--resume` to continue

---

## 🐛 Troubleshooting

### Agent is stuck
```bash
# Check the logs
cat your-project/.spinstate/logs/agent_*.log
```

### Code errors
The system has auto-recovery, but you can:
1. Edit `.spinstate/checklist.md`
2. Add a note to `.spinstate/journal.md`
3. Run again

### Context overflow
- Increase `context_limit_percent` in config.json
- Split the project into smaller phases

---

## 📝 Tips

1. **Documentation is key** - Better docs mean better results
2. **Small projects first** - Learn the system on a simple project
3. **Don't micromanage** - Let the agents work
4. **Trust handoffs** - The system remembers context

---

## 🗑️ Uninstallation

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 License

MIT License - Free to use

---

## 🤝 Created for

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"We let AI work while we eat cake."* 🍰
