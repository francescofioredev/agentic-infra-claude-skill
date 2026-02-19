# Pattern 17: Reasoning Techniques

## Intent
Apply structured reasoning techniques (CoT, ToT, ReAct, CoD, debate-based methods) to improve the quality and verifiability of agent reasoning, especially for complex multi-step problems.

## Context
Use when agent outputs require verifiable reasoning traces, when problems benefit from exploring multiple solution paths, when the agent must interleave thinking with action, or when reasoning cost (tokens) needs to be reduced without sacrificing quality.

## Forces / Tradeoffs
- **Reasoning depth vs. token cost**: More thorough reasoning (ToT, debate) produces better answers but consumes more tokens.
- **Determinism vs. exploration**: CoT is more deterministic; ToT and Self-Consistency explore multiple paths (better quality, higher cost).
- **Inference time vs. training time**: Scaling inference compute (longer CoT, more candidates) can substitute for training on harder problems.

## Solution

### Chain-of-Thought (CoT) (p. 265)
**Zero-shot CoT**: Append "Let's think step by step" to prompt — elicits step-by-step reasoning (p. 358, App A).
**Few-shot CoT**: Include worked examples with full reasoning chains in the prompt.
```python
# temperature=0 for reproducibility in CoT
response = llm.invoke(prompt + "\nLet's think step by step.", temperature=0)
```

### Self-Consistency (p. 266)
Generate N independent CoT paths → majority vote on final answer:
```python
answers = [llm.invoke(cot_prompt) for _ in range(5)]
final_answer = majority_vote(answers)  # More reliable than single chain
```

### Tree of Thoughts (ToT) (p. 267)
Explore multiple reasoning paths as a tree; evaluate and prune at each node:
- Good for: combinatorial search, multi-step planning with backtracking.

### ReAct (Reason + Act) (p. 268)
Interleave reasoning (Thought) with action (Action) and observation (Observation):
```
Thought: I need to find the current population of Paris.
Action: search_web("population of Paris 2024")
Observation: The population of Paris is approximately 2.1 million.
Thought: Now I can calculate the population density.
Action: calculate(population=2100000, area_km2=105)
Observation: Population density = 20,000 per km².
Answer: The population density of Paris is approximately 20,000 people/km².
```

### Chain of Debates (CoD) — Microsoft (p. 270)
Multiple agents debate different positions on a question → synthesized consensus answer. Reduces individual model biases.

### Graph of Debates (GoD) (p. 271)
Non-linear debate topology where agents can reference any prior argument, not just the previous turn. More expressive than CoD.

### Chain of Draft (CoD — condensed reasoning) (p. 272)
Generate minimal reasoning tokens — 5-7 words per reasoning step rather than full sentences. Up to 80% token reduction with comparable quality on certain tasks.

**Key rules:**
1. Use CoT with temperature=0 for deterministic, reproducible reasoning (p. 358, App A).
2. Use Self-Consistency (multiple paths) when answer quality matters more than speed (p. 266).
3. ReAct is the default for tool-using agents — it naturally handles Thought-Action-Observation loops (p. 268).
4. Use Chain of Draft when token cost is a concern for reasoning-heavy workloads (p. 272).
5. For research-grade tasks, CoD (debates) and GoD provide richer multi-perspective analysis (p. 270-271).

## Variants
- **Zero-shot CoT**: "Let's think step by step" appended (p. 358).
- **Few-shot CoT**: Include example reasoning chains.
- **Self-Consistency**: N parallel CoT paths + majority vote (p. 266).
- **Step-Back Prompting**: First derive abstract principle, then apply to specific task (p. 362, App A).
- **ReAct**: Thought-Action-Observation loop for tool-using agents (p. 268).
- **APE / DSPy**: Automated prompt engineering to optimize CoT prompts (p. 365, App A).

## Failure Modes
- **CoT hallucination amplification**: If the first reasoning step is wrong, subsequent steps compound the error. Mitigation: Self-Consistency (multiple paths reduces single-path errors).
- **ToT combinatorial explosion**: Too many branches → exponential cost. Mitigation: beam search with fixed beam width.
- **ReAct loop**: Agent keeps taking actions without converging on an answer. Mitigation: max_steps limit.
- **Majority vote on continuous outputs**: Majority voting doesn't apply to numeric/text outputs directly. Mitigation: use LLM as judge to rank/select best answer.

## Instrumentation
- Log: reasoning trace (each Thought/Action/Observation), number of reasoning steps.
- Track: reasoning step count distribution, token usage per reasoning pattern.
- Compare: quality score with vs. without CoT on evaluation set.

## Eval
- Evaluate CoT reasoning chains for correctness (not just final answers).
- Test Self-Consistency: verify majority vote produces better results than single-path on held-out set.
- Test ReAct: verify agent converges to correct answer within max_steps.

## Related Patterns
- **Tool Use** (p. 81): ReAct is the reasoning framework within which tools are invoked.
- **Reflection** (p. 61): CoT provides the reasoning trace; Reflection critiques it.
- **Resource-Aware Optimization** (p. 255): Chain of Draft reduces reasoning token cost.
- **Multi-Agent Collaboration** (p. 121): CoD/GoD implement multi-agent debate.

## Evidence
- p. 261-272: Reasoning Techniques chapter. CoT, ToT, Self-Correction, ReAct, CoD, GoD, MASS, Scaling Inference Law.
- p. 265: ReAct: Thought-Action-Observation loop.
- p. 266: Self-Consistency: multiple paths + majority vote.
- p. 268: Chain of Debates (CoD) — Microsoft.
- p. 270: Graph of Debates (GoD) — non-linear topology.
- p. 272: Chain of Draft — 80% token reduction.
- p. 358: Zero-shot CoT: "Let's think step by step" — temperature=0.
