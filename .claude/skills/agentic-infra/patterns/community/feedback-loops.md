# Community Patterns: Feedback Loops
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns that enable agents to improve their outputs through iterative evaluation and refinement — at inference time (self-critique, validation loops) or training time (RLAIF, preference learning). These patterns treat improvement as a first-class architectural concern, not an afterthought.

**13 patterns in this category.** For full detail on key patterns, see:
- Pattern 04: Reflection (`patterns/04-reflection.md`)
- Pattern 31: Reflection Loop / Self-Critique (`patterns/31-reflection-feedback-loop.md`)
- Pattern 28: RLAIF (`patterns/28-rlaif.md`)
- Pattern 19: Evaluation & Monitoring (`patterns/19-evaluation-monitoring.md`)

---

## Patterns

### Reflection Loop / Self-Critique
**Status**: established
**Problem**: Single-pass LLM outputs are reliably improvable in quality-sensitive tasks (code, essays, structured extraction).
**Solution**: Explicit generate-critique-revise loop with structured rubric, iteration limit, and quality score tracking. See Pattern 31 for full detail.
**Tags**: reflection, self-critique, quality, iteration
**Reference**: See Pattern 31 (`patterns/31-reflection-feedback-loop.md`)

### RLAIF (RL from AI Feedback)
**Status**: established
**Problem**: Human annotation cannot scale to the volume of outputs needed for RL training of production agents.
**Solution**: Use an LLM judge to provide reward signals for policy training; audit with human labels on a sample. See Pattern 28 for full detail.
**Tags**: RLAIF, training, reward, scale
**Reference**: See Pattern 28 (`patterns/28-rlaif.md`)

### Constitutional AI Self-Revision
**Status**: established
**Problem**: Agent outputs may violate safety principles or guidelines in ways that are hard to catch with simple filters.
**Solution**: After initial generation, agent critiques its own output against a list of constitutional principles, identifies violations, and revises. Critique-revision pairs can also serve as training data.
**Tags**: safety, self-revision, constitutional, principles
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Test-Driven Revision
**Status**: established
**Problem**: For code generation tasks, LLM self-critique is unreliable; objective correctness can be verified by running tests.
**Solution**: Generate code → run tests → feed failing tests back to the agent as critique → revise → repeat until all tests pass or budget exhausted. Deterministic feedback replaces LLM judgment.
**Tags**: code, tests, feedback, deterministic
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Critic-as-Tool
**Status**: established
**Problem**: Self-critique in a single-prompt is weak; the model tends to approve its own output.
**Solution**: Implement the critic as a separate tool the agent can explicitly call with structured parameters (output, evaluation_criteria). Tool returns structured feedback the agent must address.
**Tags**: reflection, tool, critic, separation
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Human Feedback Integration
**Status**: established
**Problem**: Agent operating in production receives implicit user signals (corrections, retries, thumbs down) that are not fed back to improve behavior.
**Solution**: Capture explicit and implicit user feedback signals; route them into a feedback store; use them for fine-tuning or prompt improvement on a regular cadence.
**Tags**: RLHF, human-feedback, improvement, production
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Preference Learning Loop
**Status**: established
**Problem**: Scalar reward signals are hard to specify for subjective quality; humans are better at ranking outputs.
**Solution**: Collect human or AI pairwise preferences (A vs. B); train a preference model (Bradley-Terry); use preference model as reward signal for DPO or PPO training.
**Tags**: DPO, preferences, ranking, training
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Adversarial Critique
**Status**: emerging
**Problem**: Friendly critics approve outputs too readily; sycophancy reduces critique quality.
**Solution**: Frame the critic with an adversarial persona ("Your job is to find flaws in this output. Be harsh and specific."). Adversarial framing produces more thorough critiques.
**Tags**: reflection, adversarial, critique, quality
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Multi-Dimensional Critique
**Status**: established
**Problem**: A single critique dimension misses important quality aspects; different dimensions require different expertise.
**Solution**: Invoke separate critic agents for different dimensions (correctness, style, safety, performance); aggregate their feedback before revision.
**Tags**: reflection, multi-agent, dimensions, critique
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Reward Model Calibration
**Status**: emerging
**Problem**: AI reward models drift from human preferences over time as the policy model distribution shifts.
**Solution**: Periodically re-calibrate the reward model against fresh human labels; track human-AI alignment score; automatically pause training when alignment drops below threshold.
**Tags**: reward, calibration, alignment, RLAIF
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Online Feedback Collection
**Status**: established
**Problem**: Batch annotation pipelines are too slow; feedback collection needs to be continuous.
**Solution**: Instrument production to capture feedback in real-time; feed into a streaming training pipeline; deploy improved model checkpoints on a rolling basis.
**Tags**: feedback, online, streaming, continuous
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Critique History Persistence
**Status**: established
**Problem**: Multi-iteration revision often re-introduces previously fixed issues because the reviser doesn't know what has already been fixed.
**Solution**: Maintain a critique history log across iterations; include it in every reviser prompt; explicitly instruct reviser to verify previously fixed issues are not re-introduced.
**Tags**: reflection, history, persistence, regression
**Reference**: Source: awesome-agentic-patterns — Feedback Loops

### Quality Gate Pattern
**Status**: established
**Problem**: Output quality is inconsistent; some outputs are excellent, others are poor, but they are all treated equally.
**Solution**: Before delivering any output, evaluate it against minimum quality criteria. Route outputs below the threshold back to revision (up to N attempts) before delivery. Only deliver outputs that pass the gate.
**Tags**: quality, gate, threshold, reliability
**Reference**: Source: awesome-agentic-patterns — Feedback Loops
