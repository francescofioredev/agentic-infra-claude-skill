# agentic-infra — Claude Code Skill

A Claude Code skill for designing, reviewing, and linting agentic AI infrastructure. Grounded in 21 design patterns covering the full spectrum of agentic system concerns.

## What it does

- **Design**: Choose patterns for a new agentic system using a structured taxonomy
- **Review**: Audit an existing ADR/design doc against a 62-item checklist
- **Lint**: Run a deterministic linter (`lint_agentic_arch.py`) on any ADR markdown file — 17 rules, JSON output, exit code 1 on CRITICAL findings

## Installation

### Via plugin (recommended)

In Claude Code, run:

```
/plugin marketplace add francescofiore/agentic-infra-claude-skill
/plugin install agentic-infra@agentic-infra-claude-skill
```

### Manual

1. Download `agentic-infra.skill`
2. Copy it to `~/.claude/skills/`

```bash
cp agentic-infra.skill ~/.claude/skills/
```

## Usage

Just describe your task naturally — the skill triggers automatically:

```
"Help me design a customer support agent"
"Review this agentic architecture ADR"
"Lint my ADR: python3 scripts/lint_agentic_arch.py my-adr.md"
"What patterns apply to memory management in multi-agent systems?"
```

## Patterns covered (21)

| # | Pattern |
|---|---------|
| 1 | Prompt Chaining |
| 2 | Routing |
| 3 | Parallelization |
| 4 | Reflection |
| 5 | Tool Use / Function Calling |
| 6 | Planning |
| 7 | Multi-Agent Collaboration |
| 8 | Memory Management |
| 9 | Learning & Adaptation |
| 10 | Model Context Protocol (MCP) |
| 11 | Goal Setting & Monitoring |
| 12 | Exception Handling & Recovery |
| 13 | Human-in-the-Loop (HITL) |
| 14 | RAG |
| 15 | A2A Inter-Agent Communication |
| 16 | Resource-Aware Optimization |
| 17 | Reasoning Techniques |
| 18 | Guardrails / Safety |
| 19 | Evaluation & Monitoring |
| 20 | Prioritization |
| 21 | Exploration & Discovery |

## Source structure

```
.claude/skills/agentic-infra/
├── SKILL.md                    # Skill metadata + quick start
├── taxonomy.yaml               # concern → patterns mapping
├── patterns/                   # 21 pattern cards with PDF citations
├── checklists/review.md        # 62-item architecture review rubric
├── templates/                  # ADR template + review report template
├── scripts/lint_agentic_arch.py# Deterministic ADR linter (17 rules)
└── examples/                   # Design and review worked examples
```

## Evidence policy

Every rule and recommendation cites a page number from the source PDF. Format: `(p. N)`. No external sources.
