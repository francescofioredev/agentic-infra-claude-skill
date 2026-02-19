# Pattern 08: Memory Management

## Intent
Give agents the ability to persist, retrieve, and reason over information across turns and sessions, extending beyond the limits of the context window.

## Context
Use when the agent needs to remember user preferences, past interactions, domain facts, or intermediate results across multiple turns or sessions. Without explicit memory management, every session starts fresh.

## Forces / Tradeoffs
- **Recency vs. relevance**: Simply including recent history is cheap but irrelevant; semantic retrieval finds relevant memories but adds latency and cost.
- **Privacy**: Persisting user-specific data raises privacy obligations (retention policies, deletion rights).
- **Memory staleness**: Stored facts can become outdated — memory needs invalidation strategies.

## Solution
The Google ADK **Session / State / Memory trichotomy** (p. 148):

| Type | Scope | Storage | Use case |
|------|-------|---------|----------|
| **Session** | Single conversation | In-memory | Conversation context within one session |
| **State** | Cross-turn within session | Session store | Intermediate task state (form filling, multi-step) |
| **Memory** | Cross-session | Persistent DB | User preferences, long-term facts |

**ADK State prefix system** (p. 151):
```python
# In agent output_key or tool:
"user:preference_language"   # Persists across all sessions for this user
"app:global_config"          # Persists across all users for this app
"temp:intermediate_result"   # Discarded after this session
```

**Long-term memory via VertexAiRagMemoryService** (p. 155):
```python
from google.adk.memory import VertexAiRagMemoryService

memory_service = VertexAiRagMemoryService(
    rag_corpus="projects/{project}/locations/{location}/ragCorpora/{corpus_id}"
)
# Agent automatically stores and retrieves from RAG corpus
```

**Key rules:**
1. Explicitly distinguish Session (ephemeral), State (turn-persistent), and Memory (cross-session) — mixing them causes data leakage between users (p. 148).
2. Use `user:` prefix for user-scoped state; `app:` for app-global state; `temp:` for ephemeral (p. 151).
3. Apply memory compression for long sessions: summarize older turns before appending new ones (p. 153).
4. Implement memory TTL (time-to-live) policies for privacy compliance (p. 154).
5. For long-term memory retrieval, use vector similarity search over raw key-value lookup (p. 155).

## Variants
- **In-context memory**: Relevant past content included directly in the context window (simple but limited by window size).
- **External vector store**: Memories stored as embeddings; retrieved by semantic similarity. Used with RAG pattern (Ch 14).
- **Key-value state store**: Simple structured state for form-filling or workflow tracking.
- **VertexAiRagMemoryService**: Managed Google Cloud service for agent long-term memory (p. 155).

## Failure Modes
- **User state bleed**: `app:`-scoped state overwriting `user:`-scoped state (wrong prefix). Mitigation: strict prefix discipline.
- **Stale memory**: Agent acts on outdated information. Mitigation: memory TTL + version tracking.
- **Context window overflow**: Too much history included in context. Mitigation: summarization or selective retrieval.
- **Privacy violation**: Retaining sensitive user data indefinitely. Mitigation: explicit TTL policies, deletion hooks.

## Instrumentation
- Log: memory read/write operations with timestamp and key.
- Track: memory hit rate (relevant memories retrieved / total retrieval attempts).
- Monitor: memory store size growth over time.

## Eval
- Test that `user:` prefixed state does not persist across different users.
- Test that `temp:` prefixed state is discarded after session ends.
- Verify memory retrieval returns relevant past interactions for a test query set.

## Related Patterns
- **RAG** (p. 215): External retrieval of domain knowledge complements in-agent memory.
- **Goal Setting & Monitoring** (p. 183): Goals can be stored in state and updated across turns.
- **Exception Handling** (p. 201): State checkpoints enable rollback to valid prior states.

## Evidence
- p. 148: ADK Session/State/Memory trichotomy with scoping rules.
- p. 151: State prefix system: `user:`, `app:`, `temp:`.
- p. 153: Memory compression / summarization for long sessions.
- p. 155: `VertexAiRagMemoryService` for cross-session long-term memory.
