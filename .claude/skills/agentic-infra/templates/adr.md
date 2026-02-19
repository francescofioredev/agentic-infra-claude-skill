# ADR-[NUMBER]: [Short Decision Title]

**Date**: YYYY-MM-DD
**Status**: `Proposed` | `Accepted` | `Deprecated` | `Superseded by ADR-NNN`
**Deciders**: [Names / Teams]

---

## Context

<!-- What is the system being designed? What problem are we solving?
     What are the constraints (scale, latency, cost, team expertise)?
     Reference relevant concerns from taxonomy.yaml. -->

**System**: [e.g., "Customer support agent for e-commerce platform"]
**Scale**: [e.g., "~10k queries/day, <3s P95 latency target"]
**Primary concerns** (from taxonomy.yaml):
- [ ] reliability
- [ ] safety
- [ ] memory
- [ ] tool-use
- [ ] orchestration
- [ ] observability
- [ ] eval
- [ ] cost

---

## Decision

<!-- State the architectural decision clearly. Reference the pattern(s) chosen. -->

**Chosen pattern(s)**:
- Primary: [e.g., `multi-agent-collaboration` (Supervisor topology)]
- Supporting: [e.g., `rag`, `guardrails-safety`, `exception-handling-recovery`]

**Decision statement**:
> We will implement [system] using [pattern] because [reason].

---

## Pattern Analysis

<!-- For each chosen pattern, fill in the relevant fields from its pattern card. -->

### [Pattern Name] (patterns/NN-pattern-name.md)

**Why this pattern**: [Justify against forces/tradeoffs in the pattern card]

**Variant selected**: [e.g., "Supervisor topology" from pattern 07]

**Key configuration decisions**:
- [Decision 1 with page reference, e.g., "Using MCPToolset for tool delivery (p. 161)"]
- [Decision 2]
- [Decision 3]

**Known failure modes addressed**:
- [Failure mode from pattern card] → [Mitigation implemented]
- [Failure mode] → [Mitigation]

---

## Consequences

### Positive
- [Expected benefit 1]
- [Expected benefit 2]

### Negative / Risks
- [Risk 1] (Severity: High/Medium/Low)
- [Risk 2]

### Mitigations
- [Risk 1] → [Mitigation approach]
- [Risk 2] → [Mitigation approach]

---

## Tool Access Matrix

| Agent | Tools | Justification |
|-------|-------|---------------|
| [Agent Name] | [tool1, tool2] | [Why these tools, per Least Privilege (p. 288)] |
| [Agent Name] | [tool3] | |

---

## Memory Design

| Data Type | Scope | Storage | TTL |
|-----------|-------|---------|-----|
| [e.g., Conversation history] | Session | In-memory | Session end |
| [e.g., User preferences] | user: | Persistent DB | 90 days |
| [e.g., Intermediate results] | temp: | Session state | Session end |

---

## Safety Boundaries

**Guardrail layers implemented** (per p. 286):
- [ ] Input validation/sanitization
- [ ] Output filtering
- [ ] Behavioral constraints (system prompt)
- [ ] Tool use restrictions (Least Privilege)
- [ ] External moderation API
- [ ] HITL escalation

**Escalation triggers** (required per p. 211):
1. [Trigger 1, e.g., "User requests account deletion"]
2. [Trigger 2, e.g., "Confidence < 0.6 on financial advice"]

**Irreversible actions requiring HITL approval**:
- [Action 1]
- [Action 2]

---

## Evaluation Plan

**Metrics** (per p. 303):
- Accuracy target: [e.g., ">90% task completion rate"]
- Latency target: [e.g., "P95 < 3s"]
- Token budget: [e.g., "< 2000 tokens/task average"]

**Eval method**:
- [ ] Evalset file (ADK: `adk eval`)
- [ ] LLM-as-Judge rubric (dimensions: Clarity, Neutrality, Relevance, Completeness, Audience) (p. 306)
- [ ] Trajectory evaluation (p. 308)
- [ ] Human eval (gold standard)

**Baseline established**: Yes / No

---

## Open Questions

1. [Question 1 — to be resolved before implementation]
2. [Question 2]

---

## References

- [Pattern Card 1]: `.claude/skills/agentic-infra/patterns/NN-name.md`
- [Pattern Card 2]: `.claude/skills/agentic-infra/patterns/NN-name.md`
- PDF Evidence: [Chapter N, p. X] — "[Quote or paraphrase]"
