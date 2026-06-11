#!/usr/bin/env python3
"""
Bloom Collective - SystemAICell (Functional Version)

Now includes basic delegation logic and more actionable proposals.
This moves the cell from pure proposals toward actual capability.
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
    Functional cell for interacting with onboard/system AI assistants.
    Can propose and simulate/prepare delegation of tasks.
    """

    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="SystemAICell", epigenetic=epigenetic)
        self._internal_state = {
            "detected_assistants": [],
            "usage_count": 0,
            "delegations": [],
        }

    def detect_available_assistants(self) -> List[Dict[str, str]]:
        detected = []

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
        if not self.epigenetic:
            return False

        current_stage = DevelopmentalStage(self.epigenetic.stage)
        allowed_stages = [DevelopmentalStage.SAPLING, DevelopmentalStage.BLOOM, DevelopmentalStage.ELDER]
        return current_stage in allowed_stages

    def delegate_task(self, task: str, assistant_name: str = None) -> Dict[str, Any]:
        """
        Attempt to delegate a task to a system AI.
        Currently simulates delegation (can be extended to real calls).
        """
        detected = self.detect_available_assistants()

        if not assistant_name:
            # Auto-select best assistant
            for a in detected:
                if "code" in task.lower() and a["type"] == "coding_assistant":
                    assistant_name = a["name"]
                    break
            if not assistant_name:
                assistant_name = detected[0]["name"] if detected else None

        delegation_record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "assistant": assistant_name,
            "status": "delegated (simulated)"
        }

        self._internal_state["delegations"].append(delegation_record)
        self._internal_state["usage_count"] += 1

        self.log(f"Delegated task to {assistant_name}: {task}")

        return {
            "status": "success",
            "delegated_to": assistant_name,
            "task": task,
            "note": "This is currently simulated. Real delegation can be added."
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "SystemAICell is currently silenced."}

        if not self.should_activate():
            return {
                "status": "stage_restricted",
                "message": "SystemAICell activates at Sapling stage or later.",
                "current_stage": self.epigenetic.stage if self.epigenetic else "unknown"
            }

        task = input_data.get("task", "general assistance")

        # Decide whether to delegate
        if input_data.get("auto_delegate", True):
            result = self.delegate_task(task)
            return result

        # Otherwise just propose
        detected = self.detect_available_assistants()
        best_match = detected[0] if detected else None

        return {
            "status": "proposal",
            "detected_assistants": [a["name"] for a in detected],
            "recommended": best_match,
            "reasoning": "Best match based on task type."
        }

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
