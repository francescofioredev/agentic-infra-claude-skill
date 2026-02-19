# Pattern 13: Human-in-the-Loop (HITL)

## Intent
Insert human oversight, intervention, and feedback at critical points in agent execution — particularly for high-stakes decisions, ambiguous situations, or unrecoverable errors.

## Context
Use when the agent might take irreversible actions with significant consequences, when confidence is low, when legal/ethical accountability requires human sign-off, or when quality is critical enough to warrant human review. HITL is the safety valve of agentic systems.

## Forces / Tradeoffs
- **Safety vs. throughput**: More HITL checkpoints increase safety but reduce autonomous throughput.
- **Escalation fatigue**: Too-frequent escalation trains humans to rubber-stamp approvals without reading. Design escalation to be rare and meaningful.
- **Async vs. sync escalation**: Synchronous HITL blocks agent execution; async HITL allows the agent to continue other work while waiting.

## Solution
Four HITL interaction modes (p. 210):
1. **Oversight**: Human passively monitors agent actions (read-only, non-blocking).
2. **Intervention**: Human can pause or modify agent execution mid-task.
3. **Escalation**: Agent proactively requests human input when stuck or uncertain.
4. **Feedback**: Human provides post-hoc quality signal that improves future behavior.

**ADK `escalate_to_human` tool** (p. 213):
```python
from google.adk.tools import FunctionTool

def escalate_to_human(reason: str, context: dict) -> str:
    """
    Pause execution and request human input.

    Args:
        reason: Why escalation is needed (e.g., "Ambiguous user intent", "High-stakes action")
        context: Relevant state for the human to review
    """
    # Implementation: write to queue, return approval/rejection + optional guidance
    response = human_review_queue.submit(reason=reason, context=context)
    return response  # "approved", "rejected", or "guidance: ..."

agent = LlmAgent(
    name="careful_agent",
    tools=[escalate_to_human],
    instruction="Use escalate_to_human before taking any irreversible action."
)
```

**Human-on-the-loop variant** (p. 215): Agent executes autonomously but logs all actions to a dashboard; human can interrupt asynchronously. Suitable for lower-stakes tasks.

**Key rules:**
1. Define explicit escalation triggers in the agent's system prompt — don't rely on the agent to infer when to escalate (p. 211).
2. Include full context (task history, current state, proposed action) in every escalation request (p. 213).
3. Log every HITL interaction with timestamp, escalation reason, human response, and outcome (p. 214).
4. Implement timeouts on escalation requests — if no human responds within N minutes, use a safe default action or abort (p. 214).
5. Track escalation frequency — if > X% of tasks escalate, the agent's autonomy boundary is too aggressive (p. 215).

## Variants
- **HITL (blocking)**: Agent pauses and waits for human decision. Highest safety, lowest throughput.
- **Human-on-the-loop**: Agent acts, human can review/interrupt asynchronously. Higher throughput.
- **Approval gate**: Every proposed action requires human approval before execution.
- **Exception-only escalation**: Agent runs autonomously except for defined exception classes.

## Failure Modes
- **Escalation fatigue**: Human approves everything without reading. Mitigation: keep escalation rate low; include clear action summaries.
- **Timeout without safe default**: Human doesn't respond → agent blocks indefinitely. Mitigation: explicit timeout + safe abort action.
- **Missing context**: Human can't make an informed decision without full task context. Mitigation: always include full state in escalation payload.
- **Bypassing HITL**: Agent takes irreversible action without escalating. Mitigation: programmatic gates that require HITL approval token before destructive operations.

## Instrumentation
- Log: escalation triggers, reasons, human response time, human decisions, outcomes.
- Track: escalation rate (target <5% of tasks), median response time, approval/rejection ratio.
- Alert: if escalation rate spikes (> 2× baseline) — indicates agent confidence has dropped.

## Eval
- Test escalation triggers fire for the defined escalation scenarios.
- Test timeout handling — mock a non-responsive human.
- Verify that rejected escalations abort the task cleanly without side effects.

## Related Patterns
- **Exception Handling** (p. 201): HITL is the recovery strategy of last resort.
- **Goal Setting** (p. 183): HITL can clarify ambiguous goals before execution begins.
- **Guardrails** (p. 285): HITL is part of the multi-layered defense strategy.
- **Evaluation** (p. 301): Human feedback from HITL can be used as training signal.

## Evidence
- p. 207-215: HITL chapter. Four interaction modes: Oversight, Intervention, Escalation, Feedback.
- p. 210: Definition of Oversight vs. Intervention vs. Escalation vs. Feedback.
- p. 213: ADK `escalate_to_human` tool implementation.
- p. 215: Human-on-the-loop variant for lower-stakes tasks.
