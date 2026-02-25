# Pattern 26: Spectrum of Control / Blended Initiative

**Source**: awesome-agentic-patterns — UX & Collaboration

## Intent
Design agent autonomy as a continuously adjustable dial rather than a binary human/agent toggle, allowing the system to operate anywhere from fully manual to fully autonomous depending on task risk, user trust level, and context.

## Context
Use when building agents that must serve different users with different risk tolerances, or a single user across tasks of varying consequence (e.g., reading emails vs. sending emails vs. deleting accounts). A fixed autonomy level is either too restrictive (frustrating for routine tasks) or too permissive (dangerous for high-stakes actions).

## Forces / Tradeoffs
- **Productivity vs. safety**: Higher autonomy increases throughput but raises risk of unrecoverable mistakes.
- **User trust calibration**: Trust must be earned over time; new users or new task types should start at lower autonomy levels.
- **Cognitive load**: Too many approval prompts causes approval fatigue — users rubber-stamp without reading.
- **Consistency**: Unpredictable autonomy level (switches without user awareness) erodes trust.

## Solution
Implement a **5-level autonomy spectrum** with explicit transitions:

| Level | Name | Agent Behavior | Human Role |
|-------|------|---------------|------------|
| 0 | Manual | Agent suggests actions; human executes | Full control |
| 1 | Confirm-all | Agent proposes each step; human approves | Gate every action |
| 2 | Batch confirm | Agent plans full sequence; human approves before execution | Pre-approve plan |
| 3 | Monitor | Agent executes; human notified after each step; can interrupt | Oversight |
| 4 | Autonomous | Agent executes; human sees summary; can audit | Post-hoc review |

**Key rules:**
1. **Default to the lowest safe level** for a new user/task; promote levels based on demonstrated success rate.
2. **Always allow instant downshift**: user can reduce autonomy level mid-task without aborting.
3. **Escalate on uncertainty**: if the agent's confidence falls below a threshold, automatically drop to Level 1 for that action.
4. **Surface the current level** prominently in the UI — never let users forget what the agent is allowed to do autonomously.
5. **Hard floor for irreversible actions** (delete, send, publish): always Level 1 or lower, regardless of global setting.

**Pseudo-implementation:**
```python
def execute_action(action, user_profile, autonomy_level):
    if action.is_irreversible:
        effective_level = min(autonomy_level, 1)
    else:
        effective_level = autonomy_level

    if effective_level <= 1:
        user.approve(action)
    result = tool.execute(action)
    if effective_level == 3:
        user.notify(action, result)
    return result
```

## Variants
- **Task-scoped autonomy**: Different levels for different task categories (read-only: Level 4; write: Level 2; delete: Level 1).
- **Time-of-day gating**: Higher autonomy during business hours (human available to interrupt); lower autonomy overnight.
- **Adaptive promotion**: System automatically suggests upgrading autonomy level after N consecutive successful executions.
- **Reversibility-gated autonomy**: Fully autonomous only for actions with a clear undo path.

## Failure Modes
- **Approval fatigue**: Level 1 with high-frequency actions → users approve everything without reading. Mitigation: auto-batch low-risk actions; reserve individual approval for high-stakes steps.
- **Silent level creep**: System promotes to higher autonomy without explicit user consent. Mitigation: require explicit user confirmation for any level promotion.
- **Inconsistent floors**: Developers hardcode different irreversible-action floors across features. Mitigation: centralize irreversibility classification in a shared action registry.
- **Opacity**: User doesn't know current level → surprises when agent acts autonomously. Mitigation: always display current level in UI.

## Instrumentation
- Track: `current_autonomy_level`, `actions_per_level`, `approval_rate_by_level` (% of proposals approved vs. rejected).
- Alert: if approval rate at Level 1 exceeds 99% (approval fatigue indicator).
- Log: every level change (who initiated, when, previous level → new level).

## Related Patterns
- **Human-in-the-Loop** (Pattern 13): HITL is Level 1 in this spectrum; Spectrum of Control generalizes it.
- **Goal Setting & Monitoring** (Pattern 11): Goal confidence score drives autonomy level escalation/de-escalation.
- **Exception Handling & Recovery** (Pattern 12): Automatic downshift to lower autonomy on exception detection.
- **Guardrails / Safety** (Pattern 18): Guardrails enforce the hard floors at Level 1 for irreversible actions.

## References
Source: awesome-agentic-patterns — UX & Collaboration
