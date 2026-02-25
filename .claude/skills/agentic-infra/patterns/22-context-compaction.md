# Pattern 22: Context Window Auto-Compaction

**Source**: awesome-agentic-patterns — Context & Memory

## Intent
Automatically compress or summarize the accumulated conversation/action history when it approaches the context window limit, preserving essential information while staying within token budgets.

## Context
Use when building long-running agents (coding assistants, research agents, autonomous pipelines) where conversation history grows over many turns. Without compaction the agent either truncates abruptly—losing critical context—or fails with a context-limit error.

## Forces / Tradeoffs
- **Fidelity vs. token budget**: Summarization always loses some detail; aggressive compression risks discarding facts needed later.
- **Latency**: Compaction requires an extra LLM call (summarization step), adding latency at the compaction trigger.
- **Trigger timing**: Too early wastes tokens on compaction overhead; too late causes hard limit errors.
- **Rolling vs. full**: Rolling compaction (compact only the oldest N turns) preserves recent context at higher granularity than full compaction.

## Solution
Implement a **sliding-window compaction** strategy:
1. Set a **high-water mark** (e.g., 80% of model's context window in tokens).
2. When accumulated tokens exceed the mark, invoke a **Summarizer** agent over the oldest portion of history.
3. Replace those turns with the compact summary in the context buffer.
4. Preserve verbatim: the most recent N turns (raw), any pinned/system instructions, and any open tool calls.

**Key rules:**
1. Always pin the system prompt and active task description outside the compaction zone.
2. Summarize with an explicit instruction: "Preserve all facts, decisions, tool results, and open questions."
3. Track a `compaction_count` metric — frequent compaction signals the context window is too small for the task.
4. Implement idempotent compaction: re-running on already-compacted context must not lose further information.

**Pseudo-implementation:**
```python
def maybe_compact(history, model_context_limit, high_water=0.8):
    token_count = count_tokens(history)
    if token_count < model_context_limit * high_water:
        return history
    # Keep last 20 turns verbatim; summarize the rest
    recent = history[-20:]
    old = history[:-20]
    summary = summarizer.invoke(
        f"Summarize preserving all facts, decisions, tool results:\n{format(old)}"
    )
    return [{"role": "system", "content": f"[Compacted context]\n{summary}"}] + recent
```

## Variants
- **Hierarchical compaction**: Multi-level summaries (recent → medium → distant) with progressively more compression.
- **Selective retention**: Use a relevance scorer to keep only context chunks relevant to the current task goal.
- **External memory offload**: Move compacted context to a vector store and retrieve on demand (see Pattern 08 Memory Management and Pattern 14 RAG).
- **Structured summary**: Summarize into typed fields (decisions[], open_questions[], tool_results[]) rather than free text.

## Failure Modes
- **Over-compression**: Summarizer omits a critical tool result or decision → agent revisits resolved issues. Mitigation: use explicit extraction prompts with structured output.
- **Trigger miss**: Token count underestimated → context-limit error mid-turn. Mitigation: use a conservative high-water mark (70-75%) and validate count before every LLM call.
- **Summary hallucination**: Summarizer invents facts not in the original history. Mitigation: instruct summarizer to only use information present in the input; include a faithfulness check.
- **Infinite compaction loop**: Each summary is itself too long. Mitigation: enforce a hard maximum summary length.

## Instrumentation
- Track: `context_tokens_at_turn`, `compaction_triggered_count`, `post_compaction_token_count`.
- Alert: if compaction fires more than once per 10 turns (task too large for context budget).
- Log: full original history before compaction (to an external store) for debugging and auditability.

## Related Patterns
- **Memory Management** (Pattern 08): Long-term memory stores are the complement — off-load to memory, retrieve via RAG.
- **RAG** (Pattern 14): Retrieval-augmented generation as an alternative to keeping everything in context.
- **Resource-Aware Optimization** (Pattern 16): Model switching to larger context windows before triggering compaction.
- **Agentic Search** (Pattern 27): Search tools reduce the need to keep retrieved content in context.

## References
Source: awesome-agentic-patterns — Context & Memory
