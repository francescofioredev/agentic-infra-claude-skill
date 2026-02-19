# Pattern 16: Resource-Aware Optimization

## Intent
Dynamically allocate compute resources (model size, token budget, tool calls) based on task complexity, optimizing the cost-quality tradeoff rather than using a single expensive model for all tasks.

## Context
Use in production agent systems with mixed workloads — some tasks are trivially simple (benefit from cheap/fast models), others are genuinely complex (require expensive/capable models). Uniform model use is either overpaying for simple tasks or underperforming on complex ones.

## Forces / Tradeoffs
- **Classification accuracy**: Misclassifying a complex task as simple produces poor output with a cheap model. Mitigation: err on the side of upclassing.
- **Router cost**: The routing decision itself costs tokens. Keep the router prompt lightweight.
- **Context window constraints**: Large context inputs may force use of models with larger windows regardless of task complexity.

## Solution

### Dynamic Model Switching (p. 257)
Route tasks to the appropriate model tier based on complexity assessment:
```
Simple tasks    → Gemini Flash / Claude Haiku  (fast, cheap)
Complex tasks   → Gemini Pro / Claude Sonnet+  (high-quality)
Critical tasks  → Gemini Ultra / Claude Opus   (maximum capability)
```

**Router Agent pattern** (p. 258) — `BaseAgent` subclass:
```python
class RouterAgent(BaseAgent):
    def classify_complexity(self, task: str) -> str:
        prompt = f"""
        Classify this task complexity: {task}
        Return one of: simple, medium, complex
        Consider: reasoning depth required, domain expertise needed, output length.
        """
        return self.llm_flash.invoke(prompt).content  # Use cheap model for classification

    def route(self, task: str):
        complexity = self.classify_complexity(task)
        if complexity == "simple":
            return self.model_flash.invoke(task)
        elif complexity == "medium":
            return self.model_pro.invoke(task)
        else:
            return self.model_ultra.invoke(task)
```

**Critique Agent** (p. 259): After generation, a lightweight critique agent reviews the output quality. If insufficient, re-runs with a more capable model.

**Seven optimization techniques** (p. 260-272):
1. **Dynamic model switching**: Select model based on task complexity.
2. **Contextual pruning**: Remove irrelevant context before sending to LLM.
3. **Caching**: Cache responses for identical/similar queries.
4. **Batch processing**: Group similar tasks for bulk API calls.
5. **Early stopping**: Stop generation when quality threshold is met.
6. **Graceful degradation**: Return partial results when full computation is too costly (p. 272).
7. **OpenRouter**: Dynamic routing across multiple LLM providers for cost arbitrage (p. 261).

**Key rules:**
1. Use a cheap model (Flash/Haiku) for the routing decision itself — don't use an expensive model to decide to use a cheap one (p. 258).
2. Default to upclassing on ambiguous complexity — cost of poor quality > cost of extra tokens (p. 259).
3. Implement contextual pruning before every LLM call — remove conversation history older than N turns unless explicitly relevant (p. 262).
4. Cache at the semantic level, not just exact-match — use embedding similarity to retrieve cached responses (p. 264).

## Variants
- **Binary routing**: Simple (Flash) vs. Complex (Pro) — no medium tier.
- **Critique-then-escalate**: Generate with cheap model, critique, escalate to expensive model only if quality fails.
- **OpenRouter**: Dynamic routing across cloud providers based on real-time pricing/availability.
- **Graceful degradation**: Return what's computable within budget rather than failing entirely.

## Failure Modes
- **Under-classification**: Complex task routed to cheap model → poor quality output. Mitigation: quality scoring on output; re-route if below threshold.
- **Over-routing overhead**: Too many routing decisions add latency. Mitigation: batch routing decisions.
- **Cache poisoning**: Stale cached response returned for a subtly different query. Mitigation: TTL on cache entries; similarity threshold for cache hit.

## Instrumentation
- Log: model selected per task, routing reason, cost per task, output quality score.
- Track: model distribution (% simple/medium/complex), cost per task type.
- Alert: if quality scores drop for a model tier (model degradation or classification shift).

## Eval
- Compare output quality: cheap model vs. expensive model on same tasks.
- Verify routing decisions match expected complexity classifications on a labeled task set.
- Measure cost savings: routing optimization vs. uniform expensive model baseline.

## Related Patterns
- **Routing** (p. 21): General routing pattern; Resource-Aware Optimization is its cost-focused application.
- **Reflection** (p. 61): Critique Agent is a reflection mechanism used to trigger upclassing.
- **Reasoning Techniques** (p. 261): Chain-of-Draft reduces token count for reasoning steps.

## Evidence
- p. 255-272: Resource-Aware Optimization chapter.
- p. 257: Dynamic model switching: Flash/Haiku for simple, Pro/Sonnet for complex.
- p. 258: RouterAgent as BaseAgent subclass.
- p. 259: Critique Agent for quality-triggered upclassing.
- p. 260-272: Seven optimization techniques including contextual pruning, caching, graceful degradation.
