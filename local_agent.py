#!/usr/bin/env python3
"""
Bloom Collective - Local Agent (Enhanced)

Now uses FileSystemCell for real file operations during execution.
"""
from typing import Any, Dict, List, Optional

try:
    from planning_cell import PlanningCell
    from verification_cell import VerificationCell
    from system_ai_cell import SystemAICell
    from file_system_cell import FileSystemCell
except ImportError:
    PlanningCell = None
    VerificationCell = None
    SystemAICell = None
    FileSystemCell = None


class LocalAgent:
    def __init__(self):
        self.planning = PlanningCell() if PlanningCell else None
        self.verification = VerificationCell() if VerificationCell else None
        self.system_ai = SystemAICell() if SystemAICell else None
        self.file_system = FileSystemCell() if FileSystemCell else None

        self.history: List[Dict[str, Any]] = []

    def _safe_call(self, cell, method: str, *args, **kwargs) -> Dict[str, Any]:
        if cell is None:
            return {"status": "unavailable"}
        try:
            func = getattr(cell, method, None)
            if callable(func):
                return func(*args, **kwargs)
            return {"status": "error", "message": f"Method {method} not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def execute_goal(self, goal: str) -> Dict[str, Any]:
        result = {
            "goal": goal,
            "status": "started",
            "cycles": [],
            "errors": [],
        }

        try:
            # Planning
            plan_result = self._safe_call(self.planning, "create_plan", goal)
            result["cycles"].append({"action": "plan", "result": plan_result})

            # Execute using FileSystemCell where possible
            if plan_result.get("plan"):
                for step in plan_result["plan"].get("steps", []):
                    step_text = step.get("step", "") if isinstance(step, dict) else str(step)

                    if "list" in step_text.lower() or "state" in step_text.lower():
                        fs_result = self._safe_call(self.file_system, "process", {"action": "list", "path": "."})
                        result["cycles"].append({"action": "file_system", "result": fs_result})

                    elif "read" in step_text.lower():
                        fs_result = self._safe_call(self.file_system, "process", {"action": "read", "filename": "README.md"})
                        result["cycles"].append({"action": "file_system", "result": fs_result})

                    else:
                        result["cycles"].append({"action": "step", "step": step_text, "status": "simulated"})

            # Verification
            verify_result = self._safe_call(self.verification, "verify_action", goal, "Goal completed")
            result["cycles"].append({"action": "verify", "result": verify_result})

            result["status"] = "completed"

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))

        self.history.append(result)
        return result

    def plan_goal(self, goal: str) -> List[Dict[str, Any]]:
        result = self._safe_call(self.planning, "create_plan", goal)
        if result.get("plan"):
            return result["plan"].get("steps", [])
        return []


if __name__ == "__main__":
    agent = LocalAgent()
    result = agent.execute_goal("List files and read README.md")
    print(result)
