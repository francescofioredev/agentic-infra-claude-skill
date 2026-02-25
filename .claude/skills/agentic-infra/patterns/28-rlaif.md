# Pattern 28: RLAIF (Reinforcement Learning from AI Feedback)

**Source**: awesome-agentic-patterns — Learning & Adaptation

## Intent
Use one or more AI models as reward signal sources to train or fine-tune another agent model, replacing or supplementing expensive human annotation with scalable automated feedback.

## Context
Use when: (1) human labeling is too slow or expensive to provide feedback at the scale needed for RL training, (2) the task has a clear quality criterion that can be evaluated by a capable LLM (e.g., helpfulness, harmlessness, code correctness), or (3) you need to continuously improve an agent from its own operation logs without human-in-the-loop bottlenecks. Common in production agents where output volume far exceeds human reviewer capacity.

## Forces / Tradeoffs
- **Scalability vs. accuracy**: AI feedback scales infinitely but may be biased, inconsistent, or reward-hacking. Human feedback is the ground truth but doesn't scale.
- **Feedback model quality**: RLAIF quality is bounded by the feedback model's quality. Using the same model family as the policy model risks reward hacking.
- **Alignment risk**: AI feedback may perpetuate or amplify the feedback model's biases. Regular human audits are essential.
- **Cost**: Running a large LLM as a reward model on every training sample is expensive. Use smaller judges for high-volume, larger for audits.

## Solution
Implement a **AI-Feedback Pipeline**:

**Phase 1 — Feedback Collection:**
1. Collect agent outputs from production or a rollout environment.
2. Pass each output (with its input and optional reference) to a **Judge LLM** with an explicit evaluation rubric.
3. Judge returns a scalar reward score (e.g., 0-10) or a preference judgment (output A vs. B).
4. Optionally: use multiple judge models and average their scores (ensemble judging).

**Phase 2 — Policy Training:**
1. Use collected (input, output, reward) triples as training signal for Proximal Policy Optimization (PPO) or Direct Preference Optimization (DPO).
2. Train the policy model to maximize the reward signal.
3. Periodically validate against a human-labeled holdout set to detect reward hacking.

**Phase 3 — Audit & Human Oversight:**
1. Sample N% of AI-feedback judgments for human review.
2. Compute alignment score (% where human agrees with AI judge).
3. If alignment drops below threshold, pause training and retrain the judge.

**Key rules:**
1. Never use the policy model as its own reward model — use a separate, preferably different model family.
2. Always maintain a human-labeled validation set; it is the ground truth.
3. Include a **Constitutional AI**-style critique step: have the judge first reason about quality before scoring.
4. Set a max reward ceiling to prevent over-optimization (reward hacking).

**Pseudo-implementation:**
```python
# Feedback collection
for (input, output) in production_sample:
    critique = judge.invoke(f"Evaluate: {input}\nResponse: {output}\nRubric: {rubric}")
    reward = judge.score(critique)
    training_data.append((input, output, reward))

# Policy update
trainer.train_ppo(policy_model, training_data)

# Audit
human_alignment = compute_alignment(training_data[:audit_sample], human_labels)
assert human_alignment > 0.8, "Judge alignment too low — halt training"
```

## Variants
- **Constitutional AI (CAI)**: Judge critiques output against a set of principles before scoring; self-revision before final score.
- **RLHF hybrid**: Start with RLHF to build the initial reward model, then switch to RLAIF for scale.
- **Preference-based RLAIF**: Judge outputs preference rankings (A > B > C) for DPO training rather than scalar rewards.
- **Multi-objective RLAIF**: Multiple judges evaluate different dimensions (helpfulness, safety, factuality); combine into a weighted reward.

## Failure Modes
- **Reward hacking**: Policy learns to generate outputs that score high on AI judge but are low quality to humans. Mitigation: regular human audits + diverse judge ensemble.
- **Mode collapse**: Policy converges to a narrow output distribution that the judge rewards. Mitigation: entropy regularization in RL training.
- **Judge bias amplification**: If judge model has systematic biases (length preference, style preference), policy amplifies them. Mitigation: bias-aware rubrics; test for known biases before deployment.
- **Distribution shift**: Training data distribution diverges from production inputs over time. Mitigation: continuous data freshness monitoring.

## Instrumentation
- Track: `human_judge_alignment`, `reward_score_distribution`, `policy_entropy` over training.
- Alert: if human alignment drops below 80% or reward score variance collapses (mode collapse signal).
- Log: all judge inputs and outputs for full audit trail.

## Related Patterns
- **Reflection** (Pattern 04): RLAIF uses LLM-as-critic at training time; Reflection uses it at inference time.
- **Evaluation & Monitoring** (Pattern 19): LLM-as-a-Judge at inference time; same mechanism applied to training.
- **Learning & Adaptation** (Pattern 09): RLAIF is one implementation of the learning loop in Pattern 09.
- **Reflection Feedback Loop** (Pattern 31): Inference-time self-critique complements training-time RLAIF.

## References
Source: awesome-agentic-patterns — Learning & Adaptation
