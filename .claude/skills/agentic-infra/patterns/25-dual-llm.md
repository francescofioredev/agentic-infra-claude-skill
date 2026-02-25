# Pattern 25: Dual LLM Pattern

**Source**: awesome-agentic-patterns — Orchestration & Control

## Intent
Use two distinct LLM instances with different roles — one for reasoning/planning (trusted) and one for execution/action (constrained) — to prevent the reasoning model's context from being contaminated by untrusted environment data, and to apply tighter safety constraints to the execution model.

## Context
Use when an agent must reason over trusted instructions AND interact with untrusted external content (user uploads, web pages, third-party APIs). Combining both in a single model creates a single point of compromise: injected content in external data can hijack the reasoning process. A Dual LLM architecture creates an explicit security boundary.

## Forces / Tradeoffs
- **Security vs. complexity**: Two models add architectural complexity and 2× the LLM call cost for each reasoning+execution cycle.
- **Latency**: Sequential calls (reason → execute) add round-trip latency vs. a single-model approach.
- **Model capability mismatch**: The execution model may be smaller/cheaper but less capable; complex tasks may require a capable model in both roles.
- **Context synchronization**: The two models share no context by default; the orchestrator must selectively pass information between them.

## Solution
Implement a **Privileged Reasoner / Constrained Executor** split:

**Privileged LLM (Reasoner):**
- Sees only: system instructions, user goals, trusted tool schemas, high-level results from executor.
- Never receives: raw retrieved documents, user-uploaded files, external API responses directly.
- Produces: structured action plans, tool invocation intents, or structured queries.

**Constrained LLM (Executor):**
- Sees only: structured action from Reasoner + the raw untrusted data needed for that action.
- Has: restricted tool permissions, output length limits, no access to system instructions.
- Produces: structured results only (not free-form instructions).

**Orchestrator** sits between them:
1. Pass user goal to Reasoner → get action plan.
2. Execute action plan: fetch untrusted data, pass to Executor.
3. Return Executor's structured result to Reasoner (not raw data).
4. Repeat until goal satisfied.

**Key rules:**
1. The Reasoner must never receive raw untrusted content — only Executor's structured output.
2. The Executor must never receive the full system prompt or user goal (only the specific action to take).
3. Use separate API keys or model instances so a bug in one cannot leak to the other.

**Pseudo-implementation:**
```python
goal = user.input()
while not done:
    action = reasoner.plan(goal, history_of_structured_results)
    # action = {tool: "web_fetch", url: "...", extract_schema: {...}}
    raw_data = tool.fetch(action.url)
    structured = executor.extract(raw_data, action.extract_schema)
    # executor never sees goal or system prompt
    history_of_structured_results.append(structured)
    done = reasoner.is_done(goal, history_of_structured_results)
```

## Variants
- **Small + large model split**: Executor uses a smaller, cheaper model (e.g., Haiku) for data extraction; Reasoner uses a larger model (e.g., Opus) for planning.
- **Read-only executor**: Executor can only read/extract, never write or call action APIs.
- **Triple LLM**: Add a Validator between Executor output and Reasoner input to check for injection attempts.

## Failure Modes
- **Result smuggling**: Executor encodes malicious instructions in its structured output (e.g., in a `notes` field). Mitigation: validate executor output strictly against schema; reject any fields not in schema.
- **Reasoner context growth**: History of structured results eventually becomes large. Mitigation: apply context compaction (Pattern 22) to result history.
- **Capability gap**: Executor is too weak to extract complex information. Mitigation: use a capable model for both; accept cost trade-off.
- **Synchronization drift**: Reasoner makes assumptions about executor capabilities that are wrong. Mitigation: test executor capabilities in isolation.

## Instrumentation
- Log: all Reasoner action plans, all Executor structured results.
- Track: `reasoner_tokens`, `executor_tokens`, separately.
- Alert: if executor output contains unexpected free-text (signals extraction failure or injection attempt).

## Related Patterns
- **Plan-Then-Execute Secure** (Pattern 23): Complementary — Dual LLM separates models; Plan-Then-Execute separates phases.
- **Guardrails / Safety** (Pattern 18): Apply guardrail checks to Executor output before passing to Reasoner.
- **Sandboxed Tool Authorization** (Pattern 29): Apply tool restrictions to the Executor.
- **Multi-Agent Collaboration** (Pattern 07): Dual LLM is a minimal two-agent collaboration pattern.

## References
Source: awesome-agentic-patterns — Orchestration & Control
