# Pattern 10: Model Context Protocol (MCP)

## Intent
Standardize how agents discover, connect to, and invoke external tools and data sources using a client-server protocol, replacing ad-hoc tool integration with a reusable, composable standard.

## Context
Use when building agents that need to integrate with multiple external tools/services, when tool definitions should be reusable across different agents, or when you want to expose internal services as tools consumable by any MCP-compatible agent.

## Forces / Tradeoffs
- **Standardization vs. flexibility**: MCP enforces a protocol contract; non-standard tool behaviors may be difficult to express.
- **Added infrastructure**: MCP requires running a server process alongside the agent — adds operational overhead.
- **Security**: MCP server exposes capabilities; must be carefully access-controlled.

## Solution
MCP uses a **client-server architecture** (p. 158):

**Three primitive types** exposed by MCP servers (p. 159):
- **Resources**: Data/content the agent can read (files, database records, web pages)
- **Tools**: Functions the agent can invoke (APIs, computations)
- **Prompts**: Pre-built prompt templates the agent can use

**Transport options** (p. 160):
- **STDIO / JSON-RPC**: Local process communication (for local tools)
- **HTTP + SSE**: Remote server communication (for cloud-hosted tools)

**ADK MCPToolset integration** (p. 161):
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=["./my_mcp_server.py"],
    )
)

agent = LlmAgent(
    name="tool_agent",
    tools=[toolset],  # Agent gets all tools from MCP server
)
```

**FastMCP server definition** (p. 162):
```python
from fastmcp import FastMCP

mcp_server = FastMCP("My Tools")

@mcp_server.tool()
def search_products(query: str, limit: int = 10) -> list[dict]:
    """Search the product catalog. Returns list of matching products."""
    return db.search(query, limit=limit)

if __name__ == "__main__":
    mcp_server.run()
```

**Key rules:**
1. Tool descriptions in MCP servers must be self-contained — the consuming agent has no other context about the tool (p. 162).
2. Use STDIO transport for local development; use HTTP+SSE for production remote services (p. 160).
3. MCP servers should be stateless where possible — enables horizontal scaling (p. 163).
4. Secure MCP servers with authentication even in internal deployments — treat as API surfaces (p. 163).
5. **MCP vs. A2A**: MCP connects agents to tools/data; A2A connects agents to other agents (p. 165).

## Variants
- **Local STDIO server**: Single process, useful for development and local tools.
- **Remote HTTP server**: Deployed as a service, shared across multiple agents.
- **FastMCP**: Python framework for rapid MCP server development with `@mcp_server.tool()` decorator.

## Failure Modes
- **Server unavailability**: MCP server crashes → agent loses all tools from that server. Mitigation: health checks, fallback tools.
- **Protocol version mismatch**: Client and server MCP versions incompatible. Mitigation: version negotiation at startup.
- **Tool description drift**: Server updates tool behavior but not description — LLM uses wrong tool parameters. Mitigation: version tool descriptions.

## Instrumentation
- Log: MCP tool invocations, server response times, protocol errors.
- Health-check MCP servers on a schedule.
- Track: tool-level usage frequency and error rates.

## Eval
- Test each MCP tool independently through the protocol (not just by calling the underlying function directly).
- Verify the agent correctly discovers available tools from the server.
- Test reconnection behavior when the MCP server restarts.

## Related Patterns
- **Tool Use** (p. 81): MCP is the standardized delivery mechanism for tools; Tool Use is the consumption pattern.
- **A2A** (p. 240): Complementary standard — MCP for tools/data, A2A for agent-to-agent.
- **Multi-Agent Collaboration** (p. 121): MCP servers can expose sub-agents as callable tools.

## Evidence
- p. 155-165: MCP chapter. Client-server architecture, three primitive types (Resources/Tools/Prompts).
- p. 158: "MCP standardizes how agents connect to external tools — replacing ad-hoc integrations."
- p. 160: Transport options: JSON-RPC/STDIO vs. SSE/HTTP.
- p. 161: ADK `MCPToolset` + `StdioServerParameters` code.
- p. 162: `@mcp_server.tool()` FastMCP decorator.
- p. 165: MCP vs. A2A distinction.
