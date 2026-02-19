# Design Example: Customer Support Agent

This example demonstrates the **design workflow** using the agentic-infra skill to design a customer support agent for an e-commerce platform.

---

## Step 1: Identify Concerns (taxonomy.yaml)

For a customer support agent, the relevant concerns are:

```yaml
# From taxonomy.yaml
reliability:   exception-handling-recovery, hitl, guardrails-safety
safety:        guardrails-safety, hitl, tool-use (least-privilege)
memory:        memory-management, rag (product knowledge base)
tool-use:      tool-use, mcp
orchestration: routing, multi-agent-collaboration (supervisor)
observability: evaluation-monitoring, goal-setting-monitoring
eval:          evaluation-monitoring
cost:          resource-aware-optimization
```

---

## Step 2: Pattern Selection

Based on the concerns, we select the following patterns:

| Concern | Pattern(s) | Rationale |
|---------|-----------|-----------|
| Orchestration | **Routing** (Ch 2) + **Supervisor multi-agent** (Ch 7) | Customer queries fall into distinct categories (billing, tech support, returns) — routing selects the right specialist agent |
| Memory | **Memory Management** (Ch 8) + **RAG** (Ch 14) | Session memory for conversation context; RAG for product knowledge base |
| Tool use | **Tool Use** (Ch 5) + **MCP** (Ch 10) | CRM lookup, order status, knowledge base search via MCP server |
| Safety | **Guardrails** (Ch 18) | Six-layer defense for user-facing system |
| Reliability | **Exception Handling** (Ch 12) + **HITL** (Ch 13) | Tool failures + human escalation for complex cases |
| Eval | **Evaluation & Monitoring** (Ch 19) | LLM-as-Judge + trajectory evaluation |
| Cost | **Resource-Aware Optimization** (Ch 16) | Route simple FAQ queries to Flash; complex complaints to Pro |

---

## Step 3: Architecture Design

### System Topology
```
User
  └─→ Input Validator (Guardrail Layer 1)
        └─→ Router Agent (pattern 02)
              ├─→ Billing Specialist Agent
              ├─→ Technical Support Agent
              ├─→ Returns/Refunds Agent
              └─→ General FAQ Agent (uses RAG)
                                         ↕
                                   MCP Server (tools)
                                   ├─→ CRM Tool
                                   ├─→ Order Status Tool
                                   └─→ Knowledge Base Search
```

This is a **Supervisor topology** (p. 127) where the Router Agent acts as the supervisor, dispatching to specialist workers.

### Pattern Applications

#### Routing (p. 21-40)
```python
from langchain_core.runnables import RunnableBranch

support_router = RunnableBranch(
    (lambda x: classify(x["query"]) == "billing", billing_agent),
    (lambda x: classify(x["query"]) == "technical", tech_agent),
    (lambda x: classify(x["query"]) == "returns", returns_agent),
    faq_agent,  # default fallback (p. 27)
)
```
Evidence: p. 25 — `RunnableBranch` always requires a default fallback.

#### Memory Management (p. 148-155)
```python
# Session state (conversation context within one session)
state["temp:current_intent"] = classified_intent      # ephemeral
state["user:preferred_language"] = "en"               # user-scoped (p. 151)
state["app:faq_cache"] = cached_faq_responses         # app-scoped
```
Evidence: p. 151 — State prefix system prevents user data leakage between sessions.

#### RAG for Knowledge Base (p. 217-227)
- Chunking: paragraph-level with 50-token overlap (p. 218)
- Search: hybrid BM25 + vector (p. 222)
- Relevance threshold: 0.7 — below this, agent acknowledges knowledge gap (p. 225)
- Source metadata: product ID, last updated date included per chunk (p. 219)

#### Guardrails (p. 285-298)
All six layers implemented:
1. Input validation: PII detection, prompt injection check (p. 286)
2. Output filtering: PII redaction before returning to user (p. 286)
3. Behavioral constraints: system prompt forbids giving financial/legal advice (p. 286)
4. Tool restrictions: Least Privilege — each agent only gets its required tools (p. 288)
5. Moderation API: content safety check on all outputs (p. 286)
6. HITL: escalation for account disputes >$500, legal threats (p. 213)

#### Resource-Aware Optimization (p. 257-262)
```
Simple FAQ / status check → Gemini Flash (fast, cheap)
Complex complaint / refund dispute → Gemini Pro
Legal/regulatory question → Gemini Ultra + HITL
```
Router uses Flash for the routing decision itself (p. 258 — "use cheap model for routing decision").

---

## Step 4: ADR (abbreviated)

See `templates/adr.md` for the full ADR template. Key decisions:

| Decision | Rationale | Evidence |
|----------|-----------|---------|
| Supervisor topology | Most controlled for multi-category support | p. 127 |
| Hybrid RAG search | Significantly better recall than vector-only | p. 222 |
| `user:` prefix for preferences | Prevents cross-session bleed | p. 151 |
| Flash for routing | Routing decision doesn't need expensive model | p. 258 |
| `before_tool_callback` | Validates user_id before CRM access | p. 295 |

---

## Step 5: Self-Check Against Review Checklist

Running the checklist (checklists/review.md):

| Area | Score |
|------|-------|
| Architecture & Orchestration | 10/11 *(open: plan depth documentation)* |
| Tool Use & Integrations | 9/9 |
| Memory & State | 9/10 *(open: RAG TTL policy for product catalog)* |
| Safety & Security | 12/12 |
| Evaluation & Observability | 8/9 *(open: trajectory eval for billing agent)* |
| Failure Modes & Recovery | 7/7 |
| Cost Optimization | 4/4 |
| **Total** | **59/62** |

**Assessment**: Production-ready (≥55). Two minor items to address in sprint 1.

---

## Lint Check

```bash
python3 scripts/lint_agentic_arch.py examples/design-example-adr.md --format text
```

Expected output: 0 CRITICAL, 0 HIGH (all addressed above). Any remaining MEDIUM/LOW findings are documented in the ADR.
