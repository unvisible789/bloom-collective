#!/usr/bin/env python3
"""
Bloom Collective - Local Agent (Polished Version)

Integrates CommandCell for real command execution.
Improved error handling, step tracking, and robustness.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from planning_cell import PlanningCell
    from verification_cell import VerificationCell
    from system_ai_cell import SystemAICell
    from file_system_cell import FileSystemCell
    from command_cell import CommandCell
except ImportError:
    PlanningCell = None
    VerificationCell = None
    SystemAICell = None
    FileSystemCell = None
    CommandCell = None


class LocalAgent:
    """Local goal execution agent with command execution support."""

    def __init__(self, verbose: bool = True):
        self.planning = PlanningCell() if PlanningCell else None
        self.verification = VerificationCell() if VerificationCell else None
        self.system_ai = SystemAICell() if SystemAICell else None
        self.file_system = FileSystemCell() if FileSystemCell else None
        self.command = CommandCell() if CommandCell else None

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
            # Step 1: Planning
            plan_result = self._safe_call(self.planning, "create_plan", goal)
            result["cycles"].append({"action": "plan", "result": plan_result})

            # Step 2: External AI if needed
            use_ai = any(word in goal.lower() for word in ["code", "explain", "analyze", "review", "help with", "debug", "refactor"])
            if use_ai and self.system_ai:
                self._log("Using external AI assistance...")
                ai_result = self._safe_call(self.system_ai, "delegate_task", goal)
                result["cycles"].append({"action": "system_ai", "result": ai_result})

            # Step 3: Execute plan steps
            executed = 0
            failed = 0

            if plan_result.get("plan"):
                for step in plan_result["plan"].get("steps", []):
                    step_text = step.get("step", "") if isinstance(step, dict) else str(step)
                    step_lower = step_text.lower()

                    step_record = {"step": step_text, "status": "pending"}

                    try:
                        # File system operations
                        if any(kw in step_lower for kw in ["list", "state", "directory", "files"]):
                            self._log("Listing directory...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "list", "path": "."})
                            step_record.update({"action": "file_system", "result": fs_result, "status": fs_result.get("status", "unknown")})

                        elif any(kw in step_lower for kw in ["read", "open", "show"]):
                            self._log("Reading file...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "read", "filename": "README.md"})
                            step_record.update({"action": "file_system", "result": fs_result, "status": fs_result.get("status", "unknown")})

                        elif any(kw in step_lower for kw in ["write", "create", "generate"]):
                            self._log("Writing file...")
                            fs_result = self._safe_call(self.file_system, "process", {"action": "write", "filename": "output.txt", "content": f"Generated for: {goal}"})
                            step_record.update({"action": "file_system", "result": fs_result, "status": fs_result.get("status", "unknown")})

                        # Command execution (new)
                        elif any(kw in step_lower for kw in ["run", "execute", "command", "test", "git", "python", "pytest"]):
                            self._log(f"Running command for: {step_text}")
                            # Extract a reasonable command from the step text
                            cmd = self._infer_command_from_step(step_text, goal)
                            cmd_result = self._safe_call(self.command, "run_command", cmd)
                            step_record.update({"action": "command", "result": cmd_result, "status": cmd_result.get("status", "unknown")})

                        else:
                            step_record["status"] = "simulated"

                        if step_record.get("status") in ["error", "failed", "blocked", "timeout"]:
                            failed += 1
                        else:
                            executed += 1

                    except Exception as step_error:
                        failed += 1
                        step_record["status"] = "error"
                        step_record["error"] = str(step_error)

                    result["cycles"].append({"action": "step", "result": step_record})

            # Step 4: Verification
            self._log("Verifying outcome...")
            verify_result = self._safe_call(self.verification, "verify_action", goal, "Goal completed")
            result["cycles"].append({"action": "verify", "result": verify_result})

            # Summary
            result["summary"] = {
                "total_cycles": len(result["cycles"]),
                "steps_executed": executed,
                "steps_failed": failed,
                "used_ai": use_ai,
                "used_commands": any(c.get("action") == "command" for c in result["cycles"]),
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
            }

            result["status"] = "completed" if failed == 0 else "completed_with_errors"
            result["completed_at"] = datetime.now().isoformat()
            self._log(f"Finished. Success: {executed}, Failed: {failed}")

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            self._log(f"Critical error: {e}")

        self.history.append(result)
        return result

    def _infer_command_from_step(self, step_text: str, goal: str) -> List[str]:
        """Simple heuristic to turn a plan step into a runnable command."""
        step_lower = step_text.lower()

        if "test" in step_lower or "pytest" in step_lower:
            return ["python", "-m", "unittest", "discover", "tests"]
        if "git status" in step_lower or "check git" in step_lower:
            return ["git", "status", "--short"]
        if "git diff" in step_lower:
            return ["git", "diff", "--stat"]
        if "run tests" in step_lower:
            return ["python", "-m", "unittest", "discover", "tests"]
        if "list files" in step_lower:
            return ["ls", "-la"]
        # Default fallback
        return ["echo", f"Would run: {step_text}"]

    def plan_goal(self, goal: str) -> List[Dict[str, Any]]:
        result = self._safe_call(self.planning, "create_plan", goal)
        if result.get("plan"):
            return result["plan"].get("steps", [])
        return []

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def get_last_summary(self) -> Dict[str, Any]:
        if not self.history:
            return {}
        return self.history[-1].get("summary", {})

    def get_last_human_summary(self) -> str:
        if not self.history:
            return "No executions yet."

        last = self.history[-1]
        summary = last.get("summary", {})

        lines = [
            f"Goal: {last.get('goal', 'Unknown')}",
            f"Status: {last.get('status', 'Unknown')}",
            f"Steps executed: {summary.get('steps_executed', 0)}",
            f"Steps failed: {summary.get('steps_failed', 0)}",
            f"Used external AI: {summary.get('used_ai', False)}",
            f"Used commands: {summary.get('used_commands', False)}",
            f"Duration: {summary.get('duration_seconds', 0):.2f} seconds",
        ]
        return "\n".join(lines)


if __name__ == "__main__":
    agent = LocalAgent(verbose=True)
    result = agent.execute_goal("List files and run tests")
    print("\n=== Human Readable Summary ===")
    print(agent.get_last_human_summary())
