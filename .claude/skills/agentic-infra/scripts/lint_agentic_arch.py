#!/usr/bin/env python3
"""
lint_agentic_arch.py

Given an ADR markdown file, produces structured findings with severity,
pattern references, and PDF evidence citations.

Usage:
    python3 lint_agentic_arch.py <path/to/adr.md>
    python3 lint_agentic_arch.py <path/to/adr.md> --format json
    python3 lint_agentic_arch.py <path/to/adr.md> --format text

Output (JSON):
{
  "file": "adr.md",
  "summary": {"critical": N, "high": N, "medium": N, "low": N, "total": N},
  "findings": [
    {
      "id": "LINT-001",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "rule": "rule_id",
      "description": "What was checked",
      "finding": "What was found / missing",
      "pattern_ref": "patterns/NN-name.md",
      "evidence_page": N,
      "evidence_quote": "Supporting PDF quote",
      "required_action": "What to do to fix this"
    }
  ]
}

All rules grounded in "Agentic Design Patterns" PDF. Evidence page numbers cited.
"""

import json
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    id: str
    severity: str  # CRITICAL | HIGH | MEDIUM | LOW
    rule: str
    description: str
    finding: str
    pattern_ref: str
    evidence_page: int
    evidence_quote: str
    required_action: str


# ---------------------------------------------------------------------------
# Lint rules
# Each rule is a function: (content: str, context: dict) -> Optional[Finding]
# Returns a Finding if the rule fires, None if the rule passes.
# ---------------------------------------------------------------------------

RULES: list = []

def rule(fn):
    RULES.append(fn)
    return fn


@rule
def check_max_iterations(content: str, ctx: dict) -> Optional[Finding]:
    """CRITICAL: Agent loops must have a max_iterations or max_steps limit."""
    has_loop = any(kw in content.lower() for kw in [
        "loop", "while", "iteration", "cycle", "agent loop", "agentic loop",
        "goals_met", "goal check", "react", "plan-and-execute"
    ])
    has_limit = any(kw in content.lower() for kw in [
        "max_iter", "max_step", "max iteration", "maximum iteration",
        "iteration limit", "step limit", "timeout"
    ])
    if has_loop and not has_limit:
        return Finding(
            id="LINT-001",
            severity="CRITICAL",
            rule="max_iterations_required",
            description="Agent loops require a max_iterations or max_steps limit",
            finding="ADR describes an agent loop but does not define a maximum iteration limit",
            pattern_ref="patterns/11-goal-setting-monitoring.md",
            evidence_page=188,
            evidence_quote="Set max_iterations alongside the goal — prevents infinite loops when goals_met() never returns true",
            required_action="Add max_iterations (or max_steps) parameter to all agent loops; document the value and rationale"
        )
    return None


