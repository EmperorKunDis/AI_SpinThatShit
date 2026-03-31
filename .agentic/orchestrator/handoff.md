# Handoff Protocol

## Required Sections

### 1. Summary
```markdown
**Agent:** developer
**Phase:** Phase 7.2
**Status:** PARTIAL (80% complete)
```

### 2. Completed Work
- What was done
- Files modified

### 3. Remaining Work
- What's left
- Specific file:line references

### 4. Recommendations
- Tips for next agent

### 5. Phase Status (REQUIRED v3.2.0 - Rule 6)

```markdown
**Phase Status:** COMPLETE | PARTIAL | BLOCKED

If PARTIAL:
- Tasks completed: X/Y
- Remaining tasks:
  - [ ] Task 1 (file:line)
  - [ ] Task 2 (file:line)
- Reason: Context limit / Time constraint / Blocker

If BLOCKED:
- Blocker: {description}
- Resolution needed: {specific action required}
- Estimated unblock: {what needs to happen}
```

**Rules:**
- NEVER use COMPLETE if checklist items are unchecked
- PARTIAL MUST list exact remaining tasks
- BLOCKED MUST describe resolution path

### 6. Security Block Warning (v3.2.0 - Rule 7)

If CRITICAL security issues were found:
```markdown
**SECURITY BLOCK:**
Phase {N+1} cannot proceed until:
- [ ] {Issue 1} - {file}:{line}
- [ ] {Issue 2} - {file}:{line}

**Risk if ignored:** {consequence}
```

---

## Enforcement

The Supervisor agent will verify:
1. Phase Status matches checklist.md state
2. PARTIAL status includes remaining tasks
3. Security blocks are properly documented
4. No "COMPLETE" status with unchecked items
