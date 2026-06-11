#!/usr/bin/env python3
"""
Bloom Collective - SystemAICell (Improved)

Moving from pure simulation toward real delegation capability.
Currently supports simulation + basic CLI integration where available.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

import subprocess

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class SystemAICell(BaseCell):
    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="SystemAICell", epigenetic=epigenetic)
        self._internal_state = {
            "detected_assistants": [],
            "usage_count": 0,
            "delegations": [],
        }

    @property
    def supported_tasks(self) -> List[str]:
        return ["system_ai", "delegate", "ai_assist"]

    def detect_available_assistants(self) -> List[Dict[str, str]]:
        detected = []

        detected.append({
            "name": "Microsoft Copilot",
            "type": "general_assistant",
            "availability": "high",
        })

        detected.append({
            "name": "GitHub Copilot / Codex",
            "type": "coding_assistant",
            "availability": "high",
            "cli_available": True,
        })

        detected.append({
            "name": "Grok",
            "type": "reasoning_assistant",
            "availability": "medium",
        })

        self._internal_state["detected_assistants"] = detected
        return detected

    def should_activate(self) -> bool:
        if not self.epigenetic:
            return False
        from epigenetic_state import DevelopmentalStage
        current_stage = DevelopmentalStage(self.epigenetic.stage)
        allowed = [DevelopmentalStage.SAPLING, DevelopmentalStage.BLOOM, DevelopmentalStage.ELDER]
        return current_stage in allowed

    def delegate_task(self, task: str, preferred_assistant: str = None) -> Dict[str, Any]:
        detected = self.detect_available_assistants()

        if not preferred_assistant:
            if any(word in task.lower() for word in ["code", "debug", "function", "refactor"]):
                preferred_assistant = "GitHub Copilot / Codex"
            elif any(word in task.lower() for word in ["reason", "analyze", "explain"]):
                preferred_assistant = "Grok"
            else:
                preferred_assistant = "Microsoft Copilot"

        # Try real delegation to GitHub Copilot CLI if available
        if preferred_assistant == "GitHub Copilot / Codex":
            try:
                result = subprocess.run(
                    ["gh", "copilot", "suggest", task],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    self._log_delegation(task, preferred_assistant, "success_via_cli")
                    return {
                        "status": "success",
                        "delegated_to": preferred_assistant,
                        "output": result.stdout.strip()[:2000],
                        "method": "cli",
                    }
            except Exception:
                pass  # Fall back to simulation

        # Default: simulated delegation
        self._log_delegation(task, preferred_assistant, "simulated")
        return {
            "status": "simulated",
            "delegated_to": preferred_assistant,
            "task": task,
            "note": "Real delegation attempted where possible (CLI).",
        }

    def _log_delegation(self, task, assistant, status):
        self._internal_state["usage_count"] += 1
        self._internal_state["delegations"].append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "assistant": assistant,
            "status": status,
        })

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive"}

        if not self.should_activate():
            return {"status": "stage_restricted"}

        task = input_data.get("task", "general task")

        if input_data.get("delegate", True):
            return self.delegate_task(task)

        return {"status": "proposal"}

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
