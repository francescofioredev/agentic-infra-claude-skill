# Pattern 27: Agentic Search Over Tools

**Source**: awesome-agentic-patterns — Tool Use & Environment

## Intent
Replace a single monolithic retrieval call with an iterative, multi-step search process where the agent formulates queries, evaluates results, refines search strategy, and decides when it has gathered sufficient information — all without relying on a vector store.

## Context
Use when: (1) the information need is complex and cannot be satisfied by a single keyword or semantic query, (2) the agent must search across heterogeneous sources (web, code repos, APIs, databases), or (3) the corpus changes frequently making pre-built vector indices stale. Agentic search is especially powerful for research tasks, debugging, and open-ended information gathering.

## Forces / Tradeoffs
- **Thoroughness vs. cost**: Each search iteration costs LLM tokens and API calls. Unbounded search loops are expensive.
- **Query reformulation**: The agent may reformulate queries suboptimally (e.g., using only one perspective). Mitigation: instruct the agent to try multiple query angles.
- **Source heterogeneity**: Coordinating results from different sources (structured DB, unstructured web) requires normalization.
- **Stopping criterion**: The agent must know when it has "enough" information — a hard problem without ground truth.

## Solution
Implement a **Search-Evaluate-Refine loop**:
1. **Decompose** the information need into sub-questions.
2. **Search**: For each sub-question, select the most appropriate tool (web search, code search, SQL query, API call) and execute it.
3. **Evaluate**: Assess whether the results answer the sub-question. Classify results as: sufficient / partial / irrelevant.
4. **Refine**: For partial results, reformulate the query (synonyms, broader/narrower scope, different source). For irrelevant results, try a different tool.
5. **Aggregate**: Merge results across sub-questions into a coherent response.
6. **Stop** when all sub-questions are sufficiently answered OR when a budget (max iterations, max cost) is exhausted.

**Key rules:**
1. Always decompose before searching — avoids returning on first match of a complex query.
2. Maintain a **search log** (query, source, result quality score) to avoid repeating failed queries.
3. Explicitly instruct the agent to prefer authoritative sources and note source credibility.
4. Budget: set `max_search_steps = 3 × num_sub_questions` as a reasonable upper bound.

**Pseudo-implementation:**
```python
sub_questions = decompose(user_query)
search_log = {}
answers = {}

for q in sub_questions:
    for attempt in range(max_attempts_per_q):
        query = formulate_query(q, search_log.get(q, []))
        tool = select_tool(q, available_tools)
        results = tool.search(query)
        quality = evaluate(q, results)
        search_log.setdefault(q, []).append((query, quality))
        if quality == "sufficient":
            answers[q] = results
            break
        # else: refine query on next iteration

return synthesize(answers)
```

## Variants
- **Parallel sub-question search**: Search all sub-questions concurrently (see Pattern 03 Parallelization) then aggregate.
- **Adaptive source selection**: Use a router (Pattern 02 Routing) to pick the optimal search tool per sub-question type.
- **Citation tracking**: For each answer chunk, record the exact source and passage — critical for research/fact-checking tasks.
- **Incremental answer building**: Build a partial answer after each sub-question, rather than waiting for all to complete.

## Failure Modes
- **Search loop**: Agent keeps refining queries without converging. Mitigation: hard max iteration cap; return best-effort answer when budget exhausted.
- **Source pollution**: Low-quality sources dominate results. Mitigation: source allow-list or credibility scoring.
- **Query drift**: Reformulated queries diverge from original intent. Mitigation: always include original user question in reformulation prompt.
- **Redundant searches**: Agent searches same content via different queries. Mitigation: deduplication in search log; check log before issuing new query.

## Instrumentation
- Track: `search_steps_per_query`, `queries_per_sub_question`, `tool_hit_rate_by_source`.
- Alert: if `search_steps_per_query` exceeds 2× expected (signals poor query formulation or difficult information need).
- Log: all queries, sources, and quality assessments for debugging and quality improvement.

## Related Patterns
- **Tool Use / Function Calling** (Pattern 05): Search tools are just specialized tools in the tool-use framework.
- **RAG** (Pattern 14): RAG uses a pre-built index; Agentic Search is dynamic and multi-step. Complementary.
- **Routing** (Pattern 02): Select the appropriate search tool per query type.
- **Memory Management** (Pattern 08): Cache search results to avoid redundant API calls across sessions.
- **Context Compaction** (Pattern 22): Agentic search results can fill context quickly; compact retrieved content.

## References
Source: awesome-agentic-patterns — Tool Use & Environment
