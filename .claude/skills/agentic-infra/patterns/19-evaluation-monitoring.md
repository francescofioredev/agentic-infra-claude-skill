# Pattern 19: Evaluation & Monitoring

## Intent
Measure agent performance with quantitative metrics and qualitative quality assessments, enabling continuous improvement and early detection of regressions.

## Context
Use to close the feedback loop in any production agent system. Without evaluation, you cannot know whether the agent is improving, regressing, or performing at a target level. Evaluation is a prerequisite for learning (pattern 09) and a prerequisite for knowing when to escalate (pattern 13).

## Forces / Tradeoffs
- **Automated vs. human eval**: Automated metrics (exact match, LLM-as-Judge) are scalable but imperfect; human eval is gold-standard but expensive and slow.
- **Eval set staleness**: Eval sets can become unrepresentative of real usage over time.
- **Goodhart's Law**: Optimizing for the eval metric can cause agents to game it without genuinely improving.

## Solution

### Five-level Best Practices Pyramid (p. 303):
1. **Define metrics** (accuracy, latency, token usage, cost)
2. **Collect quantitative + qualitative data** regularly
3. **Evaluate regularly** (CI/CD integration + periodic batch eval)
4. **Reward agents** for improvements (training signal)
5. **Feedback/coaching** for systematic improvement

### Core Metrics (p. 304):
- **Accuracy**: Correct task completion rate on eval set
- **Latency**: P50/P95/P99 response times
- **Token usage**: Input + output tokens per task (cost proxy)
- **Tool call accuracy**: Correct tool selection + parameter generation rate

### LLM-as-a-Judge (p. 306)
Use an LLM to evaluate response quality on a rubric:
```python
JUDGE_RUBRIC = """
Evaluate this agent response on a 1-5 scale for each dimension:
- Clarity: Is the response clear and well-structured?
- Neutrality: Is it free of bias?
- Relevance: Does it address the user's question?
- Completeness: Does it cover all aspects?
- Audience: Is it appropriate for the target audience?

Response to evaluate: {response}
User query: {query}
Return: {"clarity": N, "neutrality": N, "relevance": N, "completeness": N, "audience": N, "overall": N}
"""
```

### Agent Trajectory Evaluation (p. 308)
For multi-step agents, evaluate the sequence of actions (not just final output):
- **Exact order match**: Steps match expected sequence exactly
- **In-order match**: Expected steps present in order (ignores extra steps)
- **Any-order match**: All expected steps present regardless of order
- **Single-tool accuracy**: Each individual tool call is correct

### `LLMInteractionMonitor` class (p. 310):
```python
class LLMInteractionMonitor:
    def record(self, query, response, tool_calls, latency_ms, tokens):
        self.db.insert({
            "timestamp": datetime.now(),
            "query": query,
            "response": response,
            "tool_calls": tool_calls,
            "latency_ms": latency_ms,
            "tokens": tokens,
        })

    def compute_metrics(self, window="24h") -> dict:
        return {
            "avg_latency": ...,
            "p95_latency": ...,
            "avg_tokens": ...,
            "error_rate": ...,
        }
```

### ADK Evaluation Methods (p. 314):
- `adk web` — Interactive web UI for manual evaluation
- `AgentEvaluator.evaluate()` — pytest-based programmatic evaluation
- `adk eval` — CLI batch evaluation against evalset files

**Key rules:**
1. Define metrics before building the agent — retrofitting metrics is unreliable (p. 303).
2. Use separate test files and evalset files — test files test individual components; evalset files test end-to-end behavior (p. 312).
3. LLM-as-Judge rubrics should specify 5 dimensions: Clarity, Neutrality, Relevance, Completeness, Audience (p. 306).
4. Evaluate agent trajectories, not just final outputs — a correct answer via a wrong path is a bug (p. 308).
5. Track metrics over time; a declining trend is more important than a single data point (p. 305).

## Variants
- **Offline batch eval**: Run against frozen evalset; track metrics over model versions.
- **Online eval**: Sample production traffic; evaluate live responses (lower coverage, real distribution).
- **A/B eval**: Compare two agent versions on same inputs.
- **Human eval**: Expert reviewers score responses on rubric (gold standard).

## Failure Modes
- **Eval-train contamination**: Eval set leaks into training data — inflated metrics (p. 313). Mitigation: strict train/eval separation.
- **Eval set distribution drift**: Eval set no longer represents production queries. Mitigation: periodic eval set refresh.
- **LLM-Judge bias**: Judge model has inherent biases (verbosity preference, self-preference). Mitigation: use judge model different from generator; calibrate against human eval.

## Instrumentation
- Log: every interaction with full context (query, response, tool calls, latency, tokens).
- Dashboard: real-time metrics + trend charts.
- Alert: metric degradation > 10% from baseline.

## Eval (meta)
- Calibrate LLM-as-Judge against human labels: measure judge-human agreement (Cohen's kappa target >0.7).
- Verify trajectory evaluation correctly identifies missing/reordered steps.

## Related Patterns
- **Reflection** (p. 61): LLM-as-Judge shares the critique rubric with Reflection.
- **Learning & Adaptation** (p. 163): Evaluation metrics provide the reward/feedback signal for learning.
- **HITL** (p. 207): Human evaluation is the gold-standard for quality assessment.

## Evidence
- p. 301-314: Evaluation chapter. 5-level pyramid, core metrics, LLM-as-Judge, trajectory evaluation.
- p. 303: Best practices pyramid: Define → Collect → Evaluate → Reward → Coach.
- p. 306: LLM-as-Judge rubric: Clarity, Neutrality, Relevance, Completeness, Audience.
- p. 308: Agent trajectory evaluation: exact-order, in-order, any-order, single-tool.
- p. 310: `LLMInteractionMonitor` class.
- p. 312: Test files vs. evalset files in ADK.
- p. 314: ADK eval methods: `adk web`, `AgentEvaluator.evaluate()`, `adk eval`.
