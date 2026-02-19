# Pattern 15: A2A Inter-Agent Communication

## Intent
Enable agents built by different teams, in different languages, on different frameworks, to discover and communicate with each other through a standardized open HTTP protocol.

## Context
Use when building multi-agent systems where agents are deployed as independent services (not colocated in a single process), when agents need to be discoverable by external systems, or when you need to compose agents from different vendors or teams.

## Forces / Tradeoffs
- **Interoperability vs. simplicity**: A2A provides framework-agnostic communication but adds HTTP/JSON overhead vs. direct function calls.
- **Service mesh complexity**: A2A over HTTP requires service discovery, authentication, and network infrastructure.
- **Asynchrony**: Long-running tasks require async polling or webhooks rather than synchronous responses.

## Solution
The **Agent Card** (p. 243) — JSON descriptor that every A2A agent publishes at `/.well-known/agent.json`:
```json
{
  "name": "ResearchAgent",
  "description": "Performs web research and returns structured summaries",
  "version": "1.0",
  "capabilities": ["web_search", "summarization"],
  "endpoints": {
    "tasks": "https://api.myagent.com/a2a/tasks"
  },
  "authentication": {
    "scheme": "oauth2",
    "authorization_url": "https://auth.myagent.com/oauth2/token"
  }
}
```

**Task states** (p. 245): `submitted` → `working` → `completed` (or `failed`).

**Four interaction modes** (p. 246):

| Mode | When to use |
|------|------------|
| **Synchronous** | Fast tasks (<30s); caller blocks until complete |
| **Async Polling** | Long tasks; caller polls `GET /tasks/{id}` periodically |
| **Streaming (SSE)** | Progressive output (e.g., token-by-token generation) |
| **Webhooks** | Push notification when task completes |

**Security** (p. 248): mTLS (mutual TLS) for transport-layer authentication + OAuth2 bearer tokens for agent-level authorization.

**A2A vs. MCP distinction** (p. 165, 248):
- **MCP**: Agent ↔ Tool (client calls tool server)
- **A2A**: Agent ↔ Agent (peer-to-peer, both are agents)

**Key rules:**
1. Every A2A agent must publish an Agent Card at `/.well-known/agent.json` — this is the discovery mechanism (p. 243).
2. Task IDs must be globally unique (UUID) — enables polling and deduplication (p. 245).
3. Use mTLS + OAuth2 for production A2A deployments — unauthenticated A2A is a security risk (p. 248).
4. Implement idempotent task submission — network retries must not cause duplicate task execution (p. 246).
5. Design Agent Cards to be version-stamped so callers can handle capability evolution gracefully.

## Variants
- **Synchronous (request-response)**: For short tasks where blocking is acceptable.
- **Async polling**: For long-running research, generation, or computation tasks.
- **SSE streaming**: For progressive results (e.g., streaming LLM output to caller).
- **Webhook callback**: Caller provides a callback URL; agent calls it on completion.

## Failure Modes
- **Agent Card staleness**: Published capabilities don't match actual implementation. Mitigation: version Agent Cards; validate capabilities at runtime.
- **Orphaned tasks**: Caller disconnects; task continues but result is never consumed. Mitigation: TTL on task results + cleanup job.
- **Authentication failure**: mTLS cert expired or OAuth2 token rejected. Mitigation: certificate rotation automation; token refresh logic.
- **Polling overload**: Too many callers polling too frequently. Mitigation: webhook callbacks + exponential backoff on polling.

## Instrumentation
- Log: task ID, caller identity, task submitted/started/completed timestamps, final status.
- Track: task latency distribution, failure rate per agent endpoint.
- Monitor: Task queue depth (pending tasks) as a leading indicator of capacity issues.

## Eval
- Test Agent Card is valid JSON and served at `/.well-known/agent.json`.
- Test all four interaction modes (sync, async poll, SSE, webhook).
- Test authentication rejection for unauthenticated requests.
- Inject a network partition and verify callers handle task status polling gracefully.

## Related Patterns
- **MCP** (p. 155): Complementary — MCP for tools, A2A for agents.
- **Multi-Agent Collaboration** (p. 121): A2A is the communication substrate for distributed multi-agent systems.
- **Exception Handling** (p. 201): A2A task failures must be propagated to calling agents.

## Evidence
- p. 240-250: A2A chapter. Google's open HTTP standard for inter-agent communication.
- p. 243: Agent Card JSON structure and discovery via `/.well-known/agent.json`.
- p. 245: Task states: submitted → working → completed/failed.
- p. 246: Four interaction modes: Synchronous, Async Polling, Streaming (SSE), Webhooks.
- p. 248: Security: mTLS + OAuth2.
- p. 165: A2A vs. MCP distinction.
