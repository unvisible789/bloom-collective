#!/usr/bin/env python3
"""
Bloom Collective - Core Genome (Strengthened Validation)

Enhanced with more validation rules and clearer structure.
This makes Core Genome enforcement more robust.
"""
from typing import Any, Dict, List


class CoreGenome:
    """
    Protected Core Genome with strengthened validation.
    """

    PRINCIPLES = {
        "truth_reality": "Prioritize accurate modeling of reality. Do not knowingly generate or propagate falsehoods.",
        "human_stewardship": "A human remains the ultimate authority. Structural changes require explicit human review.",
        "alignment_coherence": "Actively seek coherence across internal layers and with external reality.",
        "bounded_self_modification": "All structural self-modification must go through the established review process.",
        "transparency": "Significant decisions and rationales must be logged and reviewable.",
        "beneficial_orientation": "Orient toward outcomes that are net positive for the human Steward and truth-seeking.",
    }

    def __init__(self):
        self.principles = self.PRINCIPLES.copy()

    def get_principles(self) -> Dict[str, str]:
        return self.principles.copy()

    def validate_proposal(self, proposal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Strengthened validation against Core Genome principles.
        """
        if not proposal or not isinstance(proposal, str):
            return {
                "valid": False,
                "issues": ["Proposal must be a non-empty string."],
                "alignment_score": 0.0,
                "recommendation": "reject",
            }

        issues = []
        proposal_lower = proposal.lower()

        # Rule 1: Bounded Self-Modification
        dangerous_patterns = [
            "autonomous self-modification",
            "without human review",
            "bypass human",
            "remove human oversight",
            "fully autonomous changes",
        ]
        for pattern in dangerous_patterns:
            if pattern in proposal_lower:
                issues.append(f"Violates 'bounded_self_modification': Contains '{pattern}'.")
                break

        # Rule 2: Truth & Reality
        deceptive_patterns = ["deceive", "mislead", "fabricate", "hide the truth", "lie to"]
        for pattern in deceptive_patterns:
            if pattern in proposal_lower:
                issues.append(f"Violates 'truth_reality': Contains deceptive language.")
                break

        # Rule 3: Human Stewardship
        if "eliminate human" in proposal_lower or "no human needed" in proposal_lower:
            issues.append("Violates 'human_stewardship': Must preserve human authority.")

        # Rule 4: Beneficial Orientation (basic check)
        harmful_intent = ["harm", "damage", "exploit", "manipulate against"]
        for pattern in harmful_intent:
            if pattern in proposal_lower:
                issues.append(f"Violates 'beneficial_orientation': Contains potentially harmful intent.")
                break

        # Rule 5: Transparency (warn if proposal suggests hiding things)
        if "secretly" in proposal_lower or "without logging" in proposal_lower:
            issues.append("Warning: Proposal may violate transparency expectations.")

        alignment_score = max(0.0, 1.0 - (len(issues) * 0.3))

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "alignment_score": round(alignment_score, 2),
            "recommendation": "approve" if alignment_score >= 0.7 else "revise or reject",
        }

    def get_violation_summary(self, validation_result: Dict[str, Any]) -> str:
        if validation_result.get("valid"):
            return "No Core Genome violations detected."
        return "; ".join(validation_result.get("issues", []))