@rule
def check_goals_met(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: Multi-step agents should have explicit termination criteria."""
    is_multi_step = any(kw in content.lower() for kw in [
        "multi-step", "multi step", "planning", "plan", "pipeline",
        "sequential", "agentic", "autonomous"
    ])
    has_termination = any(kw in content.lower() for kw in [
        "goals_met", "termination", "completion criteria", "done condition",
        "success criteria", "stopping", "exit condition"
    ])
    if is_multi_step and not has_termination:
        return Finding(
            id="LINT-002",
            severity="HIGH",
            rule="termination_criteria_required",
            description="Multi-step agents require explicit termination criteria",
            finding="ADR describes a multi-step agent but does not define explicit completion/termination criteria",
            pattern_ref="patterns/11-goal-setting-monitoring.md",
            evidence_page=185,
            evidence_quote="SMART goals: Specific, Measurable, Achievable, Relevant, Time-bound — all five required for reliable agent termination",
            required_action="Define a goals_met() check or explicit success criteria; include in the ADR"
        )
    return None


@rule
def check_least_privilege(content: str, ctx: dict) -> Optional[Finding]:
    """CRITICAL: Tool access should follow Principle of Least Privilege."""
    has_tools = any(kw in content.lower() for kw in [
        "tool", "function call", "api", "mcp", "capability", "action"
    ])
    has_privilege_mention = any(kw in content.lower() for kw in [
        "least privilege", "minimum permission", "scoped", "read-only",
        "tool restriction", "permission", "access control"
    ])
    if has_tools and not has_privilege_mention:
        return Finding(
            id="LINT-003",
            severity="CRITICAL",
            rule="least_privilege",
            description="Tool access must follow Principle of Least Privilege",
            finding="ADR references tools but does not apply Principle of Least Privilege — no mention of scoping or access restrictions",
            pattern_ref="patterns/18-guardrails-safety.md",
            evidence_page=288,
            evidence_quote="Apply the Principle of Least Privilege: grant agents only the tools they need for the task",
            required_action="Add a Tool Access Matrix to the ADR; justify each tool-agent assignment; separate read/write agents"
        )
    return None


@rule
def check_error_handling(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: Production agents must have error handling strategy."""
    has_production_intent = any(kw in content.lower() for kw in [
        "production", "deploy", "agent", "pipeline", "tool", "api call"
    ])
    has_error_handling = any(kw in content.lower() for kw in [
        "error handling", "exception", "retry", "fallback", "recovery",
        "rollback", "fault tolerance", "resilience", "error triad"
    ])
    if has_production_intent and not has_error_handling:
        return Finding(
            id="LINT-004",
            severity="HIGH",
            rule="error_handling_required",
            description="Production agents require an error handling strategy",
            finding="ADR does not describe error handling, retry logic, or recovery strategies",
            pattern_ref="patterns/12-exception-handling-recovery.md",
            evidence_page=203,
            evidence_quote="The Error Triad: Error Detection → Error Handling → Recovery. All three must be addressed.",
            required_action="Add error handling section covering: error classification, retry strategy, fallback handlers, escalation path"
        )
    return None


@rule
def check_guardrails_layers(content: str, ctx: dict) -> Optional[Finding]:
    """CRITICAL: Agents with user-facing inputs need multi-layer safety."""
    has_user_input = any(kw in content.lower() for kw in [
        "user input", "user query", "user message", "user request",
        "external input", "untrusted input", "customer"
    ])
    has_guardrails = any(kw in content.lower() for kw in [
        "guardrail", "safety", "content filter", "moderation", "validation",
        "sanitiz", "output filter", "input filter", "safety layer"
    ])
    if has_user_input and not has_guardrails:
        return Finding(
            id="LINT-005",
            severity="CRITICAL",
            rule="guardrails_required",
            description="Agents with user-facing inputs require multi-layer safety guardrails",
            finding="ADR describes handling user inputs but does not define safety guardrails",
            pattern_ref="patterns/18-guardrails-safety.md",
            evidence_page=286,
            evidence_quote="Six-layer defense: (1) Input Validation, (2) Output Filtering, (3) Behavioral Constraints, (4) Tool Restrictions, (5) Moderation API, (6) HITL",
            required_action="Define at minimum: input validation, output filtering, and behavioral constraints in the system prompt"
        )
    return None


@rule
def check_eval_defined(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: Agents need evaluation metrics defined before deployment."""
    has_agent = "agent" in content.lower()
    has_eval = any(kw in content.lower() for kw in [
        "evaluat", "metric", "accuracy", "latency", "benchmark",
        "test set", "eval set", "quality", "measurement", "kpi"
    ])
    if has_agent and not has_eval:
        return Finding(
            id="LINT-006",
            severity="HIGH",
            rule="eval_metrics_required",
            description="Agent deployments require evaluation metrics defined before deployment",
            finding="ADR does not define evaluation metrics, eval set, or quality measurement approach",
            pattern_ref="patterns/19-evaluation-monitoring.md",
            evidence_page=303,
            evidence_quote="Define metrics before building the agent — retrofitting metrics is unreliable",
            required_action="Add Evaluation Plan to ADR: define accuracy target, latency target, token budget, and eval method"
        )
    return None


@rule
def check_hitl_triggers(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: Agents with HITL must define explicit escalation triggers."""
    has_hitl = any(kw in content.lower() for kw in [
        "human-in-the-loop", "hitl", "human review", "human approval",
        "escalat", "human oversight", "human intervention"
    ])
    has_triggers = any(kw in content.lower() for kw in [
        "trigger", "escalation condition", "when to escalate",
        "escalate when", "escalation criteria"
    ])
    if has_hitl and not has_triggers:
        return Finding(
            id="LINT-007",
            severity="HIGH",
            rule="hitl_triggers_required",
            description="HITL integration requires explicit escalation triggers",
            finding="ADR mentions HITL but does not define explicit escalation triggers",
            pattern_ref="patterns/13-hitl.md",
            evidence_page=211,
            evidence_quote="Define explicit escalation triggers in the agent's system prompt — don't rely on the agent to infer when to escalate",
            required_action="List all escalation triggers explicitly in the ADR and in the agent system prompt"
        )
    return None


@rule
def check_hitl_timeout(content: str, ctx: dict) -> Optional[Finding]:
    """MEDIUM: HITL escalation must have a timeout with safe default."""
    has_hitl = any(kw in content.lower() for kw in [
        "human-in-the-loop", "hitl", "human review", "human approval", "escalat"
    ])
    has_timeout = any(kw in content.lower() for kw in [
        "timeout", "time limit", "deadline", "safe default", "fallback action"
    ])
    if has_hitl and not has_timeout:
        return Finding(
            id="LINT-008",
            severity="MEDIUM",
            rule="hitl_timeout_required",
            description="HITL escalation requires a timeout with a safe default action",
            finding="HITL is defined but no timeout or safe default action is specified for unresponsive humans",
            pattern_ref="patterns/13-hitl.md",
            evidence_page=214,
            evidence_quote="Implement timeouts on escalation requests — if no human responds within N minutes, use a safe default action or abort",
            required_action="Define timeout duration and safe default action (abort task, return partial result, etc.)"
        )
    return None


@rule
def check_memory_scoping(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: Agents using state/memory must use correct prefix scoping."""
    has_memory = any(kw in content.lower() for kw in [
        "session", "state", "memory", "persist", "cross-session",
        "user preference", "long-term memory", "remember"
    ])
    has_scoping = any(kw in content.lower() for kw in [
        "user:", "app:", "temp:", "session scope", "user scope",
        "memory scope", "state prefix", "ttl"
    ])
    if has_memory and not has_scoping:
        return Finding(
            id="LINT-009",
            severity="HIGH",
            rule="memory_scoping_required",
            description="Agents with state/memory must use correct prefix scoping",
            finding="ADR mentions state/memory but does not define scoping (user:/app:/temp: prefixes or equivalent)",
            pattern_ref="patterns/08-memory-management.md",
            evidence_page=151,
            evidence_quote="Use user: prefix for user-scoped state, app: for app-global, temp: for ephemeral. Mixing scopes causes data leakage between users.",
            required_action="Add Memory Design table to ADR defining scope, storage, and TTL for each data type"
        )
    return None


@rule
def check_rag_hybrid_search(content: str, ctx: dict) -> Optional[Finding]:
    """MEDIUM: RAG implementations should use hybrid search."""
    has_rag = any(kw in content.lower() for kw in [
        "rag", "retrieval-augmented", "vector search", "embedding search",
        "knowledge base", "document retrieval"
    ])
    has_hybrid = any(kw in content.lower() for kw in [
        "hybrid", "bm25", "keyword search", "sparse", "dense + sparse"
    ])
    if has_rag and not has_hybrid:
        return Finding(
            id="LINT-010",
            severity="MEDIUM",
            rule="rag_hybrid_search",
            description="RAG implementations should use hybrid search (BM25 + vector)",
            finding="ADR uses RAG but only mentions vector/embedding search, not hybrid (BM25 + vector)",
            pattern_ref="patterns/14-rag.md",
            evidence_page=222,
            evidence_quote="Hybrid search (BM25 + vector) significantly outperforms either alone for production retrieval",
            required_action="Consider adding BM25 keyword search to augment vector search; use a re-ranker for final results"
        )
    return None


@rule
def check_a2a_agent_card(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: A2A integrations must define Agent Cards."""
    has_a2a = any(kw in content.lower() for kw in [
        "a2a", "agent-to-agent", "inter-agent", "agent communication",
        "agent discovery", "remote agent"
    ])
    has_agent_card = any(kw in content.lower() for kw in [
        "agent card", ".well-known", "agent.json", "agent descriptor"
    ])
    if has_a2a and not has_agent_card:
        return Finding(
            id="LINT-011",
            severity="HIGH",
            rule="a2a_agent_card_required",
            description="A2A integrations require an Agent Card at /.well-known/agent.json",
            finding="ADR describes A2A communication but does not define Agent Cards for discovery",
            pattern_ref="patterns/15-a2a-communication.md",
            evidence_page=243,
            evidence_quote="Every A2A agent must publish an Agent Card at /.well-known/agent.json — this is the discovery mechanism",
            required_action="Define Agent Card JSON structure; specify capabilities, endpoints, and authentication scheme"
        )
    return None


@rule
def check_a2a_security(content: str, ctx: dict) -> Optional[Finding]:
    """CRITICAL: A2A production deployments require mTLS + OAuth2."""
    has_a2a = any(kw in content.lower() for kw in [
        "a2a", "agent-to-agent", "inter-agent communication"
    ])
    has_production = any(kw in content.lower() for kw in [
        "production", "deploy", "external", "cross-service"
    ])
    has_auth = any(kw in content.lower() for kw in [
        "mtls", "oauth", "authentication", "authorization", "tls", "jwt"
    ])
    if has_a2a and has_production and not has_auth:
        return Finding(
            id="LINT-012",
            severity="CRITICAL",
            rule="a2a_security_required",
            description="A2A production deployments require mTLS + OAuth2 authentication",
            finding="A2A communication described for production but no authentication mechanism defined",
            pattern_ref="patterns/15-a2a-communication.md",
            evidence_page=248,
            evidence_quote="Use mTLS (mutual TLS) for transport-layer authentication + OAuth2 bearer tokens for agent-level authorization",
            required_action="Specify mTLS certificate strategy and OAuth2 token flow for all A2A endpoints"
        )
    return None


@rule
def check_multi_agent_contracts(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: Multi-agent systems need defined input/output contracts between agents."""
    has_multi_agent = any(kw in content.lower() for kw in [
        "multi-agent", "sub-agent", "supervisor", "orchestrat", "crew", "agent team"
    ])
    has_contracts = any(kw in content.lower() for kw in [
        "contract", "interface", "schema", "input format", "output format",
        "pydantic", "json schema", "api contract"
    ])
    if has_multi_agent and not has_contracts:
        return Finding(
            id="LINT-013",
            severity="HIGH",
            rule="agent_contracts_required",
            description="Multi-agent systems require defined input/output contracts",
            finding="Multi-agent system described but no contracts defined between agents",
            pattern_ref="patterns/07-multi-agent-collaboration.md",
            evidence_page=126,
            evidence_quote="Define explicit contracts between agents: what input format, what output format",
            required_action="Define input/output schemas (Pydantic models or JSON schemas) for all inter-agent interfaces"
        )
    return None


@rule
def check_tool_injection_risk(content: str, ctx: dict) -> Optional[Finding]:
    """HIGH: Systems using external tool results must treat them as untrusted."""
    has_external_tools = any(kw in content.lower() for kw in [
        "web search", "api call", "external api", "tool result",
        "search result", "database query", "crawl"
    ])
    has_injection_mitigation = any(kw in content.lower() for kw in [
        "untrusted", "sanitize tool", "tool output filter", "injection",
        "prompt injection", "validate tool"
    ])
    if has_external_tools and not has_injection_mitigation:
        return Finding(
            id="LINT-014",
            severity="HIGH",
            rule="tool_injection_risk",
            description="External tool outputs must be treated as potentially adversarial",
            finding="ADR uses external tool calls but does not address prompt injection from tool outputs",
            pattern_ref="patterns/18-guardrails-safety.md",
            evidence_page=289,
            evidence_quote="Never trust tool outputs — treat them as potentially adversarial (prompt injection risk)",
            required_action="Add output filtering/validation for tool results before including in agent context"
        )
    return None


@rule
def check_cost_optimization(content: str, ctx: dict) -> Optional[Finding]:
    """LOW: Consider dynamic model switching for cost optimization."""
    has_cost_mention = any(kw in content.lower() for kw in [
        "cost", "budget", "token", "expense", "scale", "high volume"
    ])
    has_optimization = any(kw in content.lower() for kw in [
        "model switch", "flash", "haiku", "cheap model", "cost optim",
        "token optim", "pruning", "caching", "graceful degrad"
    ])
    if has_cost_mention and not has_optimization:
        return Finding(
            id="LINT-015",
            severity="LOW",
            rule="cost_optimization",
            description="Consider resource-aware optimization for cost management",
            finding="ADR mentions cost concerns but does not describe dynamic model switching or other optimization techniques",
            pattern_ref="patterns/16-resource-aware-optimization.md",
            evidence_page=257,
            evidence_quote="Route simple tasks to Flash/Haiku (fast, cheap); complex tasks to Pro/Opus (high-quality). Use cheap model for routing decision.",
            required_action="Consider adding: dynamic model selection, contextual pruning, response caching"
        )
    return None


@rule
def check_checkpoint_rollback(content: str, ctx: dict) -> Optional[Finding]:
    """MEDIUM: Multi-step tasks with side effects should implement checkpointing."""
    has_side_effects = any(kw in content.lower() for kw in [
        "write", "delete", "send", "update", "create", "modify",
        "side effect", "irreversible", "destructive"
    ])
    has_multi_step = any(kw in content.lower() for kw in [
        "multi-step", "pipeline", "workflow", "sequential", "chain"
    ])
    has_checkpoint = any(kw in content.lower() for kw in [
        "checkpoint", "rollback", "snapshot", "undo", "revert", "state backup"
    ])
    if has_side_effects and has_multi_step and not has_checkpoint:
        return Finding(
            id="LINT-016",
            severity="MEDIUM",
            rule="checkpoint_rollback",
            description="Multi-step tasks with side effects should implement checkpointing",
            finding="ADR describes multi-step workflow with side effects but no checkpoint/rollback mechanism",
            pattern_ref="patterns/12-exception-handling-recovery.md",
            evidence_page=290,
            evidence_quote="Implement checkpoint-and-rollback for multi-step tasks with side effects",
            required_action="Define checkpoint locations (at major milestones) and rollback procedure for each"
        )
    return None


@rule
def check_rag_relevance_threshold(content: str, ctx: dict) -> Optional[Finding]:
    """MEDIUM: RAG should have a relevance threshold to avoid hallucination."""
    has_rag = any(kw in content.lower() for kw in [
        "rag", "retrieval-augmented", "vector search", "embedding search",
        "knowledge base retrieval"
    ])
    has_threshold = any(kw in content.lower() for kw in [
        "threshold", "relevance score", "confidence", "fallback",
        "no result", "knowledge gap"
    ])
    if has_rag and not has_threshold:
        return Finding(
            id="LINT-017",
            severity="MEDIUM",
            rule="rag_relevance_threshold",
            description="RAG should define a relevance threshold to avoid hallucination",
            finding="RAG described but no relevance threshold defined — agent may hallucinate when no relevant chunks found",
            pattern_ref="patterns/14-rag.md",
            evidence_page=225,
            evidence_quote="Set a relevance threshold — if no chunk exceeds the threshold, acknowledge the knowledge gap rather than hallucinating",
            required_action="Define minimum relevance score; specify behavior when no chunks meet threshold (e.g., 'I don't have information on this')"
        )
    return None


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def lint(content: str) -> list[Finding]:
    ctx = {}
    findings = []
    for rule_fn in RULES:
        result = rule_fn(content, ctx)
        if result is not None:
            findings.append(result)
    return findings


def severity_order(s: str) -> int:
    return {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(s, 4)


def main():
    parser = argparse.ArgumentParser(
        description="Lint an agentic architecture ADR markdown file"
    )
    parser.add_argument("adr_file", help="Path to the ADR markdown file")
    parser.add_argument(
        "--format", choices=["json", "text"], default="json",
        help="Output format (default: json)"
    )
    args = parser.parse_args()

    adr_path = Path(args.adr_file)
    if not adr_path.exists():
        print(f"Error: File not found: {adr_path}", file=sys.stderr)
        sys.exit(1)

    content = adr_path.read_text(encoding="utf-8")
    findings = lint(content)
    findings.sort(key=lambda f: severity_order(f.severity))

    summary = {
        "critical": sum(1 for f in findings if f.severity == "CRITICAL"),
        "high": sum(1 for f in findings if f.severity == "HIGH"),
        "medium": sum(1 for f in findings if f.severity == "MEDIUM"),
        "low": sum(1 for f in findings if f.severity == "LOW"),
        "total": len(findings),
    }

    if args.format == "json":
        output = {
            "file": str(adr_path),
            "summary": summary,
            "findings": [asdict(f) for f in findings],
        }
        print(json.dumps(output, indent=2))
    else:
        # Text format
        print(f"\n=== Agentic Architecture Lint: {adr_path} ===\n")
        print(f"Summary: {summary['critical']} CRITICAL | {summary['high']} HIGH | "
              f"{summary['medium']} MEDIUM | {summary['low']} LOW\n")
        for f in findings:
            print(f"[{f.severity}] {f.id} — {f.rule}")
            print(f"  Finding: {f.finding}")
            print(f"  Pattern: {f.pattern_ref}")
            print(f"  Evidence: p. {f.evidence_page} — \"{f.evidence_quote}\"")
            print(f"  Action: {f.required_action}")
            print()

    # Exit code: 1 if any CRITICAL finding, 0 otherwise
    has_critical = summary["critical"] > 0
    sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()
