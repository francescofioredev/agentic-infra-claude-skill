# Community Patterns: Learning & Adaptation
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns that allow agents to improve their behavior over time — through fine-tuning, in-context learning, experience replay, and self-modification of prompts or strategies. These patterns bridge the gap between a static deployed model and a continuously improving system.

**7 patterns in this category.** For full detail on key patterns, see:
- Pattern 09: Learning & Adaptation (`patterns/09-learning-adaptation.md`)
- Pattern 28: RLAIF (`patterns/28-rlaif.md`)

---

## Patterns

### RLAIF (Reinforcement Learning from AI Feedback)
**Status**: established
**Problem**: Human annotation doesn't scale to production training volumes.
**Solution**: Use LLM judges as reward signals for policy training; validate with human labels. See Pattern 28 for full detail.
**Tags**: RLAIF, RL, training, scale
**Reference**: See Pattern 28 (`patterns/28-rlaif.md`)

### Few-Shot Prompt Adaptation
**Status**: established
**Problem**: A general-purpose prompt performs poorly on a specific user or domain without expensive fine-tuning.
**Solution**: Collect successful (input, output) examples from past interactions; dynamically select the most relevant few-shot examples for each new request and prepend them to the prompt. No model weight update required.
**Tags**: few-shot, in-context-learning, adaptation, prompt
**Reference**: Source: awesome-agentic-patterns — Learning & Adaptation

### Prompt Optimization Loop
**Status**: emerging
**Problem**: System prompts are written once at deployment and never improved despite production evidence of failure cases.
**Solution**: Periodically analyze production failures; automatically generate candidate prompt improvements; A/B test candidates; deploy the winner. Treat prompt optimization as continuous software development.
**Tags**: prompt, optimization, A/B-test, continuous
**Reference**: Source: awesome-agentic-patterns — Learning & Adaptation

### Continual Fine-Tuning
**Status**: emerging
**Problem**: Distribution shift: production inputs drift from the training distribution over time, degrading model performance.
**Solution**: Implement a continual learning pipeline: collect production data, filter for quality, periodically fine-tune on fresh data while monitoring for catastrophic forgetting via evaluation on holdout benchmarks.
**Tags**: fine-tuning, continual-learning, drift, production
**Reference**: Source: awesome-agentic-patterns — Learning & Adaptation

### Experience Replay Buffer
**Status**: established
**Problem**: Online RL training is unstable without a diverse replay buffer; recent experience is over-represented.
**Solution**: Maintain a fixed-size replay buffer of (state, action, reward) tuples sampled from production; train on randomly sampled minibatches from the buffer (not just recent experience) to stabilize training.
**Tags**: RL, replay, training, stability
**Reference**: Source: awesome-agentic-patterns — Learning & Adaptation

### Skill Distillation
**Status**: emerging
**Problem**: A large capable model performs well but is too expensive for production inference; a smaller model is cheaper but weaker.
**Solution**: Use the large model to generate high-quality (input, output) pairs; fine-tune the small model on these pairs (knowledge distillation); deploy the fine-tuned small model for production inference.
**Tags**: distillation, efficiency, fine-tuning, cost
**Reference**: Source: awesome-agentic-patterns — Learning & Adaptation

### Automated Curriculum
**Status**: emerging
**Problem**: Training on random task samples is inefficient; the model wastes time on tasks it has already mastered or tasks beyond its current capability.
**Solution**: Dynamically generate training tasks ordered by difficulty; start with tasks just above current capability; advance curriculum as the model's success rate improves. Use success rate as the curriculum progression signal.
**Tags**: curriculum, training, difficulty, efficiency
**Reference**: Source: awesome-agentic-patterns — Learning & Adaptation
