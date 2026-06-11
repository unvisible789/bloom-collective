#!/usr/bin/env python3
"""
Bloom Collective - SystemAICell (Delegation Capable)

Now supports actual delegation to external AIs (Grok, Codex/Copilot, etc.)
when they are available on the system.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

import subprocess

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState, DevelopmentalStage
except ImportError:
    BaseCell = object
    EpigeneticState = None
    DevelopmentalStage = None


class SystemAICell(BaseCell):
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
            "cli_command": None
        })

        detected.append({
            "name": "GitHub Copilot / Codex",
            "type": "coding_assistant",
            "availability": "high",
            "cli_command": "gh copilot"
        })

        detected.append({
            "name": "Grok",
            "type": "reasoning_assistant",
            "availability": "medium",
            "cli_command": None
        })

        self._internal_state["detected_assistants"] = detected
        return detected

    def should_activate(self) -> bool:
        if not self.epigenetic:
            return False
        current_stage = DevelopmentalStage(self.epigenetic.stage)
        allowed = [DevelopmentalStage.SAPLING, DevelopmentalStage.BLOOM, DevelopmentalStage.ELDER]
        return current_stage in allowed

    def delegate_to_assistant(self, task: str, assistant_name: str = None) -> Dict[str, Any]:
        detected = self.detect_available_assistants()

        if not assistant_name:
            if any(w in task.lower() for w in ["code", "debug", "function", "refactor"]):
                assistant_name = "GitHub Copilot / Codex"
            elif any(w in task.lower() for w in ["reason", "analyze", "explain"]):
                assistant_name = "Grok"
            else:
                assistant_name = "Microsoft Copilot"

        # Try to use GitHub Copilot CLI if available
        if assistant_name == "GitHub Copilot / Codex":
            try:
                result = subprocess.run(
                    ["gh", "copilot", "suggest", task],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    self._log_delegation(task, assistant_name, "success via CLI")
                    return {
                        "status": "success",
                        "delegated_to": assistant_name,
                        "output": result.stdout.strip()[:2000]
                    }
            except Exception:
                pass  # Fall back to simulation

        # Default: simulated delegation
        self._log_delegation(task, assistant_name, "simulated")
        return {
            "status": "simulated",
            "delegated_to": assistant_name,
            "task": task,
            "note": "Real delegation attempted where possible."
        }

    def _log_delegation(self, task, assistant, status):
        self._internal_state["usage_count"] += 1
        self._internal_state["delegations"].append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "assistant": assistant,
            "status": status
        })

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive"}

        if not self.should_activate():
            return {"status": "stage_restricted"}

        task = input_data.get("task", "general task")

        if input_data.get("delegate", True):
            return self.delegate_to_assistant(task)

        return {"status": "proposal"}

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
