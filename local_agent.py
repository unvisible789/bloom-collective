#!/usr/bin/env python3
"""
Bloom Collective - Local Agent (with execution summary)

Added a simple summary of what happened during goal execution.
"""
from datetime import datetime
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
    def __init__(self, verbose: bool = True):
        self.planning = PlanningCell() if PlanningCell else None
        self.verification = VerificationCell() if VerificationCell else None
        self.system_ai = SystemAICell() if SystemAICell else None
        self.file_system = FileSystemCell() if FileSystemCell else None

        self.history: List[Dict[str, Any]] = []
        self.verbose = verbose

    def _log(self, message: str):
        if self.verbose:
            print(f"[LocalAgent] {message}")

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
        self._log(f"Starting goal: {goal}")
        start_time = datetime.now()

        result = {
            "goal": goal,
            "started_at": start_time.isoformat(),
            "status": "started",
            "cycles": [],
            "errors": [],
            "summary": {},
        }

        try:
            # Planning
            plan_result = self._safe_call(self.planning, "create_plan", goal)
            result["cycles"].append({"action": "plan", "result": plan_result})

            # External AI if needed
            use_ai = any(word in goal.lower() for word in ["code", "explain", "analyze", "review", "help with"])
            if use_ai and self.system_ai:
                self._log("Consulting external AI...")
                ai_result = self._safe_call(self.system_ai, "delegate_task", goal)
                result["cycles"].append({"action": "system_ai", "result": ai_result})

            # File system actions
            if plan_result.get("plan"):
                for step in plan_result["plan"].get("steps", []):
                    step_text = step.get("step", "") if isinstance(step, dict) else str(step)

                    if "list" in step_text.lower():
                        self._log("Listing directory...")
                        fs_result = self._safe_call(self.file_system, "process", {"action": "list", "path": "."})
                        result["cycles"].append({"action": "file_system", "result": fs_result})

                    elif "read" in step_text.lower():
                        self._log("Reading file...")
                        fs_result = self._safe_call(self.file_system, "process", {"action": "read", "filename": "README.md"})
                        result["cycles"].append({"action": "file_system", "result": fs_result})

            # Verification
            self._log("Verifying outcome...")
            verify_result = self._safe_call(self.verification, "verify_action", goal, "Goal completed")
            result["cycles"].append({"action": "verify", "result": verify_result})

            # Build summary
            result["summary"] = {
                "total_cycles": len(result["cycles"]),
                "had_errors": len(result["errors"]) > 0,
                "used_ai": use_ai,
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
            }

            result["status"] = "completed"
            result["completed_at"] = datetime.now().isoformat()
            self._log("Goal completed.")

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            self._log(f"Error: {e}")

        self.history.append(result)
        return result

    def plan_goal(self, goal: str) -> List[Dict[str, Any]]:
        result = self._safe_call(self.planning, "create_plan", goal)
        if result.get("plan"):
            return result["plan"].get("steps", [])
        return []

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history


if __name__ == "__main__":
    agent = LocalAgent(verbose=True)
    result = agent.execute_goal("List files and read README.md")
    print("\n=== Execution Summary ===")
    print(f"Status: {result['status']}")
    print(f"Cycles: {result['summary'].get('total_cycles', 0)}")
    print(f"Used AI: {result['summary'].get('used_ai', False)}")
    print(f"Duration: {result['summary'].get('duration_seconds', 0):.2f}s")
