# Pattern 12: Exception Handling & Recovery

## Intent
Detect failures in agent execution, handle them gracefully with appropriate recovery strategies, and restore the agent to a valid operational state — preventing silent failures and cascading errors.

## Context
Use in any production agent system. Agents interact with unreliable external systems (APIs, databases, tools) and stochastic LLMs that can produce invalid outputs. Without explicit error handling, a single failure can silently corrupt the entire task.

## Forces / Tradeoffs
- **Recovery richness vs. complexity**: Sophisticated recovery (retry + fallback + rollback + escalation) handles more cases but adds code complexity.
- **Retry vs. fail-fast**: Retrying transient errors is valuable, but retrying persistent errors wastes resources.
- **Automatic recovery vs. human escalation**: Some failures are recoverable by the agent; others require human judgment.

## Solution
The **Error Triad** (p. 203):
1. **Error Detection**: Catch all exceptions from tool calls, LLM responses, and validation checks.
2. **Error Handling**: Classify the error and select the appropriate recovery strategy.
3. **Recovery**: Execute the recovery and resume or escalate.

**Recovery strategies by error type** (p. 205):

| Error Type | Strategy |
|-----------|----------|
| Transient (timeout, rate limit) | **Retry with exponential backoff** |
| Invalid LLM output | **Retry with corrective prompt** |
| Missing tool/service | **Fallback to alternative** |
| Data inconsistency | **Rollback to last checkpoint** |
| Unrecoverable | **Escalate to human (HITL)** |

**ADK SequentialAgent with fallback** (p. 208):
```python
from google.adk.agents import SequentialAgent

pipeline = SequentialAgent(
    name="resilient_pipeline",
    sub_agents=[
        primary_handler,    # Tries primary approach
        fallback_handler,   # Runs if primary fails
    ],
)
```

**Checkpoint pattern** (p. 209):
```python
checkpoints = {}

def save_checkpoint(step_id: str, state: dict):
    checkpoints[step_id] = copy.deepcopy(state)

def rollback_to(step_id: str) -> dict:
    return copy.deepcopy(checkpoints[step_id])
```

**Key rules:**
1. Never let exceptions propagate silently — always log with full context (p. 204).
2. Classify errors before choosing recovery: transient vs. permanent vs. logic error (p. 205).
3. Implement checkpoint-and-rollback for multi-step tasks with side effects (p. 209).
4. Set a maximum retry count — prevent infinite retry loops (p. 206).
5. Provide actionable error messages: what failed, why, and what was attempted (p. 207).

## Variants
- **Retry with backoff**: For transient errors (network timeouts, rate limits).
- **Fallback chain**: Primary → secondary → tertiary handler. Used in ADK `SequentialAgent`.
- **Rollback**: Revert state to last known-good checkpoint on data corruption.
- **Graceful degradation**: Return partial results when full completion is impossible (p. 272, Ch 16).
- **Human escalation**: Forward unrecoverable errors to HITL (see pattern 13).

## Failure Modes
- **Silent failure**: Exception caught but not logged → invisible data corruption.
- **Retry storm**: Too-aggressive retries amplify downstream load. Mitigation: exponential backoff + jitter.
- **Checkpoint bloat**: Checkpointing every step consumes excessive memory. Mitigation: checkpoint only at major milestones.
- **Recovery masking**: Successful fallback hides a persistent underlying issue. Mitigation: always alert on primary failure even when fallback succeeds.

## Instrumentation
- Log: all exceptions with step context, error type, recovery strategy attempted, outcome.
- Track: error rate per step/tool, retry count distribution, fallback activation rate.
- Alert: on retry exhaustion (primary + all fallbacks failed).

## Eval
- Inject synthetic failures at each step; verify correct recovery strategy is selected.
- Test that rollback restores state to the correct prior checkpoint.
- Verify retry limits are respected (error after N retries, not infinite).

## Related Patterns
- **Tool Use** (p. 81): Tool execution is the primary source of recoverable exceptions.
- **HITL** (p. 207): Escalation is the final recovery strategy when all automated options are exhausted.
- **Memory Management** (p. 141): Checkpoints are stored in state; rollback requires state management.
- **Goal Setting** (p. 183): After recovery, agent must re-validate that the goal is still achievable.

## Evidence
- p. 201-210: Exception Handling chapter. Error Triad: Detection → Handling → Recovery.
- p. 203: Error classification: transient, invalid output, missing tool, data inconsistency, unrecoverable.
- p. 205: Recovery strategy table by error type.
- p. 208: ADK `SequentialAgent` with `primary_handler` + `fallback_handler`.
- p. 209: Checkpoint-and-rollback implementation.
