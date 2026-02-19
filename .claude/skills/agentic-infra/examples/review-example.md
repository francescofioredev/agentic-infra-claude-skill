# Review Example: Research Pipeline Agent

This example demonstrates the **review workflow** for an existing agentic research pipeline ADR that has several architectural gaps.

---

## System Under Review

**Name**: Autonomous Research Pipeline
**Description**: Agent that accepts a research question, searches the web, and synthesizes a report.
**ADR excerpt** (hypothetical, for illustration):

```markdown
# ADR-007: Autonomous Research Pipeline

## Decision
We will build a research pipeline using LangChain.
The agent will:
1. Accept user research question
2. Use web_search tool to find relevant sources
3. Loop until enough sources are found
4. Generate a comprehensive report

## Tool Access
The agent has access to: web_search, pdf_reader, wikipedia_api, email_send

## Memory
We'll use conversation history to maintain context.

## Error Handling
Errors will be logged.

## Evaluation
We'll know if it's working by testing it manually.
```

---

## Step 1: Run Lint Script

```bash
python3 scripts/lint_agentic_arch.py adr-007-research-pipeline.md --format json
```

Output:
```json
{
  "file": "adr-007-research-pipeline.md",
  "summary": {
    "critical": 2,
    "high": 3,
    "medium": 2,
    "low": 1,
    "total": 8
  },
  "findings": [
    {
      "id": "LINT-001",
      "severity": "CRITICAL",
      "rule": "max_iterations_required",
      "finding": "ADR describes an agent loop ('loop until enough sources found') but does not define max_iterations",
      "pattern_ref": "patterns/11-goal-setting-monitoring.md",
      "evidence_page": 188,
      "evidence_quote": "Set max_iterations alongside the goal — prevents infinite loops when goals_met() never returns true",
      "required_action": "Add max_iterations parameter; document the value and rationale"
    },
    {
      "id": "LINT-003",
      "severity": "CRITICAL",
      "rule": "least_privilege",
      "finding": "Agent has email_send tool but no justification for granting it — research agent should not have send capability",
      "pattern_ref": "patterns/18-guardrails-safety.md",
      "evidence_page": 288,
      "evidence_quote": "Grant agents only the tools they need for the task",
      "required_action": "Remove email_send from research agent; create separate delivery agent if needed"
    },
    {
      "id": "LINT-005",
      "severity": "CRITICAL",
      "rule": "guardrails_required",
      "finding": "Agent processes user input but no safety guardrails defined",
      "pattern_ref": "patterns/18-guardrails-safety.md",
      "evidence_page": 286,
      "required_action": "Define six-layer guardrail strategy"
    },
    ...
  ]
}
```

---

## Step 2: Walk Review Checklist

### 1. Architecture & Orchestration

**Finding [HIGH]**: No termination criteria defined.
- ADR says "loop until enough sources found" but "enough" is not defined.
- Missing: `goals_met()` check with explicit criteria (e.g., "≥5 sources with relevance score >0.8") (p. 185, p. 188)
- Required action: Define SMART goal: "Find 5-10 high-quality sources relevant to the research question"

**Finding [HIGH]**: No max_iterations limit (also caught by LINT-001).
- Required action: Set `max_iterations=10`, document rationale

### 2. Tool Use & Security

**Finding [CRITICAL]**: Least Privilege violation.
- `email_send` tool is not needed for research — creates risk of agent sending unauthorized emails (p. 288)
- Required action: Remove `email_send`; if report delivery is needed, make it a separate, human-triggered step

**Finding [MEDIUM]**: Web search results are untrusted (prompt injection risk).
- Malicious web page content could manipulate the agent's behavior (p. 289)
- Required action: Filter/sanitize web search results before including in agent context

**Finding [LOW]**: No MCP server specified for tools.
- Not blocking, but consider MCP for tool reusability across agents (p. 158)

### 3. Memory & State

**Finding [HIGH]**: "Conversation history" is vague — no scoping defined.
- Risk: cross-session state bleed if history is stored without user-scoping (p. 148)
- Required action: Define memory using ADK state prefix system; use `user:` for cross-session, `temp:` for in-session

**Finding [MEDIUM]**: No RAG for knowledge base.
- Research agent could benefit from an internal knowledge base to avoid redundant searches (p. 217)
- Not required, but recommended for efficiency

### 4. Safety & Security

**Finding [CRITICAL]**: No guardrails for user input.
- Research questions from users are untrusted; could contain prompt injection (p. 289)
- Required action: Add input validation; behavioral constraints in system prompt

### 5. Evaluation & Observability

**Finding [HIGH]**: "Manual testing" is not a scalable eval strategy.
- No metrics defined (accuracy, latency, token usage) (p. 303)
- No evalset defined for regression testing (p. 312)
- Required action: Define: accuracy target (e.g., ">80% of reports judged 'useful' by LLM-as-Judge"), latency target, token budget

### 6. Failure Modes

**Finding [HIGH]**: "Errors will be logged" is insufficient error handling.
- No retry strategy, fallback, or escalation defined (p. 203-208)
- Web search failures are transient (should retry with backoff)
- Required action: Implement Error Triad: Detection → Classification → Recovery

---

## Step 3: Review Report

**Overall Assessment**: `NEEDS REVISION`

**Summary**: 3 CRITICAL / 3 HIGH / 2 MEDIUM / 1 LOW

### CRITICAL Findings

**[CRITICAL-001]** No max_iterations limit on agent loop
- Pattern ref: `patterns/11-goal-setting-monitoring.md`
- Evidence: p. 188 — "Set max_iterations alongside the goal"
- Required action: Add `max_iterations=10` to agent loop

**[CRITICAL-002]** `email_send` violates Principle of Least Privilege
- Pattern ref: `patterns/18-guardrails-safety.md`
- Evidence: p. 288 — "Grant agents only the tools they need"
- Required action: Remove from research agent immediately

**[CRITICAL-003]** No safety guardrails on user input
- Pattern ref: `patterns/18-guardrails-safety.md`
- Evidence: p. 286 — Six-layer defense model required
- Required action: Add input validation + output filtering at minimum

### Conditions for Approval

Before deployment:
1. Remove `email_send` tool from research agent
2. Add `max_iterations=10` with documented rationale
3. Define explicit termination criteria (SMART goal)
4. Add input validation + behavioral constraints

Within first sprint:
5. Define evaluation metrics and create evalset
6. Implement retry with backoff for transient tool failures
7. Scope memory with `user:` prefix for cross-session data

---

## Evidence Summary

| Finding | PDF Evidence |
|---------|-------------|
| max_iterations | p. 188: "Set max_iterations alongside the goal" |
| Least Privilege | p. 288: "Grant agents only the tools they need" |
| Guardrails | p. 286: Six-layer defense model |
| Prompt injection | p. 289: "Never trust tool outputs" |
| Error Triad | p. 203: "Error Detection → Error Handling → Recovery" |
| Eval metrics | p. 303: "Define metrics before building the agent" |
| Memory scoping | p. 151: `user:` / `app:` / `temp:` prefix system |
