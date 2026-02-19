# Pattern 09: Learning & Adaptation

## Intent
Allow agents to improve their behavior over time through reinforcement learning, feedback integration, or evolutionary optimization — moving beyond static, frozen models.

## Context
Use when the agent's task has a quantifiable performance signal, when fine-tuning on interaction data is feasible, or when the system is expected to improve with usage. Not suitable for one-off tasks or when training infrastructure is unavailable.

## Forces / Tradeoffs
- **Training cost vs. improvement**: Fine-tuning or RL requires significant compute; the improvement must justify the cost.
- **Alignment stability**: Learning from feedback can cause the model to drift from its intended behavior (reward hacking).
- **Data quality**: Learning quality is bounded by feedback quality — noisy rewards produce unreliable agents.

## Solution

### Reinforcement Learning from Verifiable Rewards (RLVR) (p. 168)
Use verifiable, objective rewards (test pass/fail, math solution correctness) rather than human preferences:
```python
# Reward function for code generation agent
def reward_function(agent_output, test_cases):
    passed = sum(run_test(agent_output, t) for t in test_cases)
    return passed / len(test_cases)  # 0.0 to 1.0
```
Key frameworks: PPO (Proximal Policy Optimization), DPO (Direct Preference Optimization) (p. 163).

### SICA (Self-Improving Coding Agent) (p. 169)
Iterative self-improvement loop:
1. Agent attempts task
2. Tests run against attempt
3. Success/failure feedback used to update agent behavior
4. Repeat across many tasks

### AlphaEvolve / OpenEvolve pattern (p. 172)
Evolutionary optimization for algorithms:
- Use Gemini Flash for frequent low-cost evaluations
- Use Gemini Pro for rare high-quality evaluations
- Ensemble scoring + evolutionary selection of best solutions

**Key rules:**
1. Use verifiable rewards (code tests, math checks) over human ratings where possible — more reliable signal (p. 168).
2. Define clear performance metrics before starting training — retrofitting metrics is expensive (p. 165).
3. Monitor for reward hacking — agent finds shortcuts that maximize reward without solving the actual problem (p. 170).
4. Apply safety constraints during training (RLHF safety filtering) — unconstrained RL can produce harmful behaviors (p. 170).

## Variants
- **RLVR**: Reinforcement learning with verifiable rewards (code tests, math). Most reliable signal.
- **RLHF**: Human preference-based feedback. More flexible but noisier.
- **DPO**: Direct Preference Optimization — simpler than PPO, comparable results.
- **Evolutionary (AlphaEvolve)**: Population-based search over program variants (p. 172).
- **In-context learning**: Few-shot examples updated at inference time without retraining (cheaper, less durable).

## Failure Modes
- **Reward hacking**: Agent maximizes the reward metric through unintended shortcuts (p. 170). Mitigation: diverse evaluation suite, human spot-checks.
- **Catastrophic forgetting**: Fine-tuning on new tasks degrades performance on old ones. Mitigation: replay buffers, regularization.
- **Distribution shift**: Agent trained on historical data performs poorly on new data patterns.
- **Alignment drift**: Agent's values shift through RL, moving away from intended behavior. Mitigation: safety filters, constitutional AI constraints.

## Instrumentation
- Log: reward signal per episode, training iterations, model checkpoints.
- Track: performance on held-out eval set across training time (learning curve).
- Alert: if eval performance drops during training (negative transfer signal).

## Eval
- Maintain a frozen held-out test set that is never used in training.
- Compare pre-training vs. post-training performance on the held-out set.
- Test for reward hacking by including adversarial test cases the reward function doesn't cover.

## Related Patterns
- **Reflection** (p. 61): Immediate inference-time improvement vs. Learning's durable weight updates.
- **Evaluation & Monitoring** (p. 301): Evaluation infrastructure is prerequisite for learning signal.
- **Exploration & Discovery** (p. 330): AlphaEvolve uses evolutionary exploration + learning.

## Evidence
- p. 163-172: Learning & Adaptation chapter covering PPO, DPO, RLVR, SICA, AlphaEvolve.
- p. 168: RLVR — verifiable rewards produce more reliable training signal than human preferences.
- p. 169: SICA self-improving coding agent loop.
- p. 172: AlphaEvolve ensemble: Gemini Flash (frequent cheap) + Gemini Pro (rare quality) for evolutionary optimization.
