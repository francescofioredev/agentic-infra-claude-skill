# Pattern 06: Planning

## Intent
Enable an agent to decompose a high-level goal into an ordered sequence of actionable sub-tasks before executing, rather than reacting step-by-step.

## Context
Use when the task is complex, multi-step, and requires coordinating multiple capabilities (tools, sub-agents, data sources). Planning separates the "what to do" from the "how to do it", elevating the agent from a reactive executor to a strategic planner.

## Forces / Tradeoffs
- **Flexibility vs. predictability**: Plans can be regenerated dynamically when steps fail, but this makes behavior harder to predict and audit.
- **Upfront planning vs. reactive execution**: Planning all steps upfront is efficient when the task is well-understood; reactive (ReAct-style) planning is more adaptive but slower.
- **Plan depth**: Deep plans (many sub-tasks) are expressive but harder to execute reliably.

## Solution
A **Plan-then-Execute** architecture:
1. **Planner LLM**: Receives the user goal → outputs a structured plan (ordered list of steps with dependencies).
2. **Executor**: Iterates through the plan, invoking tools or sub-agents for each step.
3. **Plan updater (optional)**: After each step, assess whether the plan needs revision based on intermediate results.

**Structured plan output example** (p. 107):
```python
plan_prompt = """
Given the goal: {goal}
Produce a JSON plan:
{
  "steps": [
    {"id": 1, "action": "search_web", "args": {"query": "..."}, "depends_on": []},
    {"id": 2, "action": "summarize", "args": {}, "depends_on": [1]},
    ...
  ]
}
"""
```

**Key rules:**
1. Use structured output (JSON/Pydantic) for the plan to make it programmatically executable (p. 107).
2. Include `depends_on` fields in plan steps to enable parallel execution of independent steps (p. 108).
3. Design the planner to output a minimal plan — LLMs tend to over-plan; prune unnecessary steps (p. 109).
4. For long-horizon tasks, use **hierarchical planning**: high-level plan → sub-plans per step (p. 110).
5. Always validate plan feasibility before execution (check tools/agents referenced exist) (p. 111).

## Variants
- **Static planning**: Plan fully generated upfront, executed without changes.
- **Dynamic re-planning**: Plan updated after each step based on results. Higher quality but more LLM calls.
- **Hierarchical planning**: Top-level plan decomposed into sub-plans. Used in multi-agent systems (p. 130, Ch 7).
- **ReAct (reactive planning)**: No upfront plan; agent decides next action one step at a time based on observations (p. 265, Ch 17).

## Failure Modes
- **Infeasible plan**: Plan references tools or data that don't exist. Mitigation: validate plan against available capabilities before execution.
- **Stale plan**: Plan becomes invalid as environment changes during execution. Mitigation: re-planning checkpoints.
- **Over-planning**: Too many fine-grained steps → high latency and cost. Mitigation: encourage brevity in planner prompt.
- **Circular dependencies**: Steps A→B→A creates an infinite loop. Mitigation: topological sort check on plan graph.

## Instrumentation
- Log: the full plan at generation time, step completions, re-planning events.
- Track: plan completion rate (steps completed / total steps), re-planning frequency.
- Alert: if plan contains > N steps (cost/latency risk).

## Eval
- Provide a fixed goal; evaluate whether the generated plan contains all necessary steps (recall).
- Test plan execution on a harness with mock tools; verify all steps complete successfully.
- Measure plan efficiency: does it produce correct output with minimal steps?

## Related Patterns
- **Tool Use** (p. 81): Plans typically execute by invoking tools at each step.
- **Multi-Agent Collaboration** (p. 121): Hierarchical planning maps to supervisor delegating to sub-agents.
- **Exception Handling** (p. 201): Recovery strategies for failed plan steps.
- **Prioritization** (p. 321): Dynamic re-ordering of plan steps based on urgency/importance.

## Evidence
- p. 101-111: "Planning decomposes a high-level goal into an ordered sequence of actionable sub-tasks."
- p. 107: Structured JSON plan output with `depends_on` for dependency tracking.
- p. 109: "LLMs tend to over-plan — prune unnecessary steps."
- p. 110: Hierarchical planning for long-horizon tasks.
