"""SIMS Writer Product 1.0 audit core.
Quality audit always precedes SEO changes and all outputs share one RuntimeState.
"""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class RuntimeState:
    input_data: dict[str, Any]
    quality_decision: str = "proceed"
    change_scope: str = "targeted"
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: dict[str, str] = field(default_factory=dict)
    article_output: dict[str, Any] = field(default_factory=dict)
    feedback_json: dict[str, Any] = field(default_factory=dict)


def evidence_verification(state: RuntimeState) -> RuntimeState:
    claims = state.input_data.get("claims", [])
    for i, claim in enumerate(claims):
        text = claim.get("text", "")
        source = claim.get("source")
        state.evidence[str(i)] = "verified" if text and source else "unverified"
        if text and not source:
            state.warnings.append("EVIDENCE_SOURCE_MISSING")
    return state


def quality_gate(state: RuntimeState) -> RuntimeState:
    critical = state.input_data.get("critical_assumption_error", False)
    if critical:
        state.quality_decision = "stop_and_rewrite"
        state.change_scope = "full_rewrite"
        state.reasons.append("QG_CRITICAL_ASSUMPTION_ERROR")
    elif state.warnings:
        state.quality_decision = "proceed_with_warnings"
        state.change_scope = "targeted"
    return state


def consistency_audit(state: RuntimeState) -> RuntimeState:
    title = state.input_data.get("seo_title", "")
    body_topic = state.input_data.get("body_topic", "")
    if title and body_topic and body_topic.lower() not in title.lower():
        state.warnings.append("CONSISTENCY_TITLE_TOPIC_MISMATCH")
    return state


def build_outputs(state: RuntimeState) -> RuntimeState:
    """Generate human and machine outputs from the same immutable decision state."""
    state.article_output = {
        "decision": state.quality_decision,
        "change_scope": state.change_scope,
        "content": state.input_data.get("proposed_content", ""),
    }
    state.feedback_json = {
        "format": "SIMS_FEEDBACK",
        "version": "2.1",
        "runtime_state_id": state.input_data.get("runtime_state_id", "local"),
        "decision": state.quality_decision,
        "change_scope": state.change_scope,
        "reason_codes": state.reasons,
        "warning_codes": state.warnings,
        "changes": state.input_data.get("changes", {}),
    }
    return state


def run_audit(input_data: dict[str, Any]) -> RuntimeState:
    state = RuntimeState(input_data=input_data)
    evidence_verification(state)
    consistency_audit(state)
    quality_gate(state)
    return build_outputs(state)
