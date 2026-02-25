# Agentic Architecture Review Checklist

Use this rubric to review an agentic system design. Each item maps to a pattern card and PDF evidence. Run `scripts/lint_agentic_arch.py` first to get automated findings, then walk this checklist for gaps.

---

## 1. Architecture & Orchestration

### 1.1 Pattern Selection
- [ ] Is the chosen orchestration pattern (chain, routing, parallelization, multi-agent) documented and justified? (p. 7, p. 27, p. 46, p. 127)
- [ ] Are the tradeoffs of the chosen pattern acknowledged (e.g., chain = predictable but no branching)? (p. 7)
- [ ] Is the topology appropriate for the complexity level? (Single agent → chain → routing → multi-agent) (p. 122)
- [ ] For multi-agent systems: is the topology explicitly specified (Supervisor/Network/Hierarchical)? (p. 122-132)

### 1.2 Planning
- [ ] For complex multi-step tasks: is there a planning step before execution? (p. 101)
- [ ] Is the plan represented as a structured object (JSON/Pydantic) with explicit step dependencies? (p. 107)
- [ ] Is there a max_iterations or max_steps limit to prevent infinite loops? (p. 109)
- [ ] Are plan steps validated for feasibility before execution? (p. 111)

### 1.3 Goal Definition
- [ ] Is the task goal expressed as a SMART goal (Specific, Measurable, Achievable, Relevant, Time-bound)? (p. 185)
- [ ] Is there a `goals_met()` termination check with explicit criteria? (p. 188)
- [ ] Is max_iterations set alongside the goal check? (p. 188)

---

## 2. Tool Use & External Integrations

### 2.1 Tool Definitions
- [ ] Are all tools defined with clear names, descriptions, and JSON Schema parameters? (p. 85-86)
- [ ] Do tool descriptions specify when to use vs. when NOT to use the tool? (p. 86)
- [ ] Are irreversible tools (delete, send, write) explicitly flagged? (p. 91)

### 2.2 Principle of Least Privilege
- [ ] Does each agent only have access to the tools it needs for its specific task? (p. 288)
- [ ] Are read-only agents separate from write/execute agents? (p. 288)
- [ ] Is there documentation of why each tool is assigned to each agent? (p. 288)

### 2.3 MCP / A2A Integrations
- [ ] If using MCP: is the server type specified (STDIO vs. HTTP+SSE)? (p. 160)
- [ ] If using A2A: is an Agent Card defined and published at `/.well-known/agent.json`? (p. 243)
- [ ] Is authentication specified for A2A endpoints (mTLS + OAuth2)? (p. 248)

---

## 3. Memory & State

### 3.1 Memory Scoping
- [ ] Are the three memory types (Session, State, Memory) explicitly distinguished? (p. 148)
- [ ] Is the state prefix system used (`user:`, `app:`, `temp:`)? (p. 151)
- [ ] Is there a risk of user state bleed between sessions? (p. 148)

### 3.2 Long-term Memory
- [ ] For cross-session memory: is a vector store or managed service specified? (p. 155)
- [ ] Are memory TTL policies defined for privacy compliance? (p. 154)
- [ ] Is there a memory staleness risk (facts that could become outdated)? (p. 154)

### 3.3 RAG (if applicable)
- [ ] Are chunking strategy and chunk size documented? (p. 218)
- [ ] Is hybrid search (BM25 + vector) used rather than vector-only? (p. 222)
- [ ] Is there a relevance threshold below which the agent acknowledges knowledge gaps? (p. 225)
- [ ] Are source metadata (document title, page, timestamp) included in chunks for citations? (p. 219)

---

## 4. Safety & Security Boundaries

### 4.1 Guardrails
- [ ] Are all six defense layers addressed (input validation, output filtering, behavioral constraints, tool restrictions, moderation API, HITL)? (p. 286)
- [ ] Is there input validation/sanitization before processing user inputs? (p. 286)
- [ ] Is there output filtering before returning results to users? (p. 286)

### 4.2 Injection & Jailbreak
- [ ] Are tool outputs treated as untrusted (prompt injection risk)? (p. 289)
- [ ] Is there structural separation between instructions and user-controlled data (XML tags, delimiters)? (p. 289)
- [ ] Is there jailbreak detection for the user input path? (p. 296)

### 4.3 Checkpoint & Rollback
- [ ] For multi-step tasks with side effects: are checkpoints defined at major milestones? (p. 290)
- [ ] Is there a rollback procedure documented for when safety checks fail? (p. 290)

