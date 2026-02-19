# Pattern 03: Parallelization

## Intent
Execute multiple independent LLM calls (or subtasks) concurrently to reduce total latency and enable aggregation of diverse outputs.

## Context
Use when a task can be split into independent subtasks with no data dependencies between them, and the final output requires combining their results. Common uses: parallel research, multi-perspective evaluation, simultaneous content generation.

## Forces / Tradeoffs
- **Latency vs. cost**: Parallel execution reduces wall-clock time but does not reduce total token cost (may even increase it due to overhead).
- **Independence requirement**: Tasks must be truly independent; hidden dependencies cause race conditions or inconsistent combined outputs.
- **Aggregation complexity**: Combining N diverse outputs adds logic that must handle missing or conflicting results.

## Solution
Split the task into N independent subtasks. Execute them concurrently. Aggregate results in a final step.

**LangChain `RunnableParallel` pattern** (p. 45):
```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    summary=summarize_chain,
    sentiment=sentiment_chain,
    keywords=keywords_chain,
)
result = parallel_chain.invoke({"text": document})
# result = {"summary": ..., "sentiment": ..., "keywords": ...}
```

**LangGraph parallel nodes** (p. 48):
```python
# All three branches from START node run concurrently
parallel_builder.add_edge(START, "call_llm_1")
parallel_builder.add_edge(START, "call_llm_2")
parallel_builder.add_edge(START, "call_llm_3")
parallel_builder.add_edge("call_llm_1", "aggregator")
parallel_builder.add_edge("call_llm_2", "aggregator")
parallel_builder.add_edge("call_llm_3", "aggregator")
```

**Google ADK `ParallelAgent`** (p. 50):
```python
parallel_agent = ParallelAgent(
    name="parallel_researcher",
    sub_agents=[research_agent_1, research_agent_2, research_agent_3],
)
```

**Key rules:**
1. Verify task independence before parallelizing — shared mutable state causes undefined behavior (p. 46).
2. Design the aggregator step to be robust to partial failures (p. 47).
3. Use parallelization to implement "sectioning" — different agents check different parts of a document simultaneously (p. 48).
4. Use parallelization to implement "voting" — multiple agents produce answers, majority vote wins (p. 48).

## Variants
- **Sectioning**: Each worker processes a different slice of the input (e.g., different document sections).
- **Voting / Ensemble**: All workers process the same input with different prompts; results are aggregated by majority vote or scoring. Reduces hallucination risk.
- **Map-Reduce**: Map phase fans out to N workers; reduce phase aggregates.

## Failure Modes
- **Partial failure**: One of N parallel calls fails — aggregator must handle gracefully.
- **False independence**: Hidden dependency between tasks causes incorrect combined output.
- **Aggregation logic failure**: Aggregator cannot reconcile conflicting outputs from workers.

## Instrumentation
- Log: parallel task IDs, individual task latencies, aggregation strategy used.
- Track: partial failure rate per worker.
- Alert: if any worker consistently fails (>X% of runs).

## Eval
- Compare parallel output against sequential baseline for equivalence.
- Inject a failing worker and verify the aggregator degrades gracefully.
- Measure latency reduction vs. sequential (should approach max(individual latencies)).

## Related Patterns
- **Routing** (p. 21): Router dispatches to one path; parallelization runs multiple paths simultaneously.
- **Multi-Agent Collaboration** (p. 121): Parallelization is the execution model used within multi-agent systems.
- **Reflection** (p. 61): Multiple parallel critique passes can be aggregated for richer feedback.

## Evidence
- p. 41-50: "Parallelization allows independent subtasks to run concurrently, reducing total latency."
- p. 45: `RunnableParallel` example.
- p. 48: "Sectioning and voting are two primary use cases for parallelization."
- p. 50: ADK `ParallelAgent` and `SequentialAgent` built-in types.
