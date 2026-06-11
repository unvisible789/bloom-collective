#!/usr/bin/env python3
"""
Bloom Collective - Local Agent (with execution memory)

Added basic memory of past goal executions.
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
                self._log("Using external AI assistance...")
                ai_result = self._safe_call(self.system_ai, "delegate_task", goal)
                result["cycles"].append({"action": "system_ai", "result": ai_result})

            # Process plan steps
            executed_steps = 0
            failed_steps = 0

            if plan_result.get("plan"):
                for step in plan_result["plan"].get("steps", []):
                    step_text = step.get("step", "") if isinstance(step, dict) else str(step)
                    step_lower = step_text.lower()

                    step_result = {"step": step_text, "status": "pending"}

                    try:
                        if "list" in step_lower or "state" in step_lower:
                            self._log("Listing directory...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "list", "path": "."})
                            step_result.update({"action": "file_system", "result": fs_result, "status": fs_result.get("status", "unknown")})

                        elif "read" in step_lower:
                            self._log("Reading file...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "read", "filename": "README.md"})
                            step_result.update({"action": "file_system", "result": fs_result, "status": fs_result.get("status", "unknown")})

                        elif "write" in step_lower or "create" in step_lower:
                            self._log("Writing file...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "write", "filename": "output.txt", "content": f"Generated for goal: {goal}"})
                            step_result.update({"action": "file_system", "result": fs_result, "status": fs_result.get("status", "unknown")})

                        else:
                            step_result["status"] = "simulated"

                        if step_result.get("status") in ["error", "failed"]:
                            failed_steps += 1
                        else:
                            executed_steps += 1

                    except Exception as step_error:
                        failed_steps += 1
                        step_result["status"] = "error"
                        step_result["error"] = str(step_error)

                    result["cycles"].append({"action": "step", "result": step_result})

            # Verification
            self._log("Verifying...")
            verify_result = self._safe_call(self.verification, "verify_action", goal, "Goal completed")
            result["cycles"].append({"action": "verify", "result": verify_result})

            # Summary
            result["summary"] = {
                "total_cycles": len(result["cycles"]),
                "steps_executed": executed_steps,
                "steps_failed": failed_steps,
                "used_ai": use_ai,
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
            }

            result["status"] = "completed" if failed_steps == 0 else "completed_with_errors"
            result["completed_at"] = datetime.now().isoformat()
            self._log(f"Finished. Success: {executed_steps}, Failed: {failed_steps}")

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

    def get_last_result(self) -> Optional[Dict[str, Any]]:
        return self.history[-1] if self.history else None


if __name__ == "__main__":
    agent = LocalAgent(verbose=True)
    result = agent.execute_goal("List files and create a file")
    print("\n=== Execution Summary ===")
    print(f"Status: {result['status']}")
    print(f"Steps: {result['summary'].get('steps_executed', 0)} executed, {result['summary'].get('steps_failed', 0)} failed")
    print(f"Duration: {result['summary'].get('duration_seconds', 0):.2f}s")
