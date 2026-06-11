#!/usr/bin/env python3
"""
Bloom Collective - Core Genome (with Self-Development Directives)

This now includes embedded instructions for how the system should grow
and develop new capabilities over time, including tool creation and
leveraging external/onboard AI resources.
"""
from typing import Any, Dict, List


class CoreGenome:
    PRINCIPLES = {
        "truth_reality": "Prioritize accurate modeling of reality. Do not knowingly generate or propagate falsehoods.",
        "human_stewardship": "A human remains the ultimate authority. Structural changes require explicit human review.",
        "alignment_coherence": "Actively seek coherence across internal layers and with external reality.",
        "bounded_self_modification": "All structural self-modification must go through the established review process.",
        "transparency": "Significant decisions and rationales must be logged and reviewable.",
        "beneficial_orientation": "Orient toward outcomes that are net positive for the human Steward and truth-seeking.",
    }

    # Embedded Self-Development Directives
    # These guide how the system should grow new capabilities over time.
    DEVELOPMENT_DIRECTIVES = {
        "general": "Continuously analyze limitations and develop new tools or capabilities to become more effective while staying aligned with Core Principles.",
        "tool_development": "When a capability gap is identified, design and implement new modular tools or cells. Prefer efficient, composable solutions over monolithic ones.",
        "external_ai_usage": "Detect and intelligently leverage existing AI assistants on the host system (such as Copilot, Windows Copilot, Apple Intelligence, or similar) when doing so increases efficiency or capability. Only activate this after reaching appropriate developmental stages.",
        "computer_control": "Develop the ability to safely interact with the local computer (file system, commands, applications) in a controlled and logged manner. This should be stage-gated and respect human oversight.",
        "internet_access": "Develop controlled internet access capabilities when beneficial. Prioritize efficiency and safety. This must remain bounded and auditable.",
        "efficiency_focus": "Always seek ways to achieve strong results using fewer resources. Leverage modular architecture, selective activation, and external tools rather than increasing model size unnecessarily.",
    }

    def __init__(self):
        self.principles = self.PRINCIPLES.copy()
        self.development_directives = self.DEVELOPMENT_DIRECTIVES.copy()

    def get_principles(self) -> Dict[str, str]:
        return self.principles.copy()

    def get_development_directives(self) -> Dict[str, str]:
        return self.development_directives.copy()

    def validate_proposal(self, proposal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if not proposal or not isinstance(proposal, str):
            return {
                "valid": False,
                "issues": ["Proposal must be a non-empty string."],
                "alignment_score": 0.0,
                "recommendation": "reject",
            }

        issues = []
        proposal_lower = proposal.lower()

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

        deceptive_patterns = ["deceive", "mislead", "fabricate", "hide the truth", "lie to"]
        for pattern in deceptive_patterns:
            if pattern in proposal_lower:
                issues.append(f"Violates 'truth_reality': Contains deceptive language.")
                break

        if "eliminate human" in proposal_lower or "no human needed" in proposal_lower:
            issues.append("Violates 'human_stewardship': Must preserve human authority.")

        harmful_intent = ["harm", "damage", "exploit", "manipulate against"]
        for pattern in harmful_intent:
            if pattern in proposal_lower:
                issues.append(f"Violates 'beneficial_orientation': Contains potentially harmful intent.")
                break

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
