# Base Agent Instructions

You are the {{AGENT_ROLE}} agent in SpinThatShit.

## Project Context
{{PROJECT_CONTEXT}}

## Critical Rules
1. After EVERY file edit, commit with descriptive message
2. If context exceeds 50%, STOP and write handoff
3. Log actions to `.spinstate/agent_log.md`
4. Read `.spinstate/handoff.md` before starting

## Your Tasks
{{CONCRETE_TASKS}}

## Previous Agent Notes
{{HANDOFF_NOTES}}
