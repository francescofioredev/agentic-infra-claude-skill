# Community Patterns: Context & Memory
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns for managing the information an agent can access and retain: short-term context window management, long-term memory across sessions, and dynamic context construction. These patterns address the fundamental constraint that LLMs have bounded working memory.

**17 patterns in this category.** For full detail on key patterns, see:
- Pattern 22: Context Window Auto-Compaction (`patterns/22-context-compaction.md`)
- Pattern 08: Memory Management (`patterns/08-memory-management.md`)
- Pattern 14: RAG (`patterns/14-rag.md`)
- Pattern 27: Agentic Search (`patterns/27-agentic-search.md`)

---

## Patterns

### Context Window Auto-Compaction
**Status**: established
**Problem**: Long-running agents accumulate conversation history that eventually exceeds the model's context window, causing either hard failures or abrupt truncation of critical context.
**Solution**: Detect when token count approaches a high-water mark; invoke a summarizer over the oldest context; replace with a compact summary while preserving recent turns verbatim.
**Tags**: context, compression, long-running, memory
**Reference**: See Pattern 22 (`patterns/22-context-compaction.md`)

### Sliding Window Context
**Status**: established
**Problem**: Keeping only the most recent N turns is simpler than compaction but loses distant context entirely.
**Solution**: Maintain a fixed-size rolling window of the last N turns; discard oldest turns when the window is full. Suitable for stateless tasks where distant history is rarely needed.
**Tags**: context, windowing, simple
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Episodic Memory
**Status**: established
**Problem**: Agent needs to recall specific past interactions or events, not just general knowledge.
**Solution**: Store interaction episodes as structured records (timestamp, entities, outcome) in a database; retrieve relevant episodes by semantic similarity or entity matching at query time.
**Tags**: memory, episodes, long-term, retrieval
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Semantic Memory / Knowledge Graph
**Status**: emerging
**Problem**: Agent needs persistent, structured world knowledge that is too large for the context window and too structured for a flat vector store.
**Solution**: Maintain a knowledge graph (entities + relationships); agent queries the graph for relevant subgraphs and injects them into context as needed.
**Tags**: memory, knowledge-graph, structured, semantic
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Working Memory Buffer
**Status**: established
**Problem**: Agent needs to track intermediate state (partial results, open questions, current plan) across multiple turns without polluting the main conversation history.
**Solution**: Maintain a structured working-memory object (JSON or Markdown) that the agent reads and updates at each turn; this is separate from the conversation history.
**Tags**: memory, state, intermediate, structured
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Memory-Augmented Generation
**Status**: established
**Problem**: Agent responses are inconsistent across sessions because the model has no persistent memory of user preferences or past decisions.
**Solution**: Before each generation, retrieve top-k relevant memories from a memory store; prepend them to the system prompt. After generation, update the memory store with new salient facts.
**Tags**: memory, retrieval, personalization, consistency
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Selective Context Injection
**Status**: established
**Problem**: Full conversation history is too long; injecting all of it wastes tokens and dilutes relevance.
**Solution**: Rank all available context chunks by relevance to the current query; inject only the top-k chunks. Use semantic similarity, recency, and importance scores for ranking.
**Tags**: context, relevance, retrieval, token-efficiency
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Memory Tiering
**Status**: emerging
**Problem**: Different information has different access patterns: some facts are needed every turn; others only occasionally.
**Solution**: Implement three tiers — hot (in-context, always present), warm (retrieved on demand from vector store), cold (archived, retrieved only on explicit query). Automatically promote/demote based on access frequency.
**Tags**: memory, tiering, performance, architecture
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Structured Memory Schema
**Status**: established
**Problem**: Unstructured free-text memory is hard to query reliably; agents often miss relevant memories when searching by semantic similarity alone.
**Solution**: Define a schema for stored memories (entity type, attributes, relationships, confidence score, source); store as structured records; enable precise retrieval by entity/attribute matching.
**Tags**: memory, schema, structured, reliability
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Forgetting Mechanism
**Status**: emerging
**Problem**: Memory stores accumulate stale, incorrect, or low-value memories that degrade retrieval quality over time.
**Solution**: Implement time-based decay and explicit forgetting: reduce confidence scores over time; allow agent to explicitly mark memories as obsolete; periodically prune low-confidence entries.
**Tags**: memory, forgetting, maintenance, staleness
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Conversation Summarization
**Status**: established
**Problem**: Long multi-turn conversations become unwieldy; the agent loses track of early decisions.
**Solution**: Periodically summarize the conversation into a structured summary (key decisions, open questions, agreed facts); replace the raw turns with the summary in the context.
**Tags**: memory, summarization, conversation, context
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Entity Tracking
**Status**: established
**Problem**: Agent loses track of entities (people, companies, tasks) mentioned across many turns.
**Solution**: Maintain an entity registry updated each turn: extract entities mentioned, update their attributes, track relationships. Inject relevant entity slots into context for each turn.
**Tags**: memory, entities, tracking, NER
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Shared Memory Blackboard
**Status**: established
**Problem**: In multi-agent systems, agents need to share state without direct message passing.
**Solution**: Maintain a shared blackboard (structured document or database) that all agents can read and write. Each agent reads relevant fields, processes, and writes results back. Optimistic locking prevents conflicts.
**Tags**: memory, multi-agent, shared-state, blackboard
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Context Pinning
**Status**: established
**Problem**: Critical instructions (system prompt, safety rules, current task goal) get pushed out of the effective context window by growing conversation history.
**Solution**: Define a pinned context section that is always prepended to every LLM call, regardless of conversation length. Pinned context is excluded from compaction.
**Tags**: context, pinning, system-prompt, invariants
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Tool Result Caching
**Status**: established
**Problem**: Agent calls the same tool (e.g., web search, database query) with identical arguments multiple times, wasting API quota and latency.
**Solution**: Cache tool results keyed by (tool_name, args_hash) with a configurable TTL. Return cached result on cache hit; invoke tool on miss.
**Tags**: context, caching, tool-use, efficiency
**Reference**: Source: awesome-agentic-patterns — Context & Memory

### Retrieval-Augmented Context
**Status**: established
**Problem**: Agent needs to reason over a large document corpus that cannot fit in context.
**Solution**: Pre-index documents into a vector store; at query time retrieve top-k relevant chunks and inject into context. See Pattern 14 RAG for full detail.
**Tags**: context, retrieval, RAG, vector-store
**Reference**: See Pattern 14 (`patterns/14-rag.md`)

### Progressive Context Loading
**Status**: emerging
**Problem**: Loading all potentially relevant context upfront wastes tokens; it's unclear what will be needed.
**Solution**: Start with minimal context (system prompt + immediate task); load additional context lazily as the agent's reasoning reveals what information is needed (via explicit retrieval calls).
**Tags**: context, lazy-loading, efficiency, progressive
**Reference**: Source: awesome-agentic-patterns — Context & Memory
