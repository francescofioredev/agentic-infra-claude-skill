# Agentic Architecture Review Report

**Review Date**: YYYY-MM-DD
**Reviewer**: [Name / Agent]
**System Under Review**: [System Name]
**ADR(s) Reviewed**: [ADR-001, ...]
**Checklist Score**: [N/62]

---

## Executive Summary

<!-- 2-3 sentence summary of the overall assessment -->

**Overall Assessment**: `APPROVED` | `APPROVED WITH CONDITIONS` | `NEEDS REVISION` | `REJECTED`

**Critical findings**: [N critical / N high / N medium / N low]

---

## Lint Findings

<!-- Output from scripts/lint_agentic_arch.py <adr.md> — paste JSON here or summarize -->

```json
{
  "summary": {
    "critical": N,
    "high": N,
    "medium": N,
    "low": N,
    "total": N
  },
  "findings": [...]
}
```

---

## Detailed Findings

### CRITICAL Findings

> Issues that must be resolved before deployment. High probability of production failure or security breach.

---

**[CRITICAL-001]** [Short finding title]

- **Rule**: [Rule ID from lint or checklist]
- **Location**: [ADR section / line reference]
- **Pattern Reference**: `patterns/NN-name.md`
- **Evidence**: PDF p. [N] — "[Supporting quote]"
- **Finding**: [What is missing or wrong]
- **Required Action**: [What must be done]
- **Verification**: [How to verify the fix]

---

### HIGH Findings

> Issues that significantly increase risk or degrade quality. Should be resolved before deployment or within the first sprint.

---

**[HIGH-001]** [Short finding title]

- **Rule**: [Rule ID]
- **Pattern Reference**: `patterns/NN-name.md`
- **Evidence**: PDF p. [N]
- **Finding**: [What is suboptimal or risky]
- **Recommended Action**: [Suggested fix]

---

### MEDIUM Findings

> Issues that reduce quality or increase technical debt. Address in the near term.

---

**[MEDIUM-001]** [Short finding title]

- **Rule**: [Rule ID]
- **Pattern Reference**: `patterns/NN-name.md`
- **Evidence**: PDF p. [N]
- **Finding**: [What is missing]
- **Recommended Action**: [Suggestion]

---

### LOW / INFORMATIONAL Findings

---

**[LOW-001]** [Short finding title]

- **Rule**: [Rule ID]
- **Finding**: [Minor issue or improvement opportunity]
- **Suggested Action**: [Optional improvement]

---

## Strengths

<!-- Document what the design does well -->

1. [Strength 1] — [Why this is good, with pattern ref]
2. [Strength 2]
3. [Strength 3]

---

## Checklist Summary

| Area | Score | Notes |
|------|-------|-------|
| Architecture & Orchestration | [N/11] | |
| Tool Use & Integrations | [N/9] | |
| Memory & State | [N/10] | |
| Safety & Security | [N/12] | |
| Evaluation & Observability | [N/9] | |
| Failure Modes & Recovery | [N/7] | |
| Cost Optimization | [N/4] | |
| **Total** | **[N/62]** | |

---

## Evidence Requests

<!-- List any claims in the ADR that require additional evidence or documentation -->

| # | Claim | Evidence Needed |
|---|-------|----------------|
| 1 | [Claim from ADR] | [What evidence would support this] |
| 2 | | |

---

## Conditions for Approval

<!-- If status is APPROVED WITH CONDITIONS, list what must be done -->

1. **Before deployment**: [Required action 1]
2. **Before deployment**: [Required action 2]
3. **Within first sprint**: [Required action 3]

---

## Reviewer Sign-off

| Reviewer | Role | Decision | Date |
|----------|------|----------|------|
| [Name] | [Architect/Engineer] | `APPROVED` / `REJECTED` | YYYY-MM-DD |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial review |
