# Orchestrator Workflow

## Default Flow
```
planner → designer → engineer → developer → reviewer → tester → supervisor
   ↓          ↓          ↓          ↓           ↓         ↓          ↓
(check)    (check)    (check)    (check)     (check)   (check)   (always)
```

## Smart Skip
Each agent checks `should_skip_agent()` before running:
- No pending tasks → SKIP
- Phase complete → SKIP
- Role-specific conditions → SKIP

## Estimated Savings
- 40-60% agents skipped per cycle
- ~50k tokens saved per skip

---

## Phase State Rules (v3.2.0)

### Phase Atomicity (Rule 6)

A phase is COMPLETE only when:
- All frontend tasks checked [x]
- All backend tasks checked [x]
- Tests pass for modified files

**Valid States:**

| State | Checklist Requirement | Handoff Requirement |
|-------|----------------------|---------------------|
| COMPLETE | 100% items [x] | "Phase X Complete" |
| PARTIAL | <100% items [x] | List remaining tasks |
| BLOCKED | External dependency | Document blocker |

### Security Blocking (Rule 7)

If `blocked_by_security: true` in state.json:
- **ONLY** Phase X.5 (security) tasks allowed
- All other phases are BLOCKED
- Developer MUST address security first
- Supervisor validates security completion

### Enforcement

1. Before writing "PHASE_COMPLETE":
   - Count [x] vs [ ] items in checklist.md
   - Verify count matches phase requirements
2. Before starting new phase:
   - Check `blocked_by_security` in state.json
   - If true, redirect to security phase

---

## Test Coherence Check (v3.2.0 - Rule 5)

Before each commit, Developer must:
1. Identify modified files
2. Check for corresponding `.spec.ts` / `test_*.py`
3. Run tests for those files
4. Fix or document failures

**Never commit code that breaks its own tests.**
