# Pattern 04: Reflection

## Intent
Improve output quality by having the agent (or a separate critic agent) critique its own output and iteratively refine it based on that critique.

## Context
Use when output quality is paramount and worth additional cost and latency. Typical domains: code generation, essay writing, structured data extraction, complex reasoning tasks where first-pass outputs are reliably improvable.

## Forces / Tradeoffs
- **Quality vs. cost/latency**: Each reflection loop adds at least one LLM call. Two-pass (generate + critique + revise) doubles token cost.
- **Convergence risk**: Without a stopping criterion, the agent may loop indefinitely or oscillate between versions.
- **Self-critique bias**: The same model that generated the output may not be an effective critic. A separate, distinct critic prompt or model reduces this bias.

## Solution
Implement a **Generator-Critic** (Producer-Critic) loop:
1. **Generator** produces an initial draft.
2. **Critic** evaluates the draft against explicit quality criteria and returns actionable feedback.
3. **Reviser** (or the Generator with critique in context) produces an improved draft.
4. Repeat until stopping criterion is met (max iterations OR quality threshold).

**Key rules:**
1. Provide the critic with explicit, measurable criteria (not "make it better") (p. 65).
2. Always set a maximum iteration count — prevent infinite loops (p. 67).
3. Use a separate critic prompt (different persona/instructions) to reduce self-critique bias (p. 68).
4. Pass the original input AND the draft to the critic so it can check fidelity to requirements (p. 66).

**Pseudo-implementation:**
```python
draft = generator.invoke(task)
for i in range(max_iterations):
    critique = critic.invoke({"task": task, "draft": draft})
    if critique["quality_score"] >= threshold:
        break
    draft = reviser.invoke({"task": task, "draft": draft, "critique": critique})
return draft
```

## Variants
- **Self-reflection**: Single model critiques and revises its own output in one prompt (cheaper, less effective).
- **Generator-Critic**: Separate generator and critic prompts (recommended, p. 68).
- **Multi-agent critic panel**: Multiple critic agents each evaluate a different dimension (correctness, style, completeness). Used in Agent Laboratory ReviewersAgent (p. 340).
- **Reflection with external tools**: Critic uses a code executor or web search to verify claims before giving feedback.

## Failure Modes
- **Infinite loop**: No stopping criterion → unbounded cost. Mitigation: hard max_iterations limit.
- **Sycophantic critique**: Critic approves poor output to avoid conflict. Mitigation: use a separate model/prompt with adversarial framing.
- **Degradation**: Revisions make output worse. Mitigation: track quality score across iterations; revert if score drops.
- **High cost**: 5 reflection cycles × 2 calls = 10× base cost. Mitigation: limit to 2-3 iterations for most tasks.

## Instrumentation
- Log: iteration number, draft at each step, critique content, quality score.
- Track: average iterations to convergence, convergence failure rate (hit max_iterations).
- Alert: if quality score not improving between iterations (signals stuck loop).

## Eval
- Compare final reflected output against un-reflected baseline on quality rubric.
- Measure win rate: "Reflection improved output" on human evaluation set.
- Verify stopping criterion fires correctly (quality threshold test).

## Related Patterns
- **Tool Use** (p. 81): Critic agent can use tools (code execution, search) to verify factual claims.
- **Multi-Agent Collaboration** (p. 121): Reflection is implemented as a Critic sub-agent in supervisor architectures.
- **Evaluation & Monitoring** (p. 301): LLM-as-a-Judge shares the critique rubric concept with Reflection.

## Evidence
- p. 61-68: "Reflection implements a Generator-Critic loop where the agent evaluates and revises its own output."
- p. 65: "Provide explicit evaluation criteria to the critic — vague feedback produces vague improvements."
- p. 68: "Using a separate critic prompt reduces the risk of the model approving its own flawed output."
- p. 340: Agent Laboratory's ReviewersAgent tripartite judgment mechanism (three reviewer personas).
