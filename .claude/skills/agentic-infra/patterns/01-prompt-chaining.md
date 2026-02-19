# Pattern 01: Prompt Chaining

## Intent
Break a complex task into a fixed sequence of LLM calls where each output feeds the next step as input.

## Context
Use when the task can be decomposed into discrete, ordered subtasks where each subtask's output is well-defined and feeds the next. The workflow is predictable and does not require runtime branching.

## Forces / Tradeoffs
- **Predictability vs. flexibility**: Chains are deterministic and debuggable but cannot handle dynamic branching.
- **Quality vs. speed**: Each step can be independently optimized and validated (including programmatic gates like regex checks), but latency accumulates linearly.
- **Simplicity vs. capability**: Chains are simpler to implement than planners or multi-agent systems but cannot self-correct or adapt.

## Solution
Decompose the task into N steps. Implement each step as a separate LLM prompt. Pass the output of step N as part of the input to step N+1. Optionally insert deterministic validation gates between steps (e.g., `assert len(output) > 0`).

**LangChain LCEL pattern** (p. 2):
```python
chain = prompt | model | output_parser
# Equivalent to: output = output_parser(model(prompt(input)))
```

**Key rules:**
1. Each prompt should request only what is needed for that step (p. 3).
2. Use XML tags or delimiters to pass structured context between steps (p. 3).
3. Insert programmatic validation (not LLM calls) between steps when possible — cheap and deterministic (p. 5).
4. Chains suit tasks whose decomposition is stable and known upfront (p. 7).

## Variants
- **Sequential pipeline**: Steps 1→2→3 strictly ordered.
- **Gated pipeline**: Programmatic checks between steps; abort on failure.
- **Prompted chain-of-thought**: Each step is a reasoning micro-step (see Reasoning Techniques, pattern 17).

## Failure Modes
- **Error propagation**: A bad output in step N silently corrupts step N+1. Mitigation: validate outputs between steps (p. 5).
- **Context loss**: Critical information from early steps is not passed downstream. Mitigation: explicitly forward required fields.
- **Over-chaining**: Splitting into too many tiny steps adds latency with no quality benefit.

## Instrumentation
- Log input/output of each step with step index and timestamp.
- Track inter-step latency to identify bottlenecks.
- Count validation gate failures per step (signals prompt quality issues).

## Eval
- Unit test each step independently with fixed inputs.
- Measure end-to-end output quality against a golden dataset.
- Check that removing a step degrades final output (validates necessity).

## Related Patterns
- **Routing** (p. 21): Add conditional dispatch between steps for dynamic branching.
- **Parallelization** (p. 41): Run independent steps concurrently instead of sequentially.
- **Reflection** (p. 61): Insert a critique-and-revise loop at any step for quality improvement.
- **Planning** (p. 101): Use a planner to dynamically generate the chain rather than hardcoding it.

## Evidence
- p. 1-3: "Prompt chaining decomposes tasks into a sequence of steps, where the output of one LLM call becomes the input of the next."
- p. 3: Gate examples — regex check, word count check between steps.
- p. 7: "Chains are best suited for tasks with a predictable, linear workflow."
