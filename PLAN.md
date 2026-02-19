# PLAN.md — Agentic Infra Skill

## PDF Index

| Chapter | Title | PDF Pages |
|---------|-------|-----------|
| Ch 1 | Prompt Chaining | ~1–20 |
| Ch 2 | Routing | ~21–40 |
| Ch 3 | Parallelization | ~41–60 |
| Ch 4 | Reflection | ~61–80 |
| Ch 5 | Tool Use / Function Calling | ~81–100 |
| Ch 6 | Planning | ~101–120 |
| Ch 7 | Multi-Agent Collaboration | ~121–140 |
| Ch 8 | Memory Management | ~141–162 |
| Ch 9 | Learning & Adaptation | ~163–180 |
| Ch 10 | Model Context Protocol (MCP) | ~155–182 |
| Ch 11 | Goal Setting & Monitoring | ~183–200 |
| Ch 12 | Exception Handling & Recovery | ~201–220 |
| Ch 13 | Human-in-the-Loop (HITL) | ~207–220 |
| Ch 14 | RAG | ~215–240 |
| Ch 15 | A2A Inter-Agent Communication | ~240–260 |
| Ch 16 | Resource-Aware Optimization | ~255–275 |
| Ch 17 | Reasoning Techniques | ~261–284 |
| Ch 18 | Guardrails / Safety | ~285–301 |
| Ch 19 | Evaluation & Monitoring | ~301–320 |
| Ch 20 | Prioritization | ~321–330 |
| Ch 21 | Exploration & Discovery | ~330–355 |
| App A | Advanced Prompting Techniques | ~355–380 |
| App B | GUI to Real World (ACIs) | ~380–395 |
| App C | Agentic Frameworks Overview | ~395–410 |
| App D | AgentSpace | ~410–418 |
| App E | AI Agents on the CLI | ~418–430 |
| App G | Coding Agents | ~430–445 |
| — | Conclusion | ~445–455 |

## Skill Structure

```
.claude/skills/agentic-infra/
├── SKILL.md                         ✅ DONE
├── taxonomy.yaml                    ✅ DONE
├── patterns/
│   ├── 01-prompt-chaining.md        ✅ DONE
│   ├── 02-routing.md                ✅ DONE
│   ├── 03-parallelization.md        ✅ DONE
│   ├── 04-reflection.md             ✅ DONE
│   ├── 05-tool-use.md               ✅ DONE
│   ├── 06-planning.md               ✅ DONE
│   ├── 07-multi-agent-collaboration.md ✅ DONE
│   ├── 08-memory-management.md      ✅ DONE
│   ├── 09-learning-adaptation.md    ✅ DONE
│   ├── 10-mcp.md                    ✅ DONE
│   ├── 11-goal-setting-monitoring.md ✅ DONE
│   ├── 12-exception-handling-recovery.md ✅ DONE
│   ├── 13-hitl.md                   ✅ DONE
│   ├── 14-rag.md                    ✅ DONE
│   ├── 15-a2a-communication.md      ✅ DONE
│   ├── 16-resource-aware-optimization.md ✅ DONE
│   ├── 17-reasoning-techniques.md   ✅ DONE
│   ├── 18-guardrails-safety.md      ✅ DONE
│   ├── 19-evaluation-monitoring.md  ✅ DONE
│   ├── 20-prioritization.md         ✅ DONE
│   └── 21-exploration-discovery.md  ✅ DONE
├── checklists/
│   └── review.md                    ✅ DONE
├── templates/
│   ├── adr.md                       ✅ DONE
│   └── review-report.md             ✅ DONE
├── scripts/
│   └── lint_agentic_arch.py         ✅ DONE
└── examples/
    ├── design-example.md            ✅ DONE
    └── review-example.md            ✅ DONE
```

## Pattern Card Schema

```yaml
name: <pattern name>
intent: <one-sentence purpose>
context: <when this pattern applies>
forces:
  - <tension 1>
  - <tension 2>
solution: <how the pattern resolves the forces>
variants:
  - <named variant and distinguishing trait>
failure_modes:
  - <failure name>: <description>
instrumentation:
  - <what to measure/log>
eval:
  - <how to evaluate correctness>
related_patterns:
  - <pattern name>: <relationship>
evidence:
  - page: <N>
    quote: "<exact or paraphrased text>"
```

## Quality Criteria

- Every rule/best practice cites a PDF page number
- No external sources referenced
- Pattern cards are deterministic: same input → same findings
- All 21 patterns have full cards
- Lint script produces machine-readable JSON output
- Examples demonstrate both design and review workflows

## Self-Review Status

**Completed (2026-02-19)**

| Deliverable | Status | Notes |
|-------------|--------|-------|
| PLAN.md | ✅ DONE | This file |
| SKILL.md | ✅ DONE | Validated by package_skill.py |
| taxonomy.yaml | ✅ DONE | 8 concern areas, all 21 patterns mapped |
| patterns/01-21 | ✅ DONE | All 21 fully detailed pattern cards |
| checklists/review.md | ✅ DONE | 62-item rubric across 7 areas |
| templates/adr.md | ✅ DONE | Full ADR template with all required sections |
| templates/review-report.md | ✅ DONE | Findings template with severity levels |
| scripts/lint_agentic_arch.py | ✅ DONE | 17 rules, JSON+text output, exit code 1 on CRITICAL |
| examples/design-example.md | ✅ DONE | Customer support agent full design walkthrough |
| examples/review-example.md | ✅ DONE | Research pipeline review with lint output |
| agentic-infra.skill | ✅ DONE | Packaged and validated |

**Self-Review Findings:**
- Lint script tested on PLAN.md — fires correctly (10 findings, correct rule triggers)
- All pattern cards include at least 3 PDF page citations
- No external sources referenced in any file
- Every lint rule includes `evidence_page` and `evidence_quote` from PDF
- Examples cover both design and review workflows with full citation chains

**Known Limitations:**
- Page number ranges are approximate (PDF renderer returns visual pages, not absolute pages; actual chapter pages shift slightly from the ~N estimates in the index)
- Lint rules are keyword-based (deterministic, no LLM) — catches structural gaps but not semantic quality issues in ADR prose
- taxonomy.yaml maps concerns → pattern names (strings), not linked objects — navigated by reading SKILL.md pattern table
