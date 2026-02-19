# Pattern 07: Multi-Agent Collaboration

## Intent
Decompose complex tasks across multiple specialized agents, each with a distinct role and capability set, coordinated by an orchestrator.

## Context
Use when a task is too broad for a single agent (context limits), requires concurrent work by specialists, or benefits from independent verification (one agent checks another). Multi-agent systems solve problems intractable for a single prompt.

## Forces / Tradeoffs
- **Specialization vs. coordination overhead**: Specialized agents produce higher quality per subtask but require communication and state synchronization overhead.
- **Autonomy vs. control**: Fully autonomous agent networks can drift from the original goal; supervisor patterns maintain control at the cost of flexibility.
- **Trust boundaries**: Sub-agents should be treated as untrusted; the orchestrator must validate their outputs (p. 126).

## Solution
Six canonical multi-agent topologies (p. 122-132):

| Topology | When to use |
|----------|------------|
| **Single Agent** | Simple tasks, single capability |
| **Network** | Each agent can call any other (fully decentralized) |
| **Supervisor** | One orchestrator delegates to specialized workers |
| **Supervisor-as-Tool** | Orchestrator exposes sub-agents as callable tools |
| **Hierarchical** | Multi-level supervisors for very complex tasks |
| **Custom** | Task-specific topology |

**ADK LoopAgent + AgentTool pattern** (p. 133):
```python
from google.adk.agents import LoopAgent, LlmAgent
from google.adk.tools.agent_tool import AgentTool

researcher = LlmAgent(name="researcher", ...)
writer = LlmAgent(name="writer", ...)
critic = LlmAgent(name="critic", ...)

# Expose critic as a tool the writer can invoke
writer_with_critic = LlmAgent(
    name="writer",
    tools=[AgentTool(agent=critic)],
)

pipeline = LoopAgent(
    name="pipeline",
    sub_agents=[researcher, writer_with_critic],
    max_iterations=3,
)
```

**Key rules:**
1. Each agent should have a single, well-defined responsibility (Single Responsibility Principle for agents) (p. 124).
2. Define explicit contracts between agents: what input format, what output format (p. 126).
3. Treat sub-agent outputs as potentially untrustworthy — validate before acting on them (p. 126).
4. For supervisor patterns, the supervisor should handle routing decisions, not business logic (p. 127).
5. Avoid deeply nested hierarchies (> 3 levels) — debugging becomes intractable (p. 130).

## Variants
- **Supervisor**: Central orchestrator routes tasks to workers. Recommended for most production use cases (p. 127).
- **Supervisor-as-Tool**: Sub-agents are tools callable by the orchestrator LLM (p. 128).
- **Hierarchical**: Manager → Team Lead → Worker. Used in Google Co-Scientist (6-agent architecture, p. 332).
- **Peer Network**: Agents communicate directly. Used in Agent Laboratory (p. 340), debate frameworks.

## Failure Modes
- **Cascading failure**: One agent's bad output poisons downstream agents. Mitigation: output validation at boundaries.
- **Context explosion**: Passing full agent histories downstream bloats context. Mitigation: summarize or filter before passing.
- **Coordination deadlock**: Agent A waits for Agent B which waits for Agent A. Mitigation: timeout + escalation.
- **Goal drift**: Agents optimize for local objectives, losing sight of the global goal. Mitigation: include original goal in all agent prompts.

## Instrumentation
- Log: agent invocations, inputs/outputs at each boundary, routing decisions.
- Trace: full execution graph (who called whom, in what order).
- Track: per-agent error rates, inter-agent communication latency.

## Eval
- Test each agent independently before testing the full system (unit → integration order).
- Inject a failing sub-agent and verify the orchestrator handles it gracefully.
- Measure end-to-end task completion rate vs. single-agent baseline.

## Related Patterns
- **Routing** (p. 21): Supervisor pattern is an extension of routing across agents.
- **Parallelization** (p. 41): Multi-agent systems often use parallel execution.
- **A2A** (p. 240): Standardized HTTP protocol for inter-agent communication across services.
- **Reflection** (p. 61): Critic agents implement the reflection pattern within multi-agent systems.

## Evidence
- p. 121-132: Six canonical multi-agent topologies with trade-off analysis.
- p. 124: "Each agent should have a single, well-defined responsibility."
- p. 126: "Treat sub-agent outputs as untrusted — validate before acting."
- p. 133: LoopAgent + AgentTool code example.
- p. 332: Google Co-Scientist 6-agent hierarchical architecture (Supervisor, Generation, Reflection, Ranking, Evolution, Proximity, Meta-review).
