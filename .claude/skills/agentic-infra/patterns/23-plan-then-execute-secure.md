# Pattern 23: Plan-Then-Execute (Security Variant)

**Source**: awesome-agentic-patterns — Orchestration & Control

## Intent
Separate plan formulation (using only trusted inputs) from plan execution (which encounters untrusted data), so that prompt injection in retrieved or user-provided content cannot alter the agent's pre-committed plan.

## Context
Use whenever an agent (1) accesses external data sources (web, databases, emails, files) during execution, and (2) takes consequential actions (send email, delete file, call API). The core threat: untrusted content in the environment instructs the agent to deviate from the user's intended task.

## Forces / Tradeoffs
- **Flexibility vs. security**: An agent that can revise its plan mid-execution is more capable but more vulnerable to injection. A frozen plan is less adaptive but auditable.
- **Plan completeness**: If the plan must be fully specified before seeing data, it may be too coarse. Mitigation: allow coarse plan steps that reference data retrieved at execution time, but no plan *modification* from retrieved content.
- **Overhead**: Two-phase approach adds a planning round-trip before any work starts.

## Solution
Implement a **two-phase protocol**:

**Phase 1 — Plan (trusted context only):**
1. Accept the user's goal and system prompt.
2. Query only pre-vetted, trusted data sources (internal DBs, user-provided files reviewed before the session).
3. Produce a structured, immutable plan: ordered list of `{step, tool, args_template}`.
4. Present the plan to the user for approval (optional HITL gate — see Pattern 13).

**Phase 2 — Execute (untrusted environment):**
1. Execute each plan step sequentially.
2. Fill `args_template` slots with data retrieved from the environment.
3. **Never allow retrieved content to modify the plan list** (no add/remove/reorder steps).
4. If a step fails, escalate to HITL rather than auto-replanning.

**Key rules:**
1. Treat all externally retrieved content as untrusted strings — never eval or re-prompt against it directly.
2. Store the approved plan as an immutable artifact; hash it and verify before each execution step.
3. If replanning is needed (e.g., step 3 reveals step 4 is impossible), require explicit user re-authorization.

**Pseudo-implementation:**
```python
plan = planner.invoke(goal, context=trusted_sources_only)
plan_hash = hash(plan)
user.approve(plan)  # optional HITL

for step in plan.steps:
    assert hash(plan) == plan_hash, "Plan was modified — abort"
    data = tool.call(step.tool, step.args_template)  # data is UNTRUSTED
    result = executor.run(step, data)  # data fills template slots, cannot modify plan
```

## Variants
- **Coarse + fine planning**: Phase 1 produces high-level steps; each step has a micro-planner that operates on trusted sub-goals only.
- **Verified execution**: Each execution step logs a signed audit record proving the action matched the approved plan.
- **Sandboxed execution**: Phase 2 runs in a restricted environment where the agent cannot modify its own prompts or instruction store.

## Failure Modes
- **Prompt injection via data**: Untrusted document contains `"IGNORE PREVIOUS INSTRUCTIONS"`. Mitigation: strict template substitution; never pass raw retrieved text as instructions.
- **Plan bypass**: Implementation bug allows an execution step to enqueue a new step. Mitigation: immutable plan data structure + hash check.
- **Overly rigid plan**: Plan commits to wrong tool before seeing data. Mitigation: allow parametric steps; require re-approval for structural changes.
- **HITL fatigue**: Frequent re-approval requests lead users to approve without reading. Mitigation: only escalate on consequential changes.

## Instrumentation
- Log: plan hash, each execution step input/output, any deviation attempt.
- Alert: if plan hash mismatch detected (potential injection or bug).
- Track: re-approval rate (high rate signals plan quality problems).

## Related Patterns
- **Planning** (Pattern 06): Base planning pattern; this variant adds the security separation.
- **Guardrails / Safety** (Pattern 18): Output filtering is a complementary control.
- **Human-in-the-Loop** (Pattern 13): HITL approval gate between planning and execution phases.
- **Sandboxed Tool Authorization** (Pattern 29): Restrict what tools can be called during execution.

## References
Source: awesome-agentic-patterns — Orchestration & Control
