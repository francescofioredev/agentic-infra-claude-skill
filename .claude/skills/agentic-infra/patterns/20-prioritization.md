# Pattern 20: Prioritization

## Intent
Dynamically order and re-order agent tasks based on urgency, importance, dependencies, and resource constraints — ensuring the most critical work is done first.

## Context
Use when an agent must manage a backlog of tasks (not just a single linear pipeline), when tasks have different urgency/importance levels, or when new tasks arrive dynamically while others are in progress. Essential for autonomous agents that operate over longer time horizons.

## Forces / Tradeoffs
- **Dynamic re-prioritization vs. stability**: Frequent re-ordering ensures optimal order but can cause task starvation (low-priority tasks never complete). Use aging mechanisms.
- **Priority accuracy**: The priority assignment is only as good as the criteria used — poorly defined priorities lead to wrong ordering.
- **Overhead**: Continuous re-prioritization adds LLM calls. Batch prioritization decisions where possible.

## Solution

### Five prioritization criteria (p. 323):
1. **Urgency**: Time sensitivity — deadline-driven tasks first
2. **Importance**: Impact value — high-impact tasks first
3. **Dependencies**: Tasks that unblock other tasks first
4. **Resource availability**: Tasks whose required resources are available now
5. **Cost/benefit ratio**: Highest ROI tasks first

### Three levels of prioritization (p. 325):
- **Goal-level**: Which high-level objective to pursue
- **Sub-task-level**: Which step within a goal to execute next
- **Action-selection**: Which individual action within a step to take

### Priority labels (P0/P1/P2) (p. 326):
```python
from pydantic import BaseModel
from enum import Enum

class Priority(str, Enum):
    P0 = "P0"  # Critical / blocking
    P1 = "P1"  # High importance
    P2 = "P2"  # Normal / nice-to-have

class Task(BaseModel):
    id: str
    description: str
    priority: Priority
    deadline: datetime | None = None
    depends_on: list[str] = []
    estimated_value: float = 1.0  # ROI proxy
```

**LangChain task manager with dynamic re-prioritization** (p. 327):
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory

# Agent uses ReAct to decide which task to work on next
task_manager_prompt = """
You are a task manager. Current task backlog: {task_list}
Select the highest-priority task considering: urgency, importance, dependencies, ROI.
Explain your prioritization reasoning, then execute the selected task.
"""

task_agent = create_react_agent(llm, tools=[execute_task_tool, update_priority_tool])
executor = AgentExecutor(agent=task_agent, memory=ConversationBufferMemory())
```

**Dynamic re-prioritization trigger** (p. 328): Re-run prioritization when:
- A task completes (its dependents may now be unblocked)
- A new task arrives with high urgency
- Resources become available or constrained
- A deadline approaches

**Key rules:**
1. Always enforce dependency ordering — never start a task before its prerequisites are complete (p. 324).
2. Implement aging: boost priority of long-waiting tasks to prevent starvation (p. 325).
3. Re-prioritize lazily (on task completion or new arrival) rather than continuously — reduce overhead (p. 328).
4. Log every prioritization decision with reasoning — enables post-hoc analysis and improvement (p. 329).

## Variants
- **Static priority queue**: Fixed priority at task creation; no re-ordering.
- **Dynamic re-prioritization**: Re-rank on each task completion event.
- **LLM-based prioritization**: Agent reasons about priority using all five criteria.
- **Rule-based prioritization**: Deadline-driven hard rules (P0 = deadline <1h, P1 = <24h, P2 = >24h).

## Failure Modes
- **Priority inversion**: Lower-priority task blocks a higher-priority one (dependency cycle). Mitigation: dependency graph validation at task creation.
- **Starvation**: P2 tasks never complete because P0/P1 tasks keep arriving. Mitigation: aging (boost priority after N hours in queue).
- **Thrashing**: Constant re-prioritization costs more time than it saves. Mitigation: re-prioritize only on trigger events, not continuously.

## Instrumentation
- Log: task priority at creation, priority changes with timestamps and reasons, task completion times.
- Track: P0/P1/P2 distribution in backlog, mean time in queue per priority level.
- Alert: P0 task in queue >X minutes (SLA breach risk).

## Eval
- Given a task set with known optimal order, verify agent produces correct prioritization.
- Test aging: inject old P2 task; verify it eventually gets promoted.
- Test dependency enforcement: task B cannot start before task A completes.

## Related Patterns
- **Planning** (p. 101): Planning generates the task list; Prioritization orders it.
- **Goal Setting** (p. 183): Goals define the importance dimension of prioritization.
- **Exception Handling** (p. 201): Failed tasks may need to be re-prioritized (or deprioritized) after failure.

## Evidence
- p. 321-329: Prioritization chapter. Five criteria, three levels, P0/P1/P2 framework.
- p. 323: Five criteria: urgency, importance, dependencies, resource availability, cost/benefit.
- p. 325: Three prioritization levels: goal, sub-task, action.
- p. 326: `Task` Pydantic model with P0/P1/P2 priority enum.
- p. 327: LangChain `create_react_agent` + `AgentExecutor` with `ConversationBufferMemory`.
- p. 328: Dynamic re-prioritization triggers.
