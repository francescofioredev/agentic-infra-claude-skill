# Pattern 05: Tool Use / Function Calling

## Intent
Extend an agent's capabilities beyond language by giving it the ability to invoke external functions, APIs, databases, and services, with the LLM deciding when and how to call each tool.

## Context
Use when the agent needs real-world data (search, database queries), needs to perform actions (send email, write file), or needs computation that LLMs handle poorly (math, code execution). Tool use is the primary mechanism for grounding agents in the real world.

## Forces / Tradeoffs
- **Capability vs. risk**: Tools give agents powerful capabilities but also the ability to cause irreversible side effects (delete data, send messages).
- **LLM decision quality**: The LLM must correctly decide when to call a tool, which tool, and with what parameters — errors here have real-world consequences.
- **Latency**: Each tool call adds a round-trip (LLM → tool → LLM), increasing latency.

## Solution
The function calling pipeline (p. 83):

1. **Tool Definition**: Define tools with name, description, and JSON Schema for parameters.
2. **LLM Decision**: LLM receives the user query + tool definitions → outputs a structured tool call request (not free text).
3. **Function Call Generation**: System extracts tool name and parameters from LLM output.
4. **Tool Execution**: System invokes the actual function with the parameters.
5. **Observation**: Tool result is returned to the LLM as context.
6. **LLM Processing**: LLM incorporates the observation and either calls another tool or returns a final answer.

**Key rules:**
1. Write tool descriptions as if explaining to a smart intern — be explicit about what it does and when to use it vs. similar tools (p. 86).
2. Use JSON Schema to constrain tool parameters — prevents malformed calls (p. 85).
3. Apply the **Principle of Least Privilege**: grant agents only the tools they need for the task (p. 288, Ch 18).
4. Handle tool execution errors gracefully — return the error as an observation so the LLM can adapt (p. 90).
5. For irreversible tools (delete, send), require explicit confirmation before execution (p. 91).

**Tool definition pattern (OpenAI/Anthropic format):**
```python
tools = [{
    "name": "search_database",
    "description": "Search the product database. Use for product info queries. Do NOT use for user account data.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "limit": {"type": "integer", "default": 10}
        },
        "required": ["query"]
    }
}]
```

## Variants
- **Single-turn tool use**: One tool call per conversation turn.
- **Multi-turn (ReAct loop)**: Thought → Action → Observation → Thought → ... until done (p. 265, Ch 17).
- **Parallel tool calls**: Multiple tools called simultaneously in one LLM response (supported by OpenAI, Anthropic APIs).
- **MCP-backed tools**: Tools defined and served via Model Context Protocol (see pattern 10).

## Failure Modes
- **Hallucinated tool calls**: LLM fabricates tool names or parameters that don't exist. Mitigation: validate tool name against defined tool set before executing.
- **Parameter type errors**: LLM passes wrong data types. Mitigation: JSON Schema validation before execution.
- **Infinite tool loop**: Agent keeps calling tools without producing a final answer. Mitigation: max_tool_calls limit.
- **Irreversible action without confirmation**: Agent deletes data without user consent. Mitigation: confirmation gate for destructive tools.
- **Tool injection**: Malicious content in tool results manipulates the agent (p. 289). Mitigation: treat tool outputs as untrusted data.

## Instrumentation
- Log: tool name called, parameters, execution time, result (truncated if large), any errors.
- Track: tool call frequency, error rate per tool, average tool execution time.
- Alert: on tool execution failures > X% of calls.

## Eval
- Test each tool's integration independently (unit test the binding).
- Verify LLM selects correct tool for a set of labeled queries.
- Test error handling: inject a tool failure, verify agent recovers gracefully.

## Related Patterns
- **MCP** (p. 155): Standardized protocol for serving tool definitions to agents.
- **Planning** (p. 101): Planners orchestrate sequences of tool calls.
- **Exception Handling** (p. 201): Required for handling tool execution errors.
- **Guardrails** (p. 285): Least-privilege principle applied to tool permissions.

## Evidence
- p. 81-91: Full function calling pipeline: Tool Definition → LLM Decision → Function Call Generation → Tool Execution → Observation → LLM Processing.
- p. 86: "Write tool descriptions as if explaining to a smart intern."
- p. 85: JSON Schema parameter constraints.
- p. 288: Principle of Least Privilege for tool permissions.
- p. 289: Tool result injection risk — treat outputs as untrusted.
