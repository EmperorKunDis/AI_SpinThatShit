# SpinThatShit - Claude Code Instructions

## 🎯 Project Identity
SpinThatShit is a self-evolving AI orchestration system for autonomous web development.

## 📁 Critical Files
- `spin.py` - Main orchestrator
- `.spincore/prompts/*.md` - Agent prompt templates
- `.spincore/evolution/rules.json` - Evolution rules
- `.agentic/standards/*.md` - Quality standards
- `config.json` - Global configuration

## ⚠️ Critical Rules

### DO NOT:
1. Break backwards compatibility with existing `.spinstate/` files
2. Remove any agent from the workflow
3. Change Git commit message format

### ALWAYS:
1. Run `python -m py_compile spin.py` before committing
2. Document changes in `.spincore/evolution/history.md`
3. Test with `--dry-run` flag first

## 🧠 Smart Agent Dispatch
The key optimization is `should_skip_agent()` - agents skip when no pending tasks exist.

## 📝 Prompt Template System
Prompts loaded from `.spincore/prompts/{agent}.md` with variables:
- `{{PROJECT_CONTEXT}}`
- `{{CONCRETE_TASKS}}`
- `{{HANDOFF_NOTES}}`
