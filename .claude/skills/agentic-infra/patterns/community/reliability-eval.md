# Community Patterns: Reliability & Eval
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns for making agentic systems trustworthy: evaluation frameworks that measure output quality, monitoring approaches that detect degradation, and reliability patterns that prevent and recover from failures. Eval and reliability are inseparable in production agents.

**16 patterns in this category.** For full detail on key patterns, see:
- Pattern 19: Evaluation & Monitoring (`patterns/19-evaluation-monitoring.md`)
- Pattern 12: Exception Handling & Recovery (`patterns/12-exception-handling-recovery.md`)
- Pattern 30: LLM Observability (`patterns/30-llm-observability.md`)

---

## Patterns

### LLM Observability
**Status**: established
**Problem**: LLM applications in production are black boxes — cost, latency, and failure root causes are invisible.
**Solution**: Instrument all LLM calls with distributed traces, cost/token metrics, and structured logs. See Pattern 30 for full detail.
**Tags**: observability, tracing, metrics, production
**Reference**: See Pattern 30 (`patterns/30-llm-observability.md`)

### LLM-as-a-Judge
**Status**: established
**Problem**: Human evaluation is the gold standard but doesn't scale to production output volumes.
**Solution**: Use a capable LLM with a structured rubric to evaluate other LLM outputs. Validate judge agreement with human ratings on a calibration set. See Pattern 19 for full detail.
**Tags**: eval, LLM-judge, quality, scale
**Reference**: See Pattern 19 (`patterns/19-evaluation-monitoring.md`)

### Regression Test Suite
**Status**: established
**Problem**: Prompt or model changes improve some cases but silently break others.
**Solution**: Maintain a curated test suite of (input, expected_output, evaluation_criteria) triples. Run the suite before every prompt/model change; gate deployment on pass rate above threshold.
**Tags**: testing, regression, deployment, CI
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Golden Set Evaluation
**Status**: established
**Problem**: Automated metrics diverge from human judgment; there is no ground truth to calibrate against.
**Solution**: Maintain a manually curated golden set of (input, ideal_output) pairs; evaluate new model/prompt versions against the golden set; track human evaluation score as the primary quality metric.
**Tags**: eval, golden-set, human, ground-truth
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### A/B Evaluation
**Status**: established
**Problem**: Two model or prompt versions produce similar automated scores but one is clearly better to humans.
**Solution**: Run both versions on the same inputs; collect pairwise human or AI preferences; declare winner when preference is statistically significant. Use for prompt optimization and model selection.
**Tags**: A/B, comparison, preference, model-selection
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Adversarial Evaluation
**Status**: established
**Problem**: Standard evaluation sets miss edge cases and adversarial inputs that break production agents.
**Solution**: Generate adversarial test cases: jailbreak attempts, ambiguous queries, contradictory context, extreme edge cases. Include in the test suite and monitor failure rate on adversarial inputs separately.
**Tags**: eval, adversarial, robustness, red-teaming
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Canary Deployment
**Status**: established
**Problem**: New model or prompt versions may degrade quality for a subset of production traffic before full rollout.
**Solution**: Route a small percentage (1-5%) of traffic to the new version; monitor quality metrics and error rates; compare against the control group; full rollout only if canary metrics are satisfactory.
**Tags**: deployment, canary, A/B, risk
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Eval-Driven Development
**Status**: emerging
**Problem**: Prompt engineering is ad-hoc; improvements are not systematically measured.
**Solution**: Before changing any prompt, define the evaluation criteria and create test cases. Change the prompt. Run the eval. Only accept changes that improve the eval score. Treat evals as tests in TDD.
**Tags**: eval, TDD, prompt-engineering, systematic
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Confidence Calibration
**Status**: emerging
**Problem**: Agent expresses high confidence on wrong answers and low confidence on correct answers; confidence is poorly calibrated.
**Solution**: Measure calibration: compare stated confidence levels against empirical accuracy; fine-tune or prompt-engineer to align expressed confidence with actual accuracy. Use Expected Calibration Error (ECE) as the metric.
**Tags**: calibration, confidence, reliability, uncertainty
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Graceful Degradation
**Status**: established
**Problem**: Primary LLM or tool failure causes total system failure even when a lower-quality fallback is available.
**Solution**: Define a fallback chain: primary model → smaller model → rule-based fallback → human escalation. Detect primary failure; automatically downgrade to the next available option; alert operators.
**Tags**: fallback, degradation, resilience, availability
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Retry with Exponential Backoff
**Status**: established
**Problem**: Transient API failures cause permanent task failures when a simple retry would succeed.
**Solution**: Wrap all external API calls with retry logic: on failure, wait `base_delay * 2^attempt` before retrying; cap at max_delay; give up after max_attempts; log all retry attempts.
**Tags**: retry, backoff, resilience, transient-failure
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Schema Validation Gate
**Status**: established
**Problem**: LLM outputs that are supposed to be structured (JSON, code) sometimes fail to parse, causing downstream failures.
**Solution**: Validate every structured LLM output against the expected schema before passing it downstream. On validation failure, retry with a correction prompt that includes the validation error. Gate on maximum retries.
**Tags**: validation, schema, reliability, structured-output
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Cost Budget Enforcement
**Status**: established
**Problem**: Runaway agent loops consume far more tokens than expected, causing budget overruns.
**Solution**: Set a per-task token budget at task start; track cumulative token consumption across all LLM calls; abort task and return partial result when budget is exhausted; alert on tasks within N% of budget.
**Tags**: cost, budget, safety, tokens
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Anomaly Detection
**Status**: established
**Problem**: Agent behavior degrades gradually in ways that are not caught by threshold-based alerts.
**Solution**: Apply statistical anomaly detection to agent metrics (output length distribution, latency, error rate, tool call patterns); alert when metrics deviate significantly from historical baseline.
**Tags**: anomaly, monitoring, statistics, drift
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Structured Error Taxonomy
**Status**: established
**Problem**: Error logs contain unstructured text; it is hard to identify systemic failure patterns.
**Solution**: Classify all agent errors into a structured taxonomy (input error, planning error, tool failure, output error, timeout, safety violation); tag every error with its type; aggregate by type for trend analysis.
**Tags**: errors, taxonomy, observability, analysis
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval

### Evaluation Pipeline Automation
**Status**: established
**Problem**: Evaluation is run manually and infrequently; quality regressions are caught too late.
**Solution**: Integrate evaluation into the CI/CD pipeline; run eval suite on every commit; block deployment if eval score drops below the baseline; publish eval reports as build artifacts.
**Tags**: eval, CI/CD, automation, deployment
**Reference**: Source: awesome-agentic-patterns — Reliability & Eval
