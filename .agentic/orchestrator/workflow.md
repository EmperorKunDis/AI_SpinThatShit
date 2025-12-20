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
