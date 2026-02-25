# Community Patterns: Security & Safety
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns that prevent agents from taking harmful, unauthorized, or unintended actions — covering prompt injection defense, tool authorization, output safety, and access control. Security in agentic systems is fundamentally different from traditional software security because the attack surface includes the LLM's own reasoning process.

**5 patterns in this category.** For full detail on key patterns, see:
- Pattern 18: Guardrails / Safety (`patterns/18-guardrails-safety.md`)
- Pattern 29: Sandboxed Tool Authorization (`patterns/29-sandboxed-authorization.md`)
- Pattern 23: Plan-Then-Execute Secure (`patterns/23-plan-then-execute-secure.md`)
- Pattern 25: Dual LLM (`patterns/25-dual-llm.md`)

---

## Patterns

### Sandboxed Tool Authorization
**Status**: established
**Problem**: Agents with broad tool access can be manipulated to call tools they should not, or call them with unsafe arguments.
**Solution**: Deny-by-default tool authorization with scoped capability tokens; execute all tools in isolated sandboxes. See Pattern 29 for full detail.
**Tags**: authorization, sandbox, least-privilege, security
**Reference**: See Pattern 29 (`patterns/29-sandboxed-authorization.md`)

### Prompt Injection Defense
**Status**: established
**Problem**: Malicious content in the environment (web pages, emails, documents) instructs the agent to ignore its system prompt and take unauthorized actions.
**Solution**: Combine multiple defenses: (1) Plan-Then-Execute Secure (Pattern 23) to separate planning from data processing, (2) Dual LLM (Pattern 25) to prevent untrusted data from reaching the reasoning model, (3) structured extraction to prevent raw untrusted text from being re-prompted, (4) output validation before any consequential action.
**Tags**: injection, defense, security, multi-layer
**Reference**: See Patterns 23 and 25

### Minimal Permission Footprint
**Status**: established
**Problem**: Agents are granted broad permissions at deployment because it is easier than scoping; this creates unnecessary risk.
**Solution**: Audit all tool calls made by the agent in staging; derive the minimal permission set; enforce it in production. Review and re-approve permissions quarterly. Any new permission requires explicit justification.
**Tags**: least-privilege, permissions, audit, security
**Reference**: Source: awesome-agentic-patterns — Security & Safety

### Output Safety Filtering
**Status**: established
**Problem**: Agent outputs may contain harmful, toxic, or policy-violating content before being shown to users or passed to downstream systems.
**Solution**: Apply a safety classifier to all agent outputs before delivery. Block outputs above the safety threshold; route to human review or regenerate. Log all blocked outputs for safety team review.
**Tags**: safety, filtering, content-policy, output
**Reference**: See Pattern 18 Guardrails / Safety (`patterns/18-guardrails-safety.md`)

### Secrets Management
**Status**: established
**Problem**: API keys and credentials are often embedded in agent prompts or context, where they can be exfiltrated.
**Solution**: Never include secrets in LLM context. Inject secrets via runtime environment variables or secret manager references; resolve secrets only at the point of use in tool execution code; the agent receives only an opaque reference (e.g., `SECRET_REF:openai_key`), not the actual value.
**Tags**: secrets, credentials, security, injection
**Reference**: Source: awesome-agentic-patterns — Security & Safety