### 4.4 Human-in-the-Loop
- [ ] Are escalation triggers explicitly defined in the agent system prompt? (p. 211)
- [ ] Is there a timeout on HITL escalation requests with a safe default? (p. 214)
- [ ] Are all irreversible actions gated behind HITL approval? (p. 213)

---

## 5. Evaluation & Observability

### 5.1 Metrics
- [ ] Are accuracy, latency, and token usage metrics defined before deployment? (p. 303)
- [ ] Is there a baseline (pre-deployment) metric snapshot for comparison? (p. 305)

### 5.2 Evaluation Infrastructure
- [ ] Is there a separate evalset (not used in training) for ongoing regression testing? (p. 312)
- [ ] Is LLM-as-Judge rubric defined with all five dimensions (Clarity, Neutrality, Relevance, Completeness, Audience)? (p. 306)
- [ ] For multi-step agents: is trajectory evaluation implemented (not just final output)? (p. 308)

### 5.3 Monitoring
- [ ] Are all LLM interactions logged with full context (query, response, tool calls, latency, tokens)? (p. 310)
- [ ] Are alerts defined for metric degradation? (p. 305)
- [ ] Is there a safety intervention log? (p. 297)

---

## 6. Failure Modes & Recovery

### 6.1 Error Handling
- [ ] Are errors classified (transient, logic, unrecoverable) with appropriate recovery strategies? (p. 205)
- [ ] Is retry with exponential backoff implemented for transient errors? (p. 206)
- [ ] Are fallback handlers defined? (p. 208)
- [ ] Is max retry count enforced? (p. 206)

### 6.2 Multi-agent Failure Modes
- [ ] Are sub-agent outputs validated before being passed downstream? (p. 126)
- [ ] Is there protection against context explosion (full agent history passed to every sub-agent)? (p. 127)
- [ ] Are coordination deadlocks prevented (timeouts on waiting agents)? (p. 127)

---

## 7. Cost Optimization

- [ ] Is dynamic model switching (Flash/Haiku for simple, Pro/Opus for complex) considered? (p. 257)
- [ ] Is contextual pruning applied to remove irrelevant history before LLM calls? (p. 262)
- [ ] Are frequently repeated queries cached? (p. 264)
- [ ] Is Chain of Draft considered for reasoning-heavy workflows to reduce token count? (p. 272)

---

## 8. Context Window Management

- [ ] Is there a context compaction strategy for long-running or multi-file agents? (Pattern 22)
- [ ] Is a high-water mark token threshold defined (e.g., 80% of model limit triggers compaction)? (Pattern 22)
- [ ] Are critical elements pinned outside the compaction zone (system prompt, active task, open tool calls)? (Pattern 22)
- [ ] Is the compaction summarizer instructed to preserve: facts, decisions, tool results, open questions? (Pattern 22)

---

## 9. Security — Sandboxed Execution & Injection Defense

- [ ] Are tools executed with deny-by-default authorization (no tool callable unless explicitly granted)? (Pattern 29)
- [ ] Are capability grants scoped to minimum necessary permissions (no wildcard scopes)? (Pattern 29)
- [ ] Are capability tokens time-bounded with an explicit TTL? (Pattern 29)
- [ ] Are secrets injected at runtime via env vars — never included in LLM context? (Pattern 29)
- [ ] Is externally retrieved content treated as untrusted data (never re-prompted directly)? (Pattern 23)
- [ ] If the agent touches untrusted data: is planning separated from execution (Plan-Then-Execute)? (Pattern 23)

---

## 10. UX & Autonomy Control

- [ ] Is the agent's autonomy level explicitly defined (from the 5-level spectrum)? (Pattern 26)
- [ ] Are irreversible actions (delete, send, publish) hard-floored at Level 1 (confirm-all), regardless of global level? (Pattern 26)
- [ ] Is there a human override/stop mechanism callable mid-execution? (Pattern 26)
- [ ] Are users notified of the current autonomy level in the interface? (Pattern 26)

---

## Summary Scoring

| Area | Items | Checked | Score |
|------|-------|---------|-------|
| Architecture & Orchestration | 11 | | /11 |
| Tool Use & Integrations | 9 | | /9 |
| Memory & State | 10 | | /10 |
| Safety & Security | 12 | | /12 |
| Evaluation & Observability | 9 | | /9 |
| Failure Modes & Recovery | 7 | | /7 |
| Cost Optimization | 4 | | /4 |
| Context Window Management | 4 | | /4 |
| Security — Sandboxed & Injection | 6 | | /6 |
| UX & Autonomy Control | 4 | | /4 |
| **Total** | **76** | | **/76** |

**Interpretation:**
- 68-76: Production-ready
- 55-67: Significant gaps — address before deployment
- <55: Major architectural concerns — redesign recommended
