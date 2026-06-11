#!/usr/bin/env python3
"""
Bloom Collective - PlanningCell (Enhanced)

Improved planning with basic dependency tracking and prioritization.
Supports better long-horizon thinking.
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
        """Declare supported task types for orchestrator routing."""
        return ["planning"]

    def create_plan(self, goal: str, max_steps: int = 6) -> Dict[str, Any]:
        steps = []
        dependencies = {}

        goal_lower = goal.lower()

        if "file" in goal_lower or "computer" in goal_lower:
            steps = [
                {"step": "Understand current file system state", "priority": 1},
                {"step": "Identify needed file operations", "priority": 2},
                {"step": "Execute file operations safely", "priority": 3, "depends_on": [1]},
                {"step": "Verify results", "priority": 4, "depends_on": [3]}
            ]
        elif "code" in goal_lower or "develop" in goal_lower:
            steps = [
                {"step": "Clarify the coding goal", "priority": 1},
                {"step": "Check existing code structure", "priority": 2},
                {"step": "Propose implementation approach", "priority": 3, "depends_on": [1, 2]},
                {"step": "Delegate to coding assistant if appropriate", "priority": 4, "depends_on": [3]},
                {"step": "Test and verify", "priority": 5, "depends_on": [4]}
            ]
        else:
            steps = [
                {"step": "Clarify the goal", "priority": 1},
                {"step": "Gather relevant information", "priority": 2, "depends_on": [1]},
                {"step": "Break into smaller tasks", "priority": 3, "depends_on": [2]},
                {"step": "Execute tasks in order", "priority": 4, "depends_on": [3]},
                {"step": "Review outcome", "priority": 5, "depends_on": [4]}
            ]

        steps = steps[:max_steps]

        plan = {
            "goal": goal,
            "steps": steps,
            "created_at": datetime.now().isoformat(),
            "status": "proposed"
        }

        self._internal_state["plans_created"] += 1
        self._internal_state["last_plan"] = plan

        self.log(f"Created enhanced plan with {len(steps)} steps for: {goal}")

        return {
            "status": "success",
            "plan": plan
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
