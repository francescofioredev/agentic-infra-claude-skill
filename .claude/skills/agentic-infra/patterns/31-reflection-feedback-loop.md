# Pattern 31: Reflection Loop / Self-Critique

**Source**: awesome-agentic-patterns — Feedback Loops

## Intent
Implement a structured, multi-turn self-critique loop where an agent explicitly evaluates its own output against stated criteria, identifies specific weaknesses, and iteratively improves — distinct from Pattern 04 Reflection in that it emphasizes the **loop mechanics**, **stopping conditions**, and **feedback persistence** as first-class concerns.

## Context
Use when the agent must produce high-quality outputs in a domain where quality criteria are well-defined (code correctness, factual accuracy, style guide compliance, safety requirements) and a single LLM pass is reliably insufficient. Also applicable when integrating self-critique into long-horizon agents where intermediate outputs feed into subsequent steps.

## Forces / Tradeoffs
- **Depth vs. cost**: Each loop iteration adds at least one additional LLM call. Three iterations = 3× baseline cost.
- **Diminishing returns**: Reflection quality degrades after 2-3 iterations as the model runs out of novel critiques. Hard-cap iterations.
- **Critique quality**: Self-critique requires explicit, structured criteria. Vague criteria ("make it better") produce vague critiques that don't drive improvement.
- **Feedback persistence**: In multi-step agents, critiques of intermediate outputs must be propagated forward — not just used for the current revision.

## Solution
Implement a **Structured Critique-Revise-Evaluate** loop with explicit state management:

**State:**
- `draft`: current output under improvement
- `critique_history`: list of (iteration, critique, changes_made) tuples
- `quality_score`: current score against rubric
- `stopping_condition`: max iterations OR score threshold

**Loop:**
1. **Critique**: Invoke critic with `{task, draft, rubric, critique_history}`. Return `{issues: [{severity, location, description, fix_suggestion}], score}`.
2. **Check stopping**: if `score >= threshold` OR `iteration >= max_iterations` → exit.
3. **Revise**: Invoke reviser with `{task, draft, critique}`. Apply suggested fixes; produce new draft.
4. **Update state**: append to critique_history; update score.
5. Repeat.

**Key rules:**
1. Rubric must be explicit and measurable — include 3-7 criteria with clear pass/fail definitions.
2. Critique must be structured (not free-text): issues list with severity levels.
3. Reviser must explicitly acknowledge each issue in critique and either fix it or explain why it was not fixable.
4. Persist `critique_history` — it prevents the agent from re-introducing previously fixed issues.

**Pseudo-implementation:**
```python
draft = initial_draft
critique_history = []

for iteration in range(max_iterations):
    critique = critic.invoke({
        "task": task,
        "draft": draft,
        "rubric": rubric,
        "history": critique_history,
    })

    critique_history.append({
        "iteration": iteration,
        "critique": critique.issues,
        "score": critique.score,
    })

    if critique.score >= quality_threshold:
        break

    draft = reviser.invoke({
        "task": task,
        "draft": draft,
        "critique": critique,
        "history": critique_history,  # prevents re-introducing old issues
    })

return draft, critique_history
```

## Variants
- **External validator loop**: Replace LLM critic with a deterministic validator (unit tests, linter, type checker) and use LLM only for revision. Highest reliability for code generation.
- **Cross-agent critique**: Different agent persona critiques from a different perspective (e.g., security review, performance review, UX review).
- **Asynchronous reflection**: Long-running agent checkpoints intermediate outputs; reflection runs in parallel.
- **Critique caching**: If the same type of issue appears repeatedly across tasks, cache the critique pattern to reduce per-task reflection cost.

## Failure Modes
- **Sycophantic self-approval**: Model approves its own output without genuine critique. Mitigation: use an adversarial prompt framing ("Find at least 3 specific problems with this output").
- **Critique without revision**: Model produces detailed critique but reviser doesn't actually change the draft. Mitigation: compute diff between draft iterations; fail if diff is below minimum change threshold.
- **Re-introduction of fixed issues**: Revision fixes issue A but re-introduces previously fixed issue B. Mitigation: include `critique_history` in reviser prompt; explicitly instruct reviser to check history.
- **Score inflation**: Critic gives high scores too readily, exiting loop before quality is truly achieved. Mitigation: calibrate critic against human-labeled examples; use strict rubric.

## Instrumentation
- Track: `iterations_to_convergence`, `score_delta_per_iteration`, `convergence_failure_rate` (hit max without threshold).
- Alert: if `score_delta_per_iteration` < 0 (revision is degrading quality).
- Log: all drafts, critiques, and scores per iteration — essential for debugging quality regressions.

## Related Patterns
- **Reflection** (Pattern 04): Foundation pattern; this pattern adds explicit loop state management and feedback persistence.
- **Evaluation & Monitoring** (Pattern 19): LLM-as-Judge at the system level; Reflection Feedback Loop at the task level.
- **RLAIF** (Pattern 28): Training-time version of self-critique; Reflection Feedback Loop is inference-time.
- **Exception Handling & Recovery** (Pattern 12): When reflection cannot fix an issue within budget, escalate to exception handler.

## References
Source: awesome-agentic-patterns — Feedback Loops
