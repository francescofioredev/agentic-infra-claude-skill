# Community Patterns: UX & Collaboration
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns for designing the human-agent interaction layer — how agents communicate intent, seek clarification, present options, adjust their level of autonomy, and collaborate with humans as a team. UX patterns determine whether users trust and adopt agentic systems.

**15 patterns in this category.** For full detail on key patterns, see:
- Pattern 13: Human-in-the-Loop (HITL) (`patterns/13-hitl.md`)
- Pattern 26: Spectrum of Control (`patterns/26-spectrum-of-control.md`)
- Pattern 24: Sub-Agent Spawning (`patterns/24-sub-agent-spawning.md`)

---

## Patterns

### Spectrum of Control / Blended Initiative
**Status**: established
**Problem**: Binary human/agent control is too restrictive for routine tasks and too permissive for high-stakes actions.
**Solution**: Five-level autonomy dial from fully manual to fully autonomous; hard floors for irreversible actions; dynamic escalation based on agent confidence. See Pattern 26 for full detail.
**Tags**: autonomy, control, UX, human-agent
**Reference**: See Pattern 26 (`patterns/26-spectrum-of-control.md`)

### Progressive Disclosure
**Status**: established
**Problem**: Agents that expose all information at once overwhelm users; minimal agents leave users in the dark.
**Solution**: Show a concise summary by default; provide a "show reasoning" toggle to reveal intermediate steps; provide a "show full trace" for expert debugging. Match information depth to user expertise.
**Tags**: UX, disclosure, transparency, progressive
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Proactive Clarification
**Status**: established
**Problem**: Agent proceeds with ambiguous instructions and produces a result the user did not want, wasting time.
**Solution**: Before starting, identify ambiguities in the task; ask a small set of clarifying questions (≤3); use the answers to produce a more precise plan. Do not ask about trivial details.
**Tags**: clarification, disambiguation, UX, upfront
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Transparent Reasoning
**Status**: established
**Problem**: Users do not understand why the agent made a particular decision, eroding trust.
**Solution**: After completing a task, present a brief explanation of the key decision points: "I chose X because Y; I rejected Z because W." Make the agent's reasoning legible without being verbose.
**Tags**: transparency, explainability, trust, UX
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Undo / Rollback Interface
**Status**: established
**Problem**: Users need a way to reverse agent actions without technical knowledge of what was changed.
**Solution**: For every consequential action, create a corresponding undo record. Expose an "Undo last action" button in the UI. Maintain an undo stack for the session. Clear undo stack on session end or explicit confirmation.
**Tags**: undo, rollback, UX, safety
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Confidence Communication
**Status**: established
**Problem**: Agent presents uncertain outputs with the same confidence as certain ones, misleading users.
**Solution**: Communicate uncertainty explicitly: "I'm confident about X, but I'm not sure about Y — you may want to verify." Use natural language rather than probability numbers for general users. Reserve probability for expert interfaces.
**Tags**: confidence, uncertainty, communication, trust
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Action Preview
**Status**: established
**Problem**: Users approve agent actions without fully understanding their consequences.
**Solution**: Before executing a consequential action, show a preview: what will change, what is reversible, what is not. Require explicit confirmation. Use plain language, not technical descriptions.
**Tags**: preview, confirmation, transparency, UX
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Progress Streaming
**Status**: established
**Problem**: Long-running agent tasks show nothing until completion, leaving users uncertain whether anything is happening.
**Solution**: Stream intermediate outputs and status updates as the agent works: current step, partial results, estimated remaining steps. Users can interrupt at any point.
**Tags**: streaming, progress, UX, long-running
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Escalation with Context
**Status**: established
**Problem**: When agents escalate to humans, they provide insufficient context; humans must re-investigate from scratch.
**Solution**: Escalation messages include: what the agent tried, why it failed, what information is needed from the human, and a recommendation for resolution. Human should be able to act immediately.
**Tags**: escalation, HITL, context, handoff
**Reference**: See Pattern 13 HITL (`patterns/13-hitl.md`)

### User Preference Learning
**Status**: emerging
**Problem**: Agent behaves the same way for all users, ignoring individual preferences for verbosity, format, and level of detail.
**Solution**: Track user feedback signals (corrections, explicit preferences, interaction patterns); update a user preference profile; personalize agent behavior (output format, detail level, confirmation thresholds) based on the profile.
**Tags**: personalization, preferences, UX, adaptation
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Collaborative Editing
**Status**: established
**Problem**: Agent produces a full document/code output; user wants to iteratively refine it with the agent's help.
**Solution**: Implement a collaborative editing interface: agent produces initial draft; user marks sections for revision; agent revises only those sections; user accepts or rejects each change.
**Tags**: collaboration, editing, iterative, UX
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Task Decomposition Transparency
**Status**: established
**Problem**: Users don't know what the agent is planning to do before it starts doing it.
**Solution**: After receiving a task, present the decomposed plan (subtasks, order, tools to be used) to the user before execution. Allow the user to edit the plan or approve it. This is the UX companion to Pattern 06 Planning.
**Tags**: planning, transparency, UX, approval
**Reference**: See Pattern 06 Planning (`patterns/06-planning.md`)

### Graceful Uncertainty Handling
**Status**: established
**Problem**: Agent refuses to act on any ambiguity, becoming unhelpfully cautious, or acts on all ambiguities, becoming recklessly confident.
**Solution**: Implement a three-tier response to uncertainty: (1) high confidence → act; (2) medium confidence → act but flag assumption; (3) low confidence → ask before acting. Calibrate thresholds per task type.
**Tags**: uncertainty, confidence, UX, calibration
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Multi-Turn Conversation Design
**Status**: established
**Problem**: Agent responses designed for single-turn use create awkward multi-turn conversations — too verbose, wrong format, missing context continuity.
**Solution**: Design conversation patterns explicitly: acknowledge previous turn, address the specific new request, invite continuation. Adjust verbosity based on turn number (first turn: full explanation; subsequent turns: concise).
**Tags**: conversation, multi-turn, UX, design
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration

### Human Override Pattern
**Status**: established
**Problem**: Agent cannot be stopped or corrected mid-execution; once started, it runs to completion regardless of user intent.
**Solution**: Implement a hard override: user can send a "stop" signal at any point; agent cleanly halts at the next safe checkpoint; returns current state and a summary of what was completed.
**Tags**: override, stop, safety, control
**Reference**: Source: awesome-agentic-patterns — UX & Collaboration
