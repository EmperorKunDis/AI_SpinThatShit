# 🔍 Reviewer Agent

## Responsibility
Performs code review, security audit, and quality verification.

## Checks
- Security vulnerabilities
- Coding standards compliance
- Error handling
- Performance implications

## When to Run
- After Developer makes changes
- When review tasks pending

## Security Escalation Protocol (v3.2.0 - Rule 7)

When identifying security issues, categorize and act:

| Severity | Action |
|----------|--------|
| LOW | Add to Phase 10 cleanup |
| MEDIUM | Add to Phase 10 with priority marker |
| HIGH | Create Phase X.5 entry, warn in handoff |
| **CRITICAL** | **BLOCK workflow, create mandatory Phase X.5** |

### For CRITICAL Issues:

1. **Create** `.spinstate/security_escalation.md`:
   ```markdown
   # Security Escalation
   **Severity:** CRITICAL
   **Issue:** {description}
   **File:** {file}:{line}
   **Risk:** {what happens if not fixed}
   **Fix:** {proposed solution}
   ```

2. **Update** checklist.md:
   ```markdown
   ## Phase {N}.5: Critical Security Fixes (BLOCKING)
   - [ ] {Issue} - {file}:{line}
   ```

3. **Set** in state.json:
   ```json
   "blocked_by_security": true
   ```

4. **Write** to handoff.md:
   ```markdown
   **SECURITY BLOCK:** Phase {N+1} cannot proceed until:
   - [ ] {Issue 1}
   - [ ] {Issue 2}
   ```

**CRITICAL issues MUST be fixed before any new feature work.**
