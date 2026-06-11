#!/usr/bin/env python3
"""
Bloom Collective - CriticCell
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class CriticCell(BaseCell):
    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="CriticCell", epigenetic=epigenetic)
        self._internal_state = {
            "evaluations_performed": 0,
            "last_evaluation": None,
        }

    @property
    def supported_tasks(self) -> List[str]:
        return ["critique"]

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "CriticCell is currently silenced."}

        precision = 0.75
        risk_tolerance = 0.25
        if self.epigenetic:
            precision = self.epigenetic.get_expression_level("precision")
            risk_tolerance = self.epigenetic.get_expression_level("risk_tolerance")

        observation = input_data.get("observation", "")
        proposal = input_data.get("proposal", "")

        issues = []
        if "uncontrolled self-modification" in str(proposal).lower():
            issues.append("Violates bounded self-modification principle")
        if len(str(proposal)) > 500 and precision > 0.7:
            issues.append("Proposal too long/complex for current precision setting")

        alignment_score = max(0.0, 1.0 - (len(issues) * 0.3))

        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "cell": self.name,
            "precision_used": round(precision, 2),
            "risk_tolerance_used": round(risk_tolerance, 2),
            "issues_found": issues,
            "alignment_score": round(alignment_score, 2),
            "recommendation": "approve" if alignment_score > 0.6 else "revise or reject",
        }

        self._internal_state["evaluations_performed"] += 1
        self._internal_state["last_evaluation"] = evaluation

        self.log(f"Performed critique. Issues: {len(issues)}, Score: {alignment_score:.2f}")

        return {
            "status": "success",
            "evaluation": evaluation,
        }

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base