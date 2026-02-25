# Design Example: Autonomous Software Engineering Agent

This example demonstrates community patterns **22–31** via a realistic design scenario: an autonomous coding agent that accepts a GitHub issue, implements a fix, runs tests, and opens a PR.

---

## Step 1: Identify Concerns

```yaml
orchestration:   sub-agent-spawning, plan-then-execute-secure, dual-llm
security:        sandboxed-authorization, plan-then-execute-secure
memory:          context-compaction
feedback:        reflection-feedback-loop
observability:   llm-observability
ux-collab:       spectrum-of-control
```

---

## Step 2: Pattern Selection

| Concern | Pattern | Rationale |
|---------|---------|-----------|
| Orchestration | **Sub-Agent Spawning** (24) | Spawn isolated agents per task phase: code-reader, implementer, test-runner |
| Security | **Plan-Then-Execute Secure** (23) | Plan from trusted sources (repo metadata); execute against untrusted file content |
| Security | **Sandboxed Tool Authorization** (29) | Deny-by-default; coding agent must not push to main without explicit grant |
| Security | **Dual LLM** (25) | Reasoner plans edits; Executor reads/writes files without seeing full system prompt |
| Context | **Context Compaction** (22) | Long file reads + test output fill context window in multi-file tasks |
| Feedback | **Reflection Feedback Loop** (31) | Validate generated code against rubric (compiles, tests pass, style) before PR |
| Observability | **LLM Observability** (30) | Trace cost/latency per sub-agent; alert on budget overrun |
| UX | **Spectrum of Control** (26) | Default Level 2 (batch confirm); promote to Level 3 after N successful PRs |

---

## Step 3: Architecture

### System Topology
```
GitHub Issue
  └─→ Orchestrator (trusted context only)
        ├─→ Plan: [read_repo_structure, identify_files, propose_edit_plan]  ← immutable
        └─→ Execute phase:
              ├─→ Reader Sub-Agent    (tools: read_file, grep_code)
              ├─→ Implementer Agent   (Dual LLM: Reasoner + File-Writer Executor)
              ├─→ Test-Runner Agent   (tools: run_tests — sandboxed container)
              └─→ Reflection Agent    (critique: compiles? tests pass? style ok?)
                                          ↓ if pass
                                    PR-Creator Agent   (HITL gate at Level 2)
```

### Pattern Applications

#### Plan-Then-Execute Secure (Pattern 23)
```python
# Phase 1 — Plan (trusted context: issue title, repo metadata, file list)
plan = planner.invoke(
    goal=issue.title,
    context=repo.metadata_only()   # NO file contents yet
)
plan_hash = hashlib.sha256(plan.json().encode()).hexdigest()
user.approve(plan)  # optional HITL at Level 2

# Phase 2 — Execute (untrusted: actual file content)
for step in plan.steps:
    assert hash_unchanged(plan, plan_hash), "Plan tampered — abort"
    data = tools.read_file(step.file_path)   # UNTRUSTED content
    result = executor.apply_edit(step, data)  # fills template slots only
```
Raw file content never reaches the Planner — it only receives structured extraction results.

#### Sub-Agent Spawning (Pattern 24)
```python
sub_tasks = [
    SubTask("read_repo", tools=["read_file", "grep_code"], timeout=30),
    SubTask("implement",  tools=["write_file"],             timeout=120, max_iterations=5),
    SubTask("run_tests",  tools=["bash_exec"],              timeout=60,  sandbox=True),
]
results = await gather(*[
    spawn_agent(task, context=plan.context_for(task))
    for task in sub_tasks
])
```
Each sub-agent gets only the context slice it needs. Test-runner runs in a fresh container.

#### Sandboxed Tool Authorization (Pattern 29)
```python
# Permission set derived at task start:
task_permissions = {
    "reader":      ["read_file:repo/*", "grep_code:repo/*"],
    "implementer": ["read_file:repo/*", "write_file:repo/src/*"],   # no write to main
    "test_runner": ["bash_exec:tests/*"],                            # no network
    "pr_creator":  ["gh_pr_create"],                                 # only after HITL
}
# pr_create is gated at Level 2 — user must approve the PR diff before creation
```

