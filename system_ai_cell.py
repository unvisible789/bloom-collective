#!/usr/bin/env python3
"""
Bloom Collective - SystemAICell (Improved)

Enhanced with better detection logic, stage-aware activation,
and more intelligent decision-making for when to propose using
onboard/system AI assistants.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState, DevelopmentalStage
except ImportError:
    BaseCell = object
    EpigeneticState = None
    DevelopmentalStage = None


class SystemAICell(BaseCell):
    """
    Improved cell for interacting with onboard/system AI assistants.
    Only becomes meaningfully active at later developmental stages.
    """

    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="SystemAICell", epigenetic=epigenetic)
        self._internal_state = {
            "detected_assistants": [],
            "usage_count": 0,
            "last_proposal": None,
        }

    def detect_available_assistants(self) -> List[Dict[str, str]]:
        """
        Detects available system AI assistants.
        In a real environment, this would query the OS for Copilot,
        Apple Intelligence, etc.
        """
        detected = []

        # Simulate detection based on common systems
        detected.append({
            "name": "Microsoft Copilot",
            "type": "general_assistant",
            "availability": "high",
            "strengths": ["general tasks", "web search", "summarization"]
        })

        detected.append({
            "name": "GitHub Copilot",
            "type": "coding_assistant",
            "availability": "medium",
            "strengths": ["code generation", "code explanation", "refactoring"]
        })

        self._internal_state["detected_assistants"] = detected
        return detected

    def should_activate(self) -> bool:
        """Only activate meaningfully at Sapling stage or later."""
        if not self.epigenetic:
            return False

        current_stage = DevelopmentalStage(self.epigenetic.stage)
        allowed_stages = [DevelopmentalStage.SAPLING, DevelopmentalStage.BLOOM, DevelopmentalStage.ELDER]

        return current_stage in allowed_stages

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "SystemAICell is currently silenced."}

        if not self.should_activate():
            return {
                "status": "stage_restricted",
                "message": "SystemAICell only activates at Sapling stage or later.",
                "current_stage": self.epigenetic.stage if self.epigenetic else "unknown"
            }

        task = input_data.get("task", "general task")
        detected = self.detect_available_assistants()

        # Intelligent proposal logic
        best_match = None
        for assistant in detected:
            if "code" in task.lower() and assistant["type"] == "coding_assistant":
                best_match = assistant
                break
            if assistant["type"] == "general_assistant":
                best_match = assistant

        self._internal_state["usage_count"] += 1
        self._internal_state["last_proposal"] = {
            "task": task,
            "recommended_assistant": best_match["name"] if best_match else None,
            "timestamp": datetime.now().isoformat()
        }

        self.log(f"Analyzed task '{task}' - recommending {best_match['name'] if best_match else 'no assistant'}")

        return {
            "status": "success",
            "detected_assistants": [a["name"] for a in detected],
            "recommended": best_match,
            "reasoning": f"Best match for task type based on strengths.",
            "action": "proposal"  # Future: could actually delegate
        }

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
