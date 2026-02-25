# Pattern 29: Sandboxed Tool Authorization

**Source**: awesome-agentic-patterns — Security & Safety

## Intent
Apply a **deny-by-default** authorization policy to all agent tool calls, where each tool invocation requires an explicit grant based on the minimum necessary scope, and all tool execution occurs in an isolated environment that cannot affect the host system.

## Context
Use whenever an agent can call external APIs, execute code, read/write files, or interact with databases — especially in multi-tenant systems, production environments, or when handling untrusted inputs. The principle: agents should not be trusted to self-limit; the infrastructure must enforce limits.

## Forces / Tradeoffs
- **Capability vs. security**: Tight sandboxing reduces what the agent can do. Balance by granting only the permissions actually needed per task.
- **Latency**: Authorization checks and sandbox setup add overhead per tool call. Batch authorization for sequential calls to the same tool to reduce overhead.
- **Developer experience**: Over-restrictive defaults block legitimate use cases. Provide clear error messages and an escalation path for legitimate permission requests.
- **Secret management**: Sandboxed agents must be able to access credentials without those credentials leaking to the agent's context.

## Solution
Implement a **four-layer sandboxed authorization model**:

**Layer 1 — Tool Registry (static):**
- Define all available tools in a registry with: name, scope categories, required permissions, risk level (read-only / write / destructive).
- Agents cannot call unregistered tools.

**Layer 2 — Permission Grant (per task):**
- At task start, the orchestrator derives the minimal tool permission set needed for the task.
- Issue a **scoped capability token** (e.g., JWT with tool whitelist + time-limited TTL).
- Agent presents the token with every tool call; the tool executor validates it.

**Layer 3 — Execution Sandbox:**
- Run tool code in an isolated environment: container, subprocess with restricted filesystem, or serverless function.
- No network access by default; allowlist specific endpoints.
- No persistent filesystem access by default; provide a scoped temp directory.

**Layer 4 — Audit Log:**
- Log every tool call: timestamp, agent ID, tool name, arguments (sanitized), result status.
- Store logs append-only; alert on any authorization failure.

**Key rules:**
1. **Deny-by-default**: all tool calls rejected unless explicitly granted.
2. **Least privilege**: grant only the specific tool + scope needed (e.g., `read:database:customers_table`, not `read:database:*`).
3. **Time-bounded**: all grants have an explicit TTL; no permanent grants for ephemeral agents.
4. **No secrets in context**: inject secrets via environment variables at execution time; never include API keys in the agent's conversation context.

**Pseudo-implementation:**
```python
# Task setup
task_permissions = derive_permissions(task_description)
token = issue_capability_token(
    agent_id=agent.id,
    tools=task_permissions.tools,
    scopes=task_permissions.scopes,
    ttl=task_permissions.estimated_duration
)

# Tool call (in agent)
result = tool_executor.call(
    tool="database_query",
    args={"table": "customers", "query": query},
    token=token  # validated by executor
)

# Tool executor
def call(tool, args, token):
    assert token.is_valid(), "Token expired or invalid"
    assert tool in token.allowed_tools, f"Tool {tool} not authorized"
    assert check_scope(tool, args, token.scopes), "Scope violation"
    return run_in_sandbox(tool, args)
```

## Variants
- **Hardware sandbox**: Run tool code in a VM or hardware-isolated environment for maximum isolation (e.g., code execution agents).
- **Time-of-use authorization**: Require fresh authorization for each tool call to a high-risk tool (vs. session-level token).
- **Capability-based security**: Each tool call consumes a one-time-use capability object, preventing replay.
- **Policy-as-code**: Express tool authorization rules in a declarative policy language (e.g., OPA/Rego) for auditability and team review.

## Failure Modes
- **Over-broad scopes**: Convenience leads to granting `*` scopes. Mitigation: code review policy requiring justification for any wildcard scope.
- **Token leakage**: Capability token leaked to agent context → agent could forge calls. Mitigation: tokens must never appear in LLM context; use opaque references.
- **Sandbox escape**: Sandbox isolation bug allows tool code to affect host. Mitigation: defense-in-depth (multiple isolation layers); assume sandbox can be escaped.
- **Authorization bypass via injection**: Agent manipulates tool arguments to exceed scope (e.g., SQL injection into a "read-only" query). Mitigation: parameterized queries; argument schema validation.

## Instrumentation
- Track: `tool_call_authorization_failure_rate`, `calls_per_tool_per_task`, `sandbox_breach_attempts`.
- Alert: any authorization failure (potential misconfiguration or attack).
- Alert: any tool call with arguments outside the declared schema.
- Log: full audit trail of all tool calls (immutable append-only store).

## Related Patterns
- **Guardrails / Safety** (Pattern 18): Guardrails operate at LLM output level; Sandboxed Authorization operates at execution level. Complementary layers.
- **Tool Use** (Pattern 05): Tool use framework; this pattern adds the security wrapper around it.
- **Plan-Then-Execute Secure** (Pattern 23): Authorization is enforced at execution phase.
- **Dual LLM** (Pattern 25): Constrained executor benefits from sandboxed authorization on its tools.
- **A2A Communication** (Pattern 15): mTLS and OAuth2 for inter-agent calls; sandboxed authorization for intra-agent tool calls.

## References
Source: awesome-agentic-patterns — Security & Safety
