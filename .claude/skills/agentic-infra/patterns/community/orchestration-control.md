# Community Patterns: Orchestration & Control
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns for coordinating multi-step and multi-agent workflows — from simple sequential chains to complex hierarchical agent networks. This is the largest category (~40 patterns) because orchestration is the central challenge of agentic systems.

**~40 patterns in this category.** For full detail on key patterns, see:
- Pattern 01: Prompt Chaining (`patterns/01-prompt-chaining.md`)
- Pattern 02: Routing (`patterns/02-routing.md`)
- Pattern 03: Parallelization (`patterns/03-parallelization.md`)
- Pattern 06: Planning (`patterns/06-planning.md`)
- Pattern 07: Multi-Agent Collaboration (`patterns/07-multi-agent-collaboration.md`)
- Pattern 23: Plan-Then-Execute Secure (`patterns/23-plan-then-execute-secure.md`)
- Pattern 24: Sub-Agent Spawning (`patterns/24-sub-agent-spawning.md`)
- Pattern 25: Dual LLM (`patterns/25-dual-llm.md`)

---

## Patterns

### Plan-Then-Execute (Security Variant)
**Status**: established
**Problem**: Agents that plan and execute in the same context are vulnerable to prompt injection from environment data.
**Solution**: Formulate an immutable plan from trusted context only; execute against untrusted environment data without allowing data to modify the plan. See Pattern 23 for full detail.
**Tags**: planning, security, injection, separation
**Reference**: See Pattern 23 (`patterns/23-plan-then-execute-secure.md`)

### Sub-Agent Spawning
**Status**: established
**Problem**: Complex tasks benefit from specialized parallel execution but pollute the orchestrator's context.
**Solution**: Orchestrator spawns isolated child agents with scoped context and tool permissions; aggregates structured results. See Pattern 24 for full detail.
**Tags**: spawning, parallelism, delegation, isolation
**Reference**: See Pattern 24 (`patterns/24-sub-agent-spawning.md`)

### Dual LLM Pattern
**Status**: established
**Problem**: Single model handles both trusted reasoning and untrusted data, creating a security boundary failure.
**Solution**: Separate reasoning (privileged model) from execution/extraction (constrained model). See Pattern 25 for full detail.
**Tags**: security, dual-model, separation, injection
**Reference**: See Pattern 25 (`patterns/25-dual-llm.md`)

### Supervisor-Worker Architecture
**Status**: established
**Problem**: Multi-agent systems need a clear coordination structure with defined responsibility boundaries.
**Solution**: A supervisor agent decomposes tasks, assigns sub-tasks to specialized worker agents, monitors progress, and aggregates results. Workers report only to the supervisor, not to each other.
**Tags**: multi-agent, supervisor, hierarchy, coordination
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Event-Driven Agent
**Status**: established
**Problem**: Polling-based agent loops waste compute when there is nothing to do and miss low-latency events.
**Solution**: Agent subscribes to an event bus; reacts to events (new message, file change, API webhook) as they arrive. Agent is idle between events, eliminating busy-waiting.
**Tags**: event-driven, reactive, async, efficiency
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Conditional Branching
**Status**: established
**Problem**: Linear pipelines cannot handle tasks with mutually exclusive paths based on intermediate results.
**Solution**: Agent evaluates an intermediate result and routes to one of several branches. Branch selection is based on structured classification, not free-form LLM judgment, to ensure reliability.
**Tags**: routing, branching, conditional, pipeline
**Reference**: See Pattern 02 Routing (`patterns/02-routing.md`)

