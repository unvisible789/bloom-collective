#!/usr/bin/env python3
"""
Bloom Collective - Local Agent (with per-step error handling)

Added better error handling at the individual step level.
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

            # External AI
            use_ai = any(word in goal.lower() for word in ["code", "explain", "analyze", "review", "help with"])
            if use_ai and self.system_ai:
                self._log("Consulting external AI...")
                ai_result = self._safe_call(self.system_ai, "delegate_task", goal)
                result["cycles"].append({"action": "system_ai", "result": ai_result})

            # Process steps with per-step error handling
            if plan_result.get("plan"):
                for step in plan_result["plan"].get("steps", []):
                    step_text = step.get("step", "") if isinstance(step, dict) else str(step)
                    step_lower = step_text.lower()

                    try:
                        if "list" in step_lower or "state" in step_lower:
                            self._log(f"Listing directory...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "list", "path": "."})
                            result["cycles"].append({"action": "file_system", "result": fs_result})

                        elif "read" in step_lower:
                            self._log(f"Reading file...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "read", "filename": "README.md"})
                            result["cycles"].append({"action": "file_system", "result": fs_result})

                        elif "write" in step_lower or "create" in step_lower:
                            self._log(f"Writing file...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "write", "filename": "output.txt", "content": "Generated during: {goal}"})
                            result["cycles"].append({"action": "file_system", "result": fs_result})

                        else:
                            result["cycles"].append({"action": "step", "step": step_text, "status": "simulated"})

                    except Exception as step_error:
                        result["errors"].append(f"Step failed: {step_text} - {step_error}")
                        result["cycles"].append({"action": "step", "step": step_text, "status": "failed", "error": str(step_error)})

            # Verification
            self._log("Verifying outcome...")
            verify_result = self._safe_call(self.verification, "verify_action", goal, "Goal completed")
            result["cycles"].append({"action": "verify", "result": verify_result})

            # Summary
            result["summary"] = {
                "total_cycles": len(result["cycles"]),
                "error_count": len(result["errors"]),
                "used_ai": use_ai,
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
            }

            result["status"] = "completed" if len(result["errors"]) == 0 else "completed_with_errors"
            result["completed_at"] = datetime.now().isoformat()
            self._log("Goal execution finished.")

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            self._log(f"Critical error: {e}")

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
    result = agent.execute_goal("List files and create output.txt")
    print("\n=== Execution Complete ===")
    print(f"Status: {result['status']}")
    print(f"Errors: {result['summary'].get('error_count', 0)}")
    print(f"Duration: {result['summary'].get('duration_seconds', 0):.2f}s")
