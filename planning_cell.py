#!/usr/bin/env python3
"""
Bloom Collective - PlanningCell

Basic cell for task decomposition and planning.
Helps break down goals into steps and supports longer-horizon thinking.
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
    """
    Cell responsible for breaking down goals into actionable steps
    and supporting longer-term planning.
    """

    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="PlanningCell", epigenetic=epigenetic)
        self._internal_state = {
            "plans_created": 0,
            "last_plan": None,
        }

    def create_plan(self, goal: str, max_steps: int = 5) -> Dict[str, Any]:
        """
        Break down a goal into a simple step-by-step plan.
        """
        steps = []

        # Very basic heuristic planning (can be greatly improved later)
        if "file" in goal.lower() or "computer" in goal.lower():
            steps = [
                "Understand the current file system state",
                "Identify needed file operations",
                "Execute file operations safely",
                "Verify the result"
            ]
        elif "code" in goal.lower() or "develop" in goal.lower():
            steps = [
                "Clarify the coding goal",
                "Check existing code structure",
                "Propose implementation approach",
                "Delegate to coding assistant if needed",
                "Test and verify"
            ]
        else:
            steps = [
                "Clarify the goal",
                "Gather relevant information",
                "Break into smaller tasks",
                "Execute tasks in order",
                "Review outcome"
            ]

        # Limit number of steps
        steps = steps[:max_steps]

        plan = {
            "goal": goal,
            "steps": steps,
            "created_at": datetime.now().isoformat(),
            "status": "proposed"
        }

        self._internal_state["plans_created"] += 1
        self._internal_state["last_plan"] = plan

        self.log(f"Created plan with {len(steps)} steps for: {goal}")

        return {
            "status": "success",
            "plan": plan
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "PlanningCell is currently silenced."}

        goal = input_data.get("goal", input_data.get("task", "general goal"))
        max_steps = input_data.get("max_steps", 5)

        return self.create_plan(goal, max_steps)

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
