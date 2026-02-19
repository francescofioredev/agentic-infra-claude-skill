# Pattern 02: Routing

## Intent
Use an LLM (or rule-based logic) to classify an input and dispatch it to the most appropriate specialized handler or sub-pipeline.

## Context
Use when different input types require fundamentally different processing paths, and a single monolithic pipeline would be suboptimal for all of them. The router acts as the entry point that matches inputs to specialists.

## Forces / Tradeoffs
- **Specialization vs. complexity**: Routing enables specialized prompts per input type, but adds architectural complexity and a potential mis-routing failure mode.
- **LLM routing vs. rule-based routing**: LLM-based routing is flexible and handles edge cases; rule-based routing (regex, keywords) is cheaper and deterministic.
- **Latency**: An extra LLM call at entry adds latency to every request.

## Solution
Implement a router that:
1. Receives the raw input.
2. Classifies it into one of N categories.
3. Dispatches to the corresponding handler.
4. Returns the handler's output.

**LangChain `RunnableBranch` pattern** (p. 25):
```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: "technical" in x["topic"].lower(), technical_chain),
    (lambda x: "billing" in x["topic"].lower(), billing_chain),
    general_chain,  # default fallback
)
```

**Google ADK `sub_agents` with Auto-Flow** (p. 28):
```python
root_agent = Agent(
    name="router",
    sub_agents=[technical_agent, billing_agent, general_agent],
    # ADK auto-selects sub-agent based on description matching
)
```

**Key rules:**
1. Always provide a default/fallback handler for unclassified inputs (p. 27).
2. Keep router logic separate from handler logic — don't mix classification and processing (p. 26).
3. Log the routing decision and confidence for observability (p. 26).
4. For high-stakes routing, use few-shot examples in the router prompt to improve accuracy (p. 27).

## Variants
- **LLM-based router**: Prompt asks the model to classify and return a category label.
- **Embedding-based router**: Cosine similarity to category exemplars — no LLM call needed.
- **Rule-based router**: Regex or keyword matching — fastest and most predictable.
- **ADK Auto-Flow**: Agent descriptions drive automatic sub-agent selection (p. 28).

## Failure Modes
- **Mis-routing**: Input classified into wrong category → wrong handler processes it. Mitigation: confidence threshold + human escalation.
- **No fallback**: Unrecognized input causes a crash. Mitigation: always define a default branch.
- **Router bottleneck**: All traffic passes through one LLM call — becomes a latency/cost hotspot.

## Instrumentation
- Log: input category label, routing decision, confidence score, handler selected.
- Alert on: routing to fallback > X% of traffic (signals classification drift).
- Track per-handler success rates to detect category-specific regressions.

## Eval
- Build a labeled routing test set with known correct categories.
- Measure router accuracy (correct dispatches / total inputs).
- Test fallback path with out-of-distribution inputs.

## Related Patterns
- **Prompt Chaining** (p. 1): Routing can precede a chain — router selects which chain to run.
- **Multi-Agent Collaboration** (p. 121): Supervisor pattern is an extended form of routing across agents.
- **Tool Use** (p. 81): Router can dispatch to tool-using agents rather than pure LLM chains.

## Evidence
- p. 21-25: "Routing implements a conditional dispatch mechanism — the LLM classifies the input and the system routes it to the appropriate handler."
- p. 25: `RunnableBranch` code example.
- p. 28: ADK `sub_agents` with Auto-Flow description matching.
- p. 27: "Always include a default fallback to handle unclassified inputs."
