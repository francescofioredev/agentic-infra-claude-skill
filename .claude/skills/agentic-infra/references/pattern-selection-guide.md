# Pattern Selection Guide

Quick "symptom → pattern" lookup. Load this file when helping choose patterns for a design task.

---

## By Problem Symptom

### "My agent loops forever / doesn't know when to stop"
→ **Goal Setting & Monitoring** (11) — define `goals_met()` + `max_iterations`
→ **Reflection Feedback Loop** (31) — add stopping criteria based on quality score

### "My agent is too expensive / uses too many tokens"
→ **Resource-Aware Optimization** (16) — dynamic model switching
→ **Context Compaction** (22) — compress history before hitting window limit
→ **Reasoning Techniques** (17) — Chain of Draft for compression
→ **Parallelization** (03) — reduce wall-clock time, not tokens
→ **Prompt Chaining** (01) — bounded per-step cost vs. open-ended loop

### "My agent was manipulated by content it retrieved / read from the web"
→ **Plan-Then-Execute Secure** (23) — separate plan (trusted) from execution (untrusted)
→ **Dual LLM** (25) — reasoner never sees raw untrusted content
→ **Guardrails / Safety** (18) — structural separation: XML tags, delimiters

### "My agent called a tool it shouldn't have"
→ **Sandboxed Tool Authorization** (29) — deny-by-default capability tokens
→ **Guardrails / Safety** (18) — tool restrictions per agent
→ **Tool Use** (05) — least-privilege tool assignment

### "My agent keeps making the same mistake / doesn't improve"
→ **Reflection Feedback Loop** (31) — structured critique with history persistence
→ **Reflection** (04) — generator-critic loop
→ **RLAIF** (28) — use AI feedback as training signal
→ **Learning & Adaptation** (09) — behavior update from experience

### "My agent loses context in long sessions / forgets earlier decisions"
→ **Context Compaction** (22) — sliding-window compaction
→ **Memory Management** (08) — session/state/long-term memory tiers
→ **RAG** (14) — retrieve relevant past context on demand

### "My agent doesn't know when to ask a human for help"
→ **Human-in-the-Loop** (13) — explicit escalation triggers in system prompt
→ **Spectrum of Control** (26) — five-level autonomy dial
→ **Goal Setting & Monitoring** (11) — confidence thresholds for escalation

### "Users don't trust my agent / can't understand what it's doing"
→ **Spectrum of Control** (26) — surface current autonomy level
→ **LLM Observability** (30) — structured logs + traces
→ **Evaluation & Monitoring** (19) — measure and report quality metrics

### "My multi-agent system is hard to debug / trace"
→ **LLM Observability** (30) — distributed traces with `trace_id` propagation
→ **Exception Handling & Recovery** (12) — structured error telemetry
→ **Sub-Agent Spawning** (24) — parent-child span relationships

### "My agent's context window is too small for the task"
→ **Context Compaction** (22) — first option; compress and continue
→ **Sub-Agent Spawning** (24) — delegate to isolated agents with fresh context
→ **Resource-Aware Optimization** (16) — switch to a larger context model

### "I need to run multiple independent subtasks faster"
→ **Parallelization** (03) — concurrent independent tasks
→ **Sub-Agent Spawning** (24) — isolated parallel child agents
→ **Multi-Agent Collaboration** (07) — specialized agents in parallel

### "My agent searches the web but returns poor results"
→ **Agentic Search** (27) — multi-step search-evaluate-refine loop
→ **RAG** (14) — for static corpora: pre-indexed vector store
→ **Routing** (02) — choose the right search tool per query type

### "My agent produces inconsistent output quality"
→ **Reflection Feedback Loop** (31) — quality gate before delivery
→ **Evaluation & Monitoring** (19) — LLM-as-Judge rubric
→ **Guardrails / Safety** (18) — output filtering

### "My agent has access to too many tools / could cause damage"
→ **Sandboxed Tool Authorization** (29) — deny-by-default, scoped tokens
→ **Tool Use** (05) — least-privilege assignment
→ **Human-in-the-Loop** (13) — gate irreversible actions

### "I need my agent to improve over time from production data"
→ **RLAIF** (28) — AI feedback as reward signal
→ **Learning & Adaptation** (09) — prompt optimization + fine-tuning loop
→ **Exploration & Discovery** (21) — Elo-based ranking and tripartite review

