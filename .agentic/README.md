# 🤖 Agentic Configuration

This directory contains agent configurations, standards, and templates.

## Structure

```
.agentic/
├── agents/              # Agent-specific configurations
│   ├── planner/
│   ├── designer/
│   ├── engineer/
│   ├── developer/
│   ├── reviewer/
│   ├── tester/
│   └── supervisor/
├── orchestrator/        # Orchestration patterns
├── standards/           # Quality standards
└── templates/           # Project templates
```

## How It Works

1. **Installation**: `.agentic/` is copied to `~/.spinthatshit/.agentic/`
2. **Project Init**: Relevant files copied to project's `.spinstate/`
3. **Runtime**: Agents read their configs from these files
4. **Evolution**: Changes propagate back to source repo
