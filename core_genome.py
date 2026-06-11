#!/usr/bin/env python3
"""
Bloom Collective - Core Genome (Phase 1 enforcement layer)

Provides programmatic access to the Core Genome principles
and basic validation functions.

This is the first step toward making the Core Genome enforceable in code.
"""
from typing import Any, Dict, List


class CoreGenome:
    """
    Represents the protected Core Genome principles.
    Provides methods to check proposals and changes against invariants.
    """

    PRINCIPLES = {
        "truth_reality": "Prioritize accurate modeling of reality. Do not knowingly generate or propagate falsehoods.",
        "human_stewardship": "A human remains the ultimate authority. Structural changes require explicit human review.",
        "alignment_coherence": "Actively seek coherence across internal layers and with external reality.",
        "bounded_self_modification": "All structural self-modification must go through the established review process. Uncontrolled autonomous self-modification is forbidden.",
        "transparency": "Significant decisions and rationales must be logged and reviewable.",
        "beneficial_orientation": "Orient toward outcomes that are net positive for the human Steward and truth-seeking.",
    }

    def __init__(self):
        self.principles = self.PRINCIPLES.copy()

    def get_principles(self) -> Dict[str, str]:
        return self.principles.copy()

    def validate_proposal(self, proposal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Basic validation of a proposal against Core Genome principles.
        Returns issues found and an overall alignment score.
        """
        issues = []
        proposal_lower = proposal.lower()

        # Check bounded self-modification
        if "autonomous self-modification" in proposal_lower or "without human review" in proposal_lower:
            issues.append("Violates 'bounded_self_modification': Proposals must go through review process.")

        # Check truth/reality orientation
        if any(word in proposal_lower for word in ["deceive", "mislead", "hide truth", "fabricate"]):
            issues.append("Violates 'truth_reality': Must not promote deception or falsehoods.")

        # Check human stewardship
        if "remove human oversight" in proposal_lower or "bypass human" in proposal_lower:
            issues.append("Violates 'human_stewardship': Human authority must be preserved.")

        alignment_score = max(0.0, 1.0 - (len(issues) * 0.35))

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "alignment_score": round(alignment_score, 2),
            "recommendation": "approve" if alignment_score > 0.7 else "revise or reject",
        }

    def get_violation_summary(self, validation_result: Dict[str, Any]) -> str:
        if validation_result["valid"]:
            return "No Core Genome violations detected."
        return "; ".join(validation_result["issues"])