#### Dual LLM (Pattern 25)
```python
# Reasoner: sees goal + plan + structured test results; never sees raw file content
action = reasoner.plan_edit(goal, plan, structured_test_failures)

# Executor: sees raw file + action template; never sees system prompt or full goal
edited_file = executor.apply(
    file_content=raw_file,       # untrusted
    edit_action=action.template  # structured slot-filling only
)
```

#### Context Compaction (Pattern 22)
```python
def llm_call(messages):
    if count_tokens(messages) > 0.8 * MODEL_LIMIT:
        old_turns = messages[:-10]  # keep last 10 verbatim
        summary = summarizer.invoke(
            "Summarize preserving: files read, edits made, test results, open issues.\n"
            + format(old_turns)
        )
        messages = [{"role": "system", "content": f"[Compacted]\n{summary}"}] + messages[-10:]
    return client.messages(messages)
```
Triggered after large file reads and verbose test output that would otherwise overflow context.

#### Reflection Feedback Loop (Pattern 31)
```python
rubric = """
1. Code compiles without errors (verify via test_runner tool)
2. All existing tests pass
3. New behavior matches issue description
4. No security anti-patterns (hardcoded secrets, SQL injection, etc.)
5. Style guide compliant (ruff, mypy pass)
"""
for i in range(max_iterations=3):
    critique = critic.invoke({"draft": impl, "rubric": rubric, "history": history})
    history.append(critique)
    if critique.score >= 0.85:
        break
    impl = reviser.invoke({"draft": impl, "critique": critique, "history": history})
```
Critique history prevents re-introducing fixed issues across iterations.

#### LLM Observability (Pattern 30)
```python
with tracer.start_span("swe_agent.implement", {"issue_id": issue.id}) as span:
    for sub_agent in [reader, implementer, test_runner]:
        with tracer.start_child_span(sub_agent.name) as child:
            result = sub_agent.run()
            child.set_attributes({
                "tokens.input": result.usage.input,
                "tokens.output": result.usage.output,
                "cost_usd": compute_cost(result.usage, sub_agent.model),
                "finish_reason": result.finish_reason,
            })
# Alert if total task cost > $0.50 (budget threshold)
```

#### Spectrum of Control (Pattern 26)
```python
autonomy_config = {
    "read_file":   Level.AUTONOMOUS,   # no approval needed
    "write_file":  Level.MONITOR,      # execute + notify user
    "run_tests":   Level.AUTONOMOUS,
    "gh_pr_create": Level.BATCH_CONFIRM,  # user approves PR diff before creation
}
# After 10 successful PRs with zero reverts: promote write_file to AUTONOMOUS
```

---

## Step 4: Key ADR Decisions

| Decision | Pattern | Rationale |
|----------|---------|-----------|
| Immutable plan hash before file reads | Plan-Then-Execute (23) | File content could contain injection attempts |
| Dual LLM for file editing | Dual LLM (25) | File content should never reach the Reasoner's context |
| Deny-by-default per sub-agent | Sandboxed Auth (29) | PR creation must require explicit HITL at Level 2 |
| Compact after test output | Context Compaction (22) | Test verbose output can be 10k+ tokens |
| Max 3 reflection iterations | Reflection Loop (31) | Diminishing returns after iteration 2; tests are ground truth |
| OpenTelemetry trace per issue | LLM Observability (30) | Cost per issue needed for pricing and budget alerts |

---

## Step 5: Self-Check Against Review Checklist

| Area | Score | Notes |
|------|-------|-------|
| Architecture & Orchestration | 10/11 | *(open: explicit dependency graph between sub-agents)* |
| Tool Use & Integrations | 9/9 | All tools sandboxed and scoped |
| Memory & State | 8/10 | *(open: compaction TTL policy; cross-session issue history)* |
| Safety & Security | 12/12 | Plan separation + Dual LLM + sandbox + HITL gate |
| Evaluation & Observability | 9/9 | Distributed traces + reflection score as quality signal |
| Failure Modes & Recovery | 7/7 | Sub-agent timeout + reflection budget + plan hash abort |
| Cost Optimization | 4/4 | Haiku for Reader/Test-Runner; Sonnet for Implementer; Opus for Reasoner |
| **Total** | **59/62** | Production-ready |

---

## Lint Check

```bash
python3 scripts/lint_agentic_arch.py examples/community-design-example.md --format text
```

Expected: 0 CRITICAL (all guardrails, max_iterations, and HITL triggers are defined above).
