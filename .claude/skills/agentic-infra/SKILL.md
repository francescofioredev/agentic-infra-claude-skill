---
name: agentic-infra
description: >
  Knowledge base for designing, reviewing, and linting agentic AI infrastructure.
  Use when: (1) designing a new agentic system and need to choose patterns,
  (2) reviewing an existing agentic architecture ADR or design doc for gaps/risks,
  (3) applying the lint script to an ADR markdown file to get structured findings,
  (4) looking up a specific agentic pattern (prompt chaining, routing, parallelization,
  reflection, tool use, planning, multi-agent collaboration, memory management,
  learning/adaptation, MCP, goal setting, exception handling, HITL, RAG, A2A,
  resource optimization, reasoning techniques, guardrails, evaluation, prioritization,
  exploration/discovery).
  All rules and guidance are grounded in the PDF "Agentic Design Patterns" (482 pages).
---

# Agentic Infra Skill

## Quick Start

**Design use case**: "Help me design a customer support agent"
→ Consult `taxonomy.yaml` to identify relevant concerns → load the relevant `patterns/*.md` cards → use `templates/adr.md`

**Review use case**: "Review this agentic architecture ADR"
→ Run `scripts/lint_agentic_arch.py <adr.md>` → cross-reference findings against `checklists/review.md` → produce `templates/review-report.md`

## Taxonomy

See `taxonomy.yaml` for the full concern → patterns mapping across 8 concern areas:
`reliability`, `safety`, `memory`, `tool-use`, `orchestration`, `observability`, `eval`, `cost`

## Pattern Library

All 21 patterns have full pattern cards in `patterns/`. Each card specifies:
- Intent, context, forces/tradeoffs
- Solution with code evidence
- Failure modes and instrumentation
- Related patterns and PDF page citations

| # | Pattern | File |
|---|---------|------|
| 1 | Prompt Chaining | patterns/01-prompt-chaining.md |
| 2 | Routing | patterns/02-routing.md |
| 3 | Parallelization | patterns/03-parallelization.md |
| 4 | Reflection | patterns/04-reflection.md |
| 5 | Tool Use / Function Calling | patterns/05-tool-use.md |
| 6 | Planning | patterns/06-planning.md |
| 7 | Multi-Agent Collaboration | patterns/07-multi-agent-collaboration.md |
| 8 | Memory Management | patterns/08-memory-management.md |
| 9 | Learning & Adaptation | patterns/09-learning-adaptation.md |
| 10 | Model Context Protocol (MCP) | patterns/10-mcp.md |
| 11 | Goal Setting & Monitoring | patterns/11-goal-setting-monitoring.md |
| 12 | Exception Handling & Recovery | patterns/12-exception-handling-recovery.md |
| 13 | Human-in-the-Loop (HITL) | patterns/13-hitl.md |
| 14 | RAG | patterns/14-rag.md |
| 15 | A2A Inter-Agent Communication | patterns/15-a2a-communication.md |
| 16 | Resource-Aware Optimization | patterns/16-resource-aware-optimization.md |
| 17 | Reasoning Techniques | patterns/17-reasoning-techniques.md |
| 18 | Guardrails / Safety | patterns/18-guardrails-safety.md |
| 19 | Evaluation & Monitoring | patterns/19-evaluation-monitoring.md |
| 20 | Prioritization | patterns/20-prioritization.md |
| 21 | Exploration & Discovery | patterns/21-exploration-discovery.md |

## Review Workflow

1. Run lint script: `python3 scripts/lint_agentic_arch.py <path/to/adr.md>`
2. Inspect JSON findings (each finding includes: `severity`, `rule`, `pattern_ref`, `evidence_page`)
3. Walk `checklists/review.md` for any gaps not caught by lint
4. Fill in `templates/review-report.md` with findings

## Design Workflow

1. Identify system concerns from `taxonomy.yaml`
2. Load the pattern cards for those concerns
3. Choose patterns considering forces/tradeoffs in each card
4. Record decisions in `templates/adr.md`
5. Self-check against `checklists/review.md` before finalizing

## Examples

- Design scenario: `examples/design-example.md`
- Review scenario: `examples/review-example.md`

## Evidence Policy

Every rule in this skill cites a PDF page. Format: `(p. N)`. Never state a rule without citation.