### Map-Reduce Agent
**Status**: established
**Problem**: Large datasets or document corpora cannot be processed in a single LLM call.
**Solution**: Map phase: split input into chunks and process each chunk independently (in parallel). Reduce phase: aggregate chunk results into a final output. Classic distributed computing adapted for LLMs.
**Tags**: map-reduce, parallel, chunking, aggregation
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Checkpoint and Resume
**Status**: established
**Problem**: Long-running agents fail midway through a task, requiring full restart.
**Solution**: After each significant step, serialize the agent's state (plan position, partial results, tool call history) to persistent storage. On restart, load the latest checkpoint and resume from that point.
**Tags**: checkpointing, fault-tolerance, long-running, state
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Interrupt and Preemption
**Status**: emerging
**Problem**: Long-running agent tasks block higher-priority work that arrives mid-execution.
**Solution**: Implement an interrupt mechanism that suspends a running agent at the next safe checkpoint; saves state; allows higher-priority task to run; resumes suspended task when the priority queue permits.
**Tags**: preemption, priority, interrupt, scheduling
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Backpressure and Rate Limiting
**Status**: established
**Problem**: Agent networks overwhelm downstream services (APIs, databases) with request bursts.
**Solution**: Implement token-bucket rate limiting on outbound tool calls; queue excess requests; apply backpressure to upstream agents to slow task acceptance when queues fill.
**Tags**: rate-limiting, backpressure, reliability, flow-control
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Saga / Compensating Transactions
**Status**: established
**Problem**: Multi-step agent workflows that partially complete leave the system in an inconsistent state.
**Solution**: For each forward action, define a compensating action (undo operation). If the workflow fails at step N, execute compensating actions for steps N-1, N-2, ... 1 in reverse order.
**Tags**: saga, compensation, rollback, consistency
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Workflow as Code
**Status**: established
**Problem**: Workflows defined in declarative YAML or GUI tools are hard to version, test, and debug.
**Solution**: Define agent workflows as regular code (Python, TypeScript) using a workflow SDK. Leverage normal software engineering practices: version control, unit tests, code review.
**Tags**: workflow, code, testing, maintainability
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Agent Pool
**Status**: established
**Problem**: Unpredictable traffic spikes require over-provisioning agents; under-provisioning causes queue buildup.
**Solution**: Maintain a pool of idle agent instances; dynamically scale up/down based on queue depth and latency SLOs. Reuse warm agent instances for related tasks to amortize initialization cost.
**Tags**: pooling, scaling, efficiency, load-balancing
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Task Dependency Graph
**Status**: established
**Problem**: Complex tasks have dependencies between sub-tasks; a flat list misses the execution order constraints.
**Solution**: Model task dependencies as a directed acyclic graph (DAG); topological sort determines execution order; tasks with no un-met dependencies run in parallel.
**Tags**: DAG, dependencies, scheduling, parallelism
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Dead Letter Queue
**Status**: established
**Problem**: Failed tasks are silently dropped; there is no visibility into what failed and why.
**Solution**: Route all permanently failed tasks to a dead letter queue with full context (input, error, stack trace, attempt count). Operator reviews DLQ regularly; some tasks are retried manually or with modified inputs.
**Tags**: reliability, failure, queue, observability
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Agent Handoff Protocol
**Status**: established
**Problem**: When one agent transfers a task to another, context is lost and the receiving agent duplicates work.
**Solution**: Define a structured handoff document: current state, completed steps, open questions, relevant context, suggested next actions. Receiving agent reviews the handoff document before proceeding.
**Tags**: handoff, multi-agent, context, transfer
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Timeout and Circuit Breaker
**Status**: established
**Problem**: Agent calls to external services or sub-agents may hang indefinitely, blocking the pipeline.
**Solution**: Wrap every external call with a timeout. After N consecutive timeouts, open the circuit breaker (reject calls immediately); after a cooldown period, test with a single probe call; close breaker on success.
**Tags**: timeout, circuit-breaker, resilience, external-calls
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Hierarchical Planning
**Status**: established
**Problem**: Flat task lists become unwieldy for complex tasks with many sub-tasks.
**Solution**: Generate a hierarchical plan: high-level goals → mid-level tasks → atomic actions. Execute bottom-up; report progress bottom-up. Enables re-planning at any level without discarding the full plan.
**Tags**: planning, hierarchy, decomposition, complex-tasks
**Reference**: See Pattern 06 Planning (`patterns/06-planning.md`)

### Speculative Execution
**Status**: emerging
**Problem**: Sequential agent steps waste latency when the output of step N can be speculatively predicted.
**Solution**: Speculatively execute step N+1 based on the most likely output of step N while step N is running; discard if the speculation is wrong; keep if correct. Reduces critical path latency.
**Tags**: speculation, latency, parallelism, efficiency
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control

### Rollback-Safe Operations
**Status**: established
**Problem**: Agents that modify external state cannot safely retry failed operations without side effects.
**Solution**: Make all agent operations idempotent (safe to retry) or implement an explicit rollback: before every state-modifying operation, create a snapshot; on failure, restore the snapshot.
**Tags**: idempotency, rollback, safety, state
**Reference**: Source: awesome-agentic-patterns — Orchestration & Control
