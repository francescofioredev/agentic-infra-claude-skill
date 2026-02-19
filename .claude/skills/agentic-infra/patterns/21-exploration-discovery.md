# Pattern 21: Exploration & Discovery

## Intent
Apply systematic exploration strategies — evolutionary search, debate, ranking, and iterative refinement — to discover novel solutions, research insights, or optimal configurations that cannot be specified upfront.

## Context
Use for open-ended research tasks, hypothesis generation, algorithm optimization, or any problem where the solution space is large and the evaluation function exists but the optimal solution is unknown. Exploration patterns are the agentic equivalent of search algorithms.

## Forces / Tradeoffs
- **Exploration vs. exploitation**: Too much exploration wastes resources on poor candidates; too little exploitation misses better solutions nearby.
- **Evaluation cost**: Each candidate solution must be evaluated — expensive LLM or compute evals limit population size.
- **Convergence**: Evolutionary approaches can converge to local optima. Diversity mechanisms (mutation, cross-domain seeding) prevent this.

## Solution

### Google Co-Scientist Architecture (p. 332)
Six-agent system for scientific hypothesis generation:
```
Supervisor Agent
├── Generation Agent        → Generate initial hypotheses
├── Reflection/Review Agent → Critically evaluate hypotheses
├── Ranking Agent           → Elo-based tournament ranking
├── Evolution Agent         → Refine and mutate top candidates
├── Proximity Agent         → Find related/adjacent hypotheses
└── Meta-review Agent       → Synthesize across tournament results
```
**"Generate, debate, and evolve"** approach. Validated on:
- GPQA benchmark: 78.4% top-1 accuracy (p. 335)
- Drug repurposing: KIRA6 for AML (p. 336)
- Novel epigenetic targets for liver fibrosis (p. 336)
- Antimicrobial resistance (p. 336)

### Agent Laboratory (p. 340)
Three-phase scientific research pipeline (MIT License, Samuel Schmidgall):
1. **Literature Review**: Agents survey and summarize prior work
2. **Experimentation**: Agents design, implement, and run experiments
3. **Report Writing**: Agents synthesize findings into a paper
- **Knowledge Sharing** via AgentRxiv (p. 341)

**Specialist roles:**
- `ProfessorAgent`: Sets research direction
- `PostDocAgent`: Executes experiments
- `ReviewersAgent`: Tripartite judgment — three reviewer personas evaluate quality (p. 342)
- `MLEngineeringAgent`, `SWEngineerAgent`: Implementation roles

**ReviewersAgent `get_score()` output schema** (p. 343):
```python
{
  "Summary": str,
  "Strengths": list[str],
  "Weaknesses": list[str],
  "Originality": int,  # 1-4
  "Quality": int,      # 1-4
  "Clarity": int,      # 1-4
  "Significance": int, # 1-4
  "Questions": list[str],
  "Limitations": list[str],
  "Ethical Concerns": list[str],
  "Soundness": int,    # 1-4
  "Presentation": int, # 1-4
  "Contribution": int, # 1-4
  "Overall": int,      # 1-10
  "Confidence": int,   # 1-5
  "Decision": str,     # "Accept" | "Reject"
}
```

### Elo-Based Ranking (p. 334)
For comparing N candidates without evaluating all N² pairs:
- Run round-robin "debates" between candidates
- Update Elo scores based on debate outcomes
- Top-K ranked candidates proceed to evolution phase

**Key rules:**
1. Use diverse initial generation strategies to avoid early convergence (p. 332).
2. Elo ranking is more efficient than pairwise comparison for large candidate sets — use it for N > 20 candidates (p. 334).
3. Include a Meta-review Agent to synthesize insights across multiple tournament runs (p. 335).
4. Apply "generate, debate, evolve" as the core loop: generate candidates, debate to rank, evolve top candidates (p. 332).
5. Tripartite review (three independent reviewer personas) reduces individual reviewer bias (p. 342).

## Variants
- **Evolutionary search**: AlphaEvolve-style population + selection + mutation (p. 172, Ch 9).
- **Tournament ranking**: Elo-based agent debates for pairwise comparison at scale.
- **Parallel hypothesis generation**: Multiple agents generate diverse initial candidates simultaneously.
- **Hierarchical refinement**: Generate broad → critique → evolve narrow.

## Failure Modes
- **Premature convergence**: All candidates become similar — no diversity in the population. Mitigation: explicit diversity injection (different temperature, different seed prompts).
- **Evaluation bias**: ReviewersAgent systematically favors certain types of solutions. Mitigation: tripartite review with adversarially distinct reviewer personas.
- **Elo instability**: Early matches heavily influence final rankings. Mitigation: warm-up rounds with random seeding.
- **Runaway exploration**: No convergence criterion → infinite LLM calls. Mitigation: max_rounds limit + quality threshold stopping.

## Instrumentation
- Log: candidate IDs, evaluation scores, ranking changes, evolution mutations applied.
- Track: score distribution across rounds (convergence metric), diversity metric (variance in candidate features).
- Alert: if all candidates converge to identical scores (premature convergence detected).

## Eval
- Seed with a known-optimal solution and verify it rises to the top within N rounds.
- Test diversity: verify initial generation produces meaningfully different candidates.
- Validate ReviewersAgent scoring consistency: same paper → scores within ±1 across runs.

## Related Patterns
- **Reflection** (p. 61): Review/Critique is applied within exploration to evaluate candidates.
- **Parallelization** (p. 41): Candidate generation and evaluation can run in parallel.
- **Multi-Agent Collaboration** (p. 121): Exploration uses specialized agent teams (Co-Scientist 6-agent model).
- **Learning & Adaptation** (p. 163): AlphaEvolve combines exploration with evolutionary learning.

## Evidence
- p. 330-345: Exploration chapter. Google Co-Scientist (6-agent), Agent Laboratory (3-phase).
- p. 332: Co-Scientist architecture: 6 agents in "generate, debate, evolve" loop.
- p. 334: Elo-based ranking tournament.
- p. 335: Co-Scientist GPQA 78.4% top-1 accuracy.
- p. 336: Drug repurposing / antimicrobial resistance validation.
- p. 340: Agent Laboratory 3 phases + specialist roles.
- p. 342: ReviewersAgent tripartite judgment mechanism.
- p. 343: `get_score()` JSON schema with Overall/Confidence/Decision fields.
