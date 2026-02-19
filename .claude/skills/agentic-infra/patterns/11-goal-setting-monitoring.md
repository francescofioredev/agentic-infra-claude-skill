# Pattern 11: Goal Setting & Monitoring

## Intent
Give agents explicit, measurable goals and an ongoing mechanism to verify whether those goals have been met, preventing indefinite execution and enabling course correction.

## Context
Use whenever an agent executes a multi-step task that might have unclear termination conditions, or when the agent must track progress toward a complex objective. Without explicit goals, agents either terminate too early (miss the objective) or loop indefinitely.

## Forces / Tradeoffs
- **Goal specificity vs. flexibility**: Specific SMART goals are easier to evaluate but may be too rigid for open-ended tasks.
- **Goal checking cost**: Every `goals_met()` check is an LLM call — adds cost per iteration.
- **Goal drift**: In long tasks, the agent may achieve sub-goals while losing sight of the top-level objective.

## Solution
Apply **SMART goals** (p. 185):
- **Specific**: Clear, unambiguous statement of what must be achieved
- **Measurable**: Quantifiable completion criteria
- **Achievable**: Within the agent's capability and tool access
- **Relevant**: Aligned with user intent
- **Time-bound**: Has a completion deadline or iteration limit

**goals_met() LLM checker** (p. 188):
```python
def goals_met(original_goal: str, current_state: dict) -> bool:
    """Use LLM to determine if goal has been achieved."""
    prompt = f"""
    Original goal: {original_goal}
    Current state: {current_state}

    Has the goal been fully achieved? Answer only 'true' or 'false'.
    """
    result = llm.invoke(prompt).content.strip().lower()
    return result == "true"

# In agent loop:
while not goals_met(goal, state) and iterations < max_iterations:
    state = agent.step(state)
    iterations += 1
```

**Iterative goal refinement** (p. 190):
When goals are ambiguous, implement a clarification phase before execution:
1. Agent parses the user request and identifies ambiguities
2. Agent asks targeted clarifying questions
3. Refined goal is stored in state before execution begins

**Key rules:**
1. Always express the goal as a structured object (string or Pydantic model) — not implicit in the prompt (p. 186).
2. Set `max_iterations` alongside the goal — prevents infinite loops when `goals_met()` never returns true (p. 188).
3. For complex goals, decompose into sub-goals with their own completion criteria (p. 191).
4. Log the goal and each `goals_met()` evaluation for debugging (p. 192).

## Variants
- **Single goal**: Simple boolean completion check.
- **Goal hierarchy**: Top-level goal + ordered sub-goals; agent must complete all sub-goals.
- **Goal with metrics**: Goal defined as achieving a quantitative threshold (e.g., "find 10 valid results").
- **Dynamic goal refinement**: Agent clarifies and refines the goal with the user before starting (p. 190).

## Failure Modes
- **Underspecified goal**: `goals_met()` never returns true because goal is ambiguous. Mitigation: structured goal specification with explicit success criteria.
- **Early termination**: `goals_met()` incorrectly returns true on partial completion. Mitigation: provide examples of incomplete states in the prompt.
- **Infinite loop**: Goal unreachable but `max_iterations` not set. Mitigation: always set max_iterations.
- **Goal substitution**: Agent achieves a different (easier) goal than intended. Mitigation: include negative examples in `goals_met()` prompt.

## Instrumentation
- Log: goal text at task start, each `goals_met()` evaluation result, iteration count.
- Track: task completion rate (% where goal was fully met), average iterations to completion.
- Alert: tasks hitting max_iterations without goal completion.

## Eval
- Provide a fixed set of tasks with known completion states; verify `goals_met()` accuracy.
- Test that `goals_met()` correctly returns false for partial completions.
- Test early stopping: agent completes in fewer iterations than max.

## Related Patterns
- **Planning** (p. 101): Planning decomposes goals into a sequence of steps.
- **Exception Handling** (p. 201): When a step fails, recovery must re-align with the original goal.
- **HITL** (p. 207): Escalate to human when `goals_met()` cannot be determined.
- **Evaluation & Monitoring** (p. 301): SMART goal criteria align with evaluation metric definition.

## Evidence
- p. 183-192: Goal Setting chapter. SMART goals framework.
- p. 185: SMART goal criteria applied to agent tasks.
- p. 188: `goals_met()` LLM True/False checker implementation.
- p. 190: Iterative goal clarification before execution.