---

## By Use Case

### Customer Support Agent
Core: Routing (02) · Multi-Agent (07) · Memory (08) · RAG (14) · Guardrails (18)
Add: LLM Observability (30) · Spectrum of Control (26) · Exception Handling (12)

### Coding / SWE Agent
Core: Planning (06) · Tool Use (05) · Reflection Loop (31) · Sub-Agent Spawning (24)
Add: Plan-Then-Execute Secure (23) · Dual LLM (25) · Sandboxed Auth (29) · Context Compaction (22)

### Research / Information Gathering Agent
Core: Agentic Search (27) · RAG (14) · Memory (08) · Parallelization (03)
Add: Context Compaction (22) · Reflection (04) · LLM Observability (30)

### Autonomous Long-Horizon Agent (days-long tasks)
Core: Planning (06) · Sub-Agent Spawning (24) · Memory (08) · Goal Setting (11)
Add: Context Compaction (22) · Exception Handling (12) · HITL (13) · LLM Observability (30) · Spectrum of Control (26)

### Data Processing Pipeline
Core: Prompt Chaining (01) · Parallelization (03) · Tool Use (05)
Add: Resource-Aware Optimization (16) · Exception Handling (12) · Evaluation (19)

### Multi-Tenant SaaS Agent
Core: Guardrails (18) · A2A (15) · Memory (08) · HITL (13)
Add: Sandboxed Auth (29) · LLM Observability (30) · Spectrum of Control (26)

---

## Pattern Quick-Reference Table

| Pattern | # | When to use | Key constraint |
|---------|---|-------------|---------------|
| Prompt Chaining | 01 | Linear sequential tasks | No branching |
| Routing | 02 | Mutually exclusive task types | Classifier must be reliable |
| Parallelization | 03 | Independent concurrent subtasks | Results must be aggregatable |
| Reflection | 04 | Quality-sensitive single output | 2–3 iterations max |
| Tool Use | 05 | Any external API/DB/service | Define schema + least-privilege |
| Planning | 06 | Complex multi-step tasks | Plan must be serializable |
| Multi-Agent | 07 | Specialized parallel workstreams | Needs supervisor/coordinator |
| Memory Management | 08 | Cross-turn/session state | Define prefix scoping |
| Learning & Adaptation | 09 | Continuous improvement loop | Needs feedback signal |
| MCP | 10 | Standardized tool reuse | Server type: STDIO vs HTTP |
| Goal Setting | 11 | Any loop-based agent | SMART goal + `goals_met()` |
| Exception Handling | 12 | Any production agent | Error triad required |
| HITL | 13 | High-stakes / uncertain decisions | Explicit trigger list |
| RAG | 14 | Static knowledge corpus | Hybrid search recommended |
| A2A | 15 | Cross-system agent calls | mTLS + OAuth2 |
| Resource Optimization | 16 | Variable task complexity | Model cost tiers |
| Reasoning Techniques | 17 | Token-expensive reasoning | Chain-of-Draft first |
| Guardrails | 18 | Any user-facing agent | Six-layer defense |
| Eval & Monitoring | 19 | Production deployment | Define metrics before build |
| Prioritization | 20 | Multi-goal agents | Dynamic re-ordering |
| Exploration | 21 | Unknown solution space | Elo-based ranking |
| Context Compaction | 22 | Long-running / large-context | 80% high-water trigger |
| Plan-Then-Execute Secure | 23 | Untrusted env data + actions | Immutable plan hash |
| Sub-Agent Spawning | 24 | Parallel specialized isolation | Max spawn depth limit |
| Dual LLM | 25 | Untrusted data + reasoning | Reasoner never sees raw data |
| Spectrum of Control | 26 | Variable autonomy needs | Hard floor for irreversible |
| Agentic Search | 27 | Complex / multi-source queries | Max iteration budget |
| RLAIF | 28 | Scale feedback for training | Human audit ≥80% alignment |
| Sandboxed Auth | 29 | Any tool-using agent in prod | Deny-by-default always |
| LLM Observability | 30 | Any production deployment | 100% span coverage |
| Reflection Feedback Loop | 31 | Structured quality gate | Max 3 iterations |
