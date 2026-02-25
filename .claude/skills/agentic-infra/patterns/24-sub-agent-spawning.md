# Pattern 24: Sub-Agent Spawning

**Source**: awesome-agentic-patterns — Orchestration & Control

## Intent
Delegate well-scoped sub-tasks to isolated child agents that run with their own context, tools, and lifecycle, enabling parallel work, fault isolation, and specialization without polluting the orchestrator's context window.

## Context
Use when a task can be decomposed into independent or semi-independent sub-tasks that: (1) benefit from specialized toolsets or prompts, (2) can run concurrently to reduce latency, or (3) should be isolated so that a failure or runaway loop in one sub-task does not crash the orchestrator. Common in coding agents, research pipelines, and long-horizon automation.

## Forces / Tradeoffs
- **Parallelism vs. coordination overhead**: Spawning N agents requires N result aggregations; if sub-tasks are tightly coupled the coordination cost exceeds the parallelism benefit.
- **Context isolation**: Each sub-agent starts fresh — it cannot see the parent's history unless explicitly injected. This is a security benefit but requires careful context passing.
- **Cost multiplication**: N concurrent sub-agents = N× token cost. Use only when sub-tasks genuinely benefit from specialization or parallelism.
- **Observability complexity**: Distributed execution makes tracing and debugging harder.

## Solution
Implement a **Spawner-Worker** hierarchy:
1. **Orchestrator** decomposes the task into independent sub-tasks (see Pattern 06 Planning).
2. For each sub-task, the orchestrator **spawns a child agent** with: a scoped system prompt, relevant context slice, allowed tool set, and a result schema.
3. Child agents run concurrently (or serially, based on dependency graph).
4. Orchestrator **aggregates results** when all children complete (or applies timeout/cancellation).
5. Child agents are **terminated** after result delivery — no persistent state leaks.

**Key rules:**
1. Pass only the minimum necessary context to each child (least-privilege context).
2. Define a strict result schema — children return structured output, not free-form text.
3. Set a hard timeout and max-iteration cap on each child agent.
4. Never allow a child agent to spawn further children without explicit orchestrator authorization (prevents uncontrolled spawning trees).

**Pseudo-implementation:**
```python
sub_tasks = orchestrator.decompose(task)
futures = [
    spawn_agent(
        system_prompt=task.prompt,
        context=task.context_slice,
        tools=task.allowed_tools,
        result_schema=task.schema,
        timeout=60,
        max_iterations=10,
    )
    for task in sub_tasks
]
results = await gather(*futures)
final = orchestrator.aggregate(results)
```

## Variants
- **Background agents**: Long-running sub-agents that execute asynchronously; orchestrator polls for completion or receives a webhook.
- **Hierarchical spawning (controlled)**: Sub-agents may spawn their own children, but only from a pre-approved spawn list defined by the orchestrator.
- **Ephemeral sandboxed agents**: Each sub-agent runs in a fresh OS process/container with no access to parent filesystem.
- **Fan-out / fan-in**: Orchestrator fans out N identical tasks to N agents with different data slices (e.g., parallel document analysis).

## Failure Modes
- **Uncontrolled spawn explosion**: Child spawns children without limit → exponential cost. Mitigation: enforce spawn depth limit (max depth 2) and total agent count cap.
- **Context leakage**: Orchestrator passes full history to child → child re-executes completed work. Mitigation: always construct minimal context slice per child.
- **Silent child failure**: Child times out or errors without reporting → orchestrator hangs. Mitigation: always collect child exit status; treat timeout as failure.
- **Result schema mismatch**: Child returns unexpected structure → aggregation fails. Mitigation: validate child output against schema before aggregation.

## Instrumentation
- Track: `agents_spawned_per_task`, `child_completion_time`, `child_failure_rate`, `total_tokens_across_children`.
- Alert: if `agents_spawned_per_task` exceeds expected bound (signals uncontrolled decomposition).
- Log: parent-child relationship tree for each task execution (enables full distributed trace).

## Related Patterns
- **Multi-Agent Collaboration** (Pattern 07): Peer agents; sub-agent spawning is a hierarchical variant.
- **Planning** (Pattern 06): Decomposition is the pre-condition for spawning.
- **Parallelization** (Pattern 03): Sub-agent spawning is one implementation of parallelization.
- **Sandboxed Tool Authorization** (Pattern 29): Apply per-child tool restrictions.
- **LLM Observability** (Pattern 30): Distributed tracing across spawned agents.

## References
Source: awesome-agentic-patterns — Orchestration & Control
