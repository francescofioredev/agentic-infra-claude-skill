# Pattern 30: LLM Observability

**Source**: awesome-agentic-patterns — Reliability & Eval

## Intent
Instrument every LLM call and agent action with structured telemetry — traces, metrics, logs — so that system behavior can be understood, debugged, and optimized in production, with the same rigor as traditional software observability.

## Context
Use whenever deploying LLM-based agents in production. Without observability, you cannot answer: "Why did the agent behave unexpectedly?", "Where is token cost coming from?", "Which tools are most frequently failing?", "What is the p99 latency for this agent?". LLM applications have unique observability challenges: non-determinism, long context windows, multi-step traces across agents.

## Forces / Tradeoffs
- **Completeness vs. cost**: Logging full prompts and responses provides maximum debuggability but is expensive in storage and has PII risks. Mitigation: log metadata + truncated content by default; full content to secure store on error or sampling.
- **Latency overhead**: Synchronous telemetry emission in the call path adds latency. Mitigation: async/fire-and-forget telemetry clients.
- **Privacy**: Prompts and responses may contain sensitive user data. Mitigation: PII detection and redaction before logging.
- **Alert noise**: LLMs have high natural output variance — naive alerting on output content causes noise. Mitigation: alert on metrics (latency, cost, error rate) not on content.

## Solution
Implement a **four-signal observability stack**:

**Signal 1 — Distributed Traces:**
- Every agent execution creates a trace. Each LLM call, tool call, and sub-agent spawn is a span.
- Spans include: `model_id`, `input_tokens`, `output_tokens`, `latency_ms`, `finish_reason`.
- Parent-child relationships link orchestrator to sub-agents (see Pattern 24 Sub-Agent Spawning).
- Use OpenTelemetry as the standard instrumentation layer.

**Signal 2 — Metrics:**
- `llm.tokens.input` / `llm.tokens.output` (by model, task type)
- `llm.latency.ms` (p50, p95, p99 by model)
- `llm.cost.usd` (derived from token counts × model pricing)
- `agent.tool_call.success_rate` (by tool name)
- `agent.task.completion_rate` / `agent.task.failure_rate`

**Signal 3 — Structured Logs:**
- Log at key agent lifecycle events: task start, plan produced, tool called, reflection iteration, task complete/failed.
- Always include: `trace_id`, `agent_id`, `task_id`, `timestamp`.
- Log LLM call metadata (never raw prompt in default log level; raw prompt in DEBUG only).

**Signal 4 — Eval Metrics (online):**
- Sample N% of completions; run a lightweight LLM-as-Judge evaluation inline.
- Track: helpfulness score, factuality score, safety violations over time.

**Key rules:**
1. Every LLM call must be wrapped in a span — no un-instrumented calls in production.
2. Propagate `trace_id` across all agent boundaries (including sub-agents, A2A calls).
3. Always log `finish_reason` (stop / length / tool_call / content_filter) — it's the first signal for many bugs.
4. Cost budget alerts: fire when cumulative task cost exceeds the expected budget threshold.

**Pseudo-implementation:**
```python
with tracer.start_span("llm_call", attributes={"model": model_id}) as span:
    start = time.time()
    response = llm.call(messages)
    latency = time.time() - start
    span.set_attributes({
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "finish_reason": response.finish_reason,
        "latency_ms": latency * 1000,
        "cost_usd": compute_cost(response.usage, model_id),
    })
    metrics.record("llm.tokens.input", response.usage.input_tokens, tags={"model": model_id})
    metrics.record("llm.latency.ms", latency * 1000)
return response
```

## Variants
- **Sampling-based logging**: Log 100% of metadata, 10% of full prompt/response content.
- **Error-triggered full logging**: Log full content only when `finish_reason=error` or task fails.
- **Replay debugger**: Store sanitized traces that can be replayed in a dev environment for debugging.
- **Cost attribution**: Tag traces with `user_id`, `feature`, `tenant` for per-customer cost accounting.

## Failure Modes
- **Context leakage in logs**: Full prompts logged to a shared log aggregator accessible to unauthorized parties. Mitigation: PII redaction pipeline; access-controlled log store for sensitive content.
- **Trace explosion**: Deeply nested sub-agent trees generate thousands of spans per task. Mitigation: span sampling for high-volume sub-tasks; alert on trace depth exceeding N.
- **Missing trace propagation**: Sub-agent spawned without inheriting parent `trace_id` → orphaned spans. Mitigation: mandatory `trace_id` in every agent initialization interface.
- **Metric drift**: Model price changes make `cost_usd` calculation stale. Mitigation: externalize model pricing configuration; alert on pricing config age > 30 days.

## Instrumentation
(This pattern is itself about instrumentation. The meta-level instrumentation is:)
- Track: `instrumentation_coverage` (% of LLM calls with spans) — target 100%.
- Alert: if any LLM call detected without a span (via static analysis or runtime monitoring).
- Audit: monthly review of sampled traces for quality and completeness.

## Related Patterns
- **Evaluation & Monitoring** (Pattern 19): LLM-as-a-Judge eval; LLM Observability provides the data pipeline for it.
- **Goal Setting & Monitoring** (Pattern 11): Goal progress tracked via observability metrics.
- **Exception Handling & Recovery** (Pattern 12): Error detection relies on observability signals.
- **Sub-Agent Spawning** (Pattern 24): Distributed tracing across spawned agents requires trace propagation.
- **Resource-Aware Optimization** (Pattern 16): Cost metrics from observability drive optimization decisions.

## References
Source: awesome-agentic-patterns — Reliability & Eval
