#!/usr/bin/env python3
"""
Bloom Collective - PlanningCell (Improved)

Enhanced with:
- Step dependencies
- Priority levels
- Better structured output
- Support for alternatives
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class PlanningCell(BaseCell):
    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="PlanningCell", epigenetic=epigenetic)
        self._internal_state = {
            "plans_created": 0,
            "last_plan": None,
        }

    @property
    def supported_tasks(self) -> List[str]:
        return ["planning", "plan", "create_plan"]

    def create_plan(self, goal: str, max_steps: int = 6) -> Dict[str, Any]:
        steps = []
        goal_lower = goal.lower()

        # Basic planning logic with dependencies and priorities
        if "file" in goal_lower or "computer" in goal_lower:
            steps = [
                {"id": 1, "step": "Understand current file system state", "priority": 1, "depends_on": []},
                {"id": 2, "step": "Identify needed file operations", "priority": 2, "depends_on": [1]},
                {"id": 3, "step": "Execute file operations safely", "priority": 3, "depends_on": [2]},
                {"id": 4, "step": "Verify results", "priority": 4, "depends_on": [3]},
            ]
        elif "code" in goal_lower or "develop" in goal_lower:
            steps = [
                {"id": 1, "step": "Clarify the coding goal", "priority": 1, "depends_on": []},
                {"id": 2, "step": "Check existing code structure", "priority": 2, "depends_on": [1]},
                {"id": 3, "step": "Propose implementation approach", "priority": 3, "depends_on": [1, 2]},
                {"id": 4, "step": "Delegate to coding assistant if appropriate", "priority": 4, "depends_on": [3]},
                {"id": 5, "step": "Test and verify", "priority": 5, "depends_on": [4]},
            ]
        else:
            steps = [
                {"id": 1, "step": "Clarify the goal", "priority": 1, "depends_on": []},
                {"id": 2, "step": "Gather relevant information", "priority": 2, "depends_on": [1]},
                {"id": 3, "step": "Break into smaller tasks", "priority": 3, "depends_on": [2]},
                {"id": 4, "step": "Execute tasks in order", "priority": 4, "depends_on": [3]},
                {"id": 5, "step": "Review outcome", "priority": 5, "depends_on": [4]},
            ]

        # Limit number of steps
        steps = steps[:max_steps]

        plan = {
            "goal": goal,
            "steps": steps,
            "created_at": datetime.now().isoformat(),
            "status": "proposed",
            "total_steps": len(steps),
        }

        self._internal_state["plans_created"] += 1
        self._internal_state["last_plan"] = plan

        self.log(f"Created plan with {len(steps)} steps for: {goal}")

        return {
            "status": "success",
            "plan": plan,
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "PlanningCell is currently silenced."}

        goal = input_data.get("goal", input_data.get("task", "general goal"))
        max_steps = input_data.get("max_steps", 6)

        return self.create_plan(goal, max_steps)

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
