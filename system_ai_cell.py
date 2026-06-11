#!/usr/bin/env python3
"""
Bloom Collective - SystemAICell (Expanded for Grok, Codex, etc.)

Now detects and can delegate to a wider range of computer/onboard AIs,
including Grok and Codex-style coding assistants.
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
    Expanded cell for tapping into computer/onboard AI assistants
    (Microsoft Copilot, GitHub Copilot / Codex, Grok, etc.).
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

        # General assistants
        detected.append({
            "name": "Microsoft Copilot",
            "type": "general_assistant",
            "availability": "high",
            "strengths": ["general tasks", "web search", "summarization", "reasoning"]
        })

        # Coding assistants
        detected.append({
            "name": "GitHub Copilot / Codex",
            "type": "coding_assistant",
            "availability": "high",
            "strengths": ["code generation", "code explanation", "debugging", "refactoring"]
        })

        # Grok (xAI)
        detected.append({
            "name": "Grok",
            "type": "reasoning_assistant",
            "availability": "medium",
            "strengths": ["reasoning", "coding", "real-time knowledge", "humor"]
        })

        # Future / other possible assistants
        detected.append({
            "name": "Apple Intelligence",
            "type": "general_assistant",
            "availability": "medium",
            "strengths": ["on-device tasks", "writing", "image understanding"]
        })

        self._internal_state["detected_assistants"] = detected
        return detected

    def should_activate(self) -> bool:
        if not self.epigenetic:
            return False

        current_stage = DevelopmentalStage(self.epigenetic.stage)
        allowed_stages = [DevelopmentalStage.SAPLING, DevelopmentalStage.BLOOM, DevelopmentalStage.ELDER]
        return current_stage in allowed_stages

    def delegate_task(self, task: str, preferred_assistant: str = None) -> Dict[str, Any]:
        detected = self.detect_available_assistants()

        if not preferred_assistant:
            # Smart matching
            if any(word in task.lower() for word in ["code", "debug", "refactor", "function"]):
                preferred_assistant = "GitHub Copilot / Codex"
            elif any(word in task.lower() for word in ["reason", "explain", "analyze"]):
                preferred_assistant = "Grok"
            else:
                preferred_assistant = "Microsoft Copilot"

        delegation_record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "assistant": preferred_assistant,
            "status": "delegated (simulated)"
        }

        self._internal_state["delegations"].append(delegation_record)
        self._internal_state["usage_count"] += 1

        self.log(f"Delegated to {preferred_assistant}: {task}")

        return {
            "status": "success",
            "delegated_to": preferred_assistant,
            "task": task,
            "note": "Simulated delegation. Real integration possible in future."
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "SystemAICell is currently silenced."}

        if not self.should_activate():
            return {
                "status": "stage_restricted",
                "message": "Activates at Sapling stage or later.",
                "current_stage": self.epigenetic.stage if self.epigenetic else "unknown"
            }

        task = input_data.get("task", "general assistance")

        if input_data.get("auto_delegate", True):
            result = self.delegate_task(task)
            return result

        # Proposal mode
        detected = self.detect_available_assistants()
        return {
            "status": "proposal",
            "detected_assistants": [a["name"] for a in detected],
            "recommended": self._smart_recommend(detected, task),
        }

    def _smart_recommend(self, detected, task: str):
        task_lower = task.lower()
        if any(word in task_lower for word in ["code", "debug", "function"]):
            return next((a for a in detected if a["type"] == "coding_assistant"), detected[0])
        if any(word in task_lower for word in ["reason", "analyze", "explain"]):
            return next((a for a in detected if a["name"] == "Grok"), detected[0])
        return detected[0]

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
