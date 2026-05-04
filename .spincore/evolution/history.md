# Evolution History

## v3.2.0 (2025-12-21) - Quality & Safety Rules

### Root Cause Analysis (PostHub Sessions 2-4)
Evolver agent analyzed 3 recurring patterns:
1. Test-Code Drift (9 false test failures)
2. Partial Phase Completion (Phase 8 Backend skipped)
3. Security Escalation Gap (4 CRITICAL issues unaddressed)

### New Rules

**Rule 5: Test Coherence Gate**
- Developer MUST run tests for modified files before commit
- If `auth.service.ts` modified, run `auth.service.spec.ts`
- Prevents code-test mismatch issues

**Rule 6: Phase Atomicity**
- Phases can only be COMPLETE, PARTIAL, or BLOCKED
- COMPLETE requires ALL items checked (frontend + backend)
- PARTIAL MUST list exact remaining tasks
- Prevents orphaned work

**Rule 7: Security Escalation Protocol**
- CRITICAL findings create mandatory Phase X.5
- `blocked_by_security: true` blocks other phases
- Ensures security issues are addressed before features

### Files Modified
- `.agentic/agents/developer/README.md` - Added Rules 5, 6
- `.agentic/agents/reviewer/README.md` - Added Rule 7
- `.agentic/orchestrator/workflow.md` - Added phase rules
- `.agentic/orchestrator/handoff.md` - Added phase status section
- `.agentic/standards/quality.md` - Added item 14 (Test Coherence)

### Expected Outcomes
- 0 test-code drift incidents
- 0 orphaned partial phases
- 0 unaddressed CRITICAL security issues

---

## v3.0.1 (2025-12-20) - Bugfix
- Fixed `NameError: name 'ProjectState' is not defined` forward reference error
- Added `from __future__ import annotations` for postponed annotation evaluation

## v3.0.0 (2025-12-20) - Major Enhancement Release

### Phase 1: Structured Logging
- `AgentLogger` class with JSON Lines output
- Session tracking with unique IDs
- Colored console output with context indicators
- Session export and summary statistics

### Phase 2: Memory Management
- `ContextManager` with memory blocks architecture
- 6 priority-based blocks (system, project, task, history, tools, handoff)
- Automatic context compaction at 40% threshold
- Serialization/deserialization for checkpoints

### Phase 3: Enhanced Prompt Engineering
- `PromptEnhancer` with Chain of Thought injection
- Self-verification checklists in prompts
- Negative examples (what NOT to do)
- Few-shot examples for Developer, Planner, Reviewer

### Phase 4: Error Handling & Security
- `retry_with_backoff` decorator with exponential backoff + jitter
- Error classification (TRANSIENT, RECOVERABLE, PERMANENT)
- `SecretDetector` with 13 pattern types (API keys, tokens, passwords)
- Automatic secret scanning before commits

### Phase 5: Tool Optimization
- `FileCache` with LRU eviction and modification detection
- `CodeAnalyzer` with ruff/eslint integration
- Fallback to py_compile for syntax checking

### Phase 6: Workflow & UX
- `CheckpointManager` with history tracking
- `InteractiveController` for human-in-the-loop approval
- Session resume from checkpoints
- New CLI flags: --interactive, --list-checkpoints, --restore-checkpoint

### Integration
- All components integrated into main Orchestrator
- Post-agent security and quality scans
- Structured logging throughout workflow
- Graceful shutdown with checkpoint save

## v2.1.0 (2025-12-19)
- Circuit Breaker
- Security Library Rules
