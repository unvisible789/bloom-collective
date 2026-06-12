#!/usr/bin/env python3
"""
Bloom Collective - Local Agent (Desktop Control Version)

Supports:
- Terminal commands (CommandCell)
- File operations
- GUI control (mouse + keyboard)
- Basic safety checks
- Improved action inference
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from planning_cell import PlanningCell
    from verification_cell import VerificationCell
    from system_ai_cell import SystemAICell
    from file_system_cell import FileSystemCell
    from command_cell import CommandCell
    from gui_control_cell import GUIControlCell
except ImportError:
    PlanningCell = None
    VerificationCell = None
    SystemAICell = None
    FileSystemCell = None
    CommandCell = None
    GUIControlCell = None


class LocalAgent:
    """Agent with terminal + GUI control capabilities."""

    def __init__(self, verbose: bool = True):
        self.planning = PlanningCell() if PlanningCell else None
        self.verification = VerificationCell() if VerificationCell else None
        self.system_ai = SystemAICell() if SystemAICell else None
        self.file_system = FileSystemCell() if FileSystemCell else None
        self.command = CommandCell() if CommandCell else None
        self.gui = GUIControlCell() if GUIControlCell else None

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
            plan_result = self._safe_call(self.planning, "create_plan", goal)
            result["cycles"].append({"action": "plan", "result": plan_result})

            use_ai = any(word in goal.lower() for word in ["code", "explain", "analyze", "review", "help with", "debug", "refactor"])
            if use_ai and self.system_ai:
                ai_result = self._safe_call(self.system_ai, "delegate_task", goal)
                result["cycles"].append({"action": "system_ai", "result": ai_result})

            executed = 0
            failed = 0

            if plan_result.get("plan"):
                for step in plan_result["plan"].get("steps", []):
                    step_text = step.get("step", "") if isinstance(step, dict) else str(step)
                    step_lower = step_text.lower()

                    step_record = {"step": step_text, "status": "pending"}

                    try:
                        action_result = None
                        action_type = "other"

                        # File system
                        if any(kw in step_lower for kw in ["list", "state", "directory", "files"]):
                            action_result = self._safe_call(self.file_system, "process", {"action": "list", "path": "."})
                            action_type = "file_system"

                        # Terminal commands
                        elif any(kw in step_lower for kw in ["run", "execute", "command", "test", "git", "python", "pytest"]):
                            cmd = self._infer_command_from_step(step_text, goal)
                            action_result = self._safe_call(self.command, "run_command", cmd)
                            action_type = "command"

                        # GUI actions
                        elif any(kw in step_lower for kw in ["click", "type", "move mouse", "press", "screenshot", "gui", "mouse", "keyboard"]):
                            gui_action = self._infer_gui_action(step_text)
                            # Safety check
                            if self._is_gui_action_safe(gui_action):
                                action_result = self._safe_call(self.gui, "process", gui_action)
                            else:
                                action_result = {"status": "blocked", "reason": "Safety check failed"}
                            action_type = "gui"

                        else:
                            action_result = {"status": "simulated"}

                        step_record.update({"action": action_type, "result": action_result})

                        status = action_result.get("status", "unknown") if isinstance(action_result, dict) else "unknown"
                        if status in ["error", "failed", "blocked"]:
                            failed += 1
                        else:
                            executed += 1

                    except Exception as step_error:
                        failed += 1
                        step_record["status"] = "error"
                        step_record["error"] = str(step_error)

                    result["cycles"].append({"action": "step", "result": step_record})

            verify_result = self._safe_call(self.verification, "verify_action", goal, "Goal completed")
            result["cycles"].append({"action": "verify", "result": verify_result})

            result["summary"] = {
                "total_cycles": len(result["cycles"]),
                "steps_executed": executed,
                "steps_failed": failed,
                "used_gui": any(c.get("action") == "gui" for c in result["cycles"]),
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
            }

            result["status"] = "completed" if failed == 0 else "completed_with_errors"
            result["completed_at"] = datetime.now().isoformat()

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))

        self.history.append(result)
        return result

    def _infer_command_from_step(self, step_text: str, goal: str) -> List[str]:
        step_lower = step_text.lower()
        if "test" in step_lower:
            return ["python", "-m", "unittest", "discover", "tests"]
        if "git status" in step_lower:
            return ["git", "status", "--short"]
        return ["echo", step_text]

    def _infer_gui_action(self, step_text: str) -> Dict[str, Any]:
        step_lower = step_text.lower()

        if "click" in step_lower:
            return {"action": "click", "button": "left"}
        if "type" in step_lower or "write" in step_lower:
            return {"action": "type", "text": "Sample text"}
        if "move mouse" in step_lower or "move to" in step_lower:
            return {"action": "move", "x": 600, "y": 400}
        if "screenshot" in step_lower:
            return {"action": "screenshot"}
        if "press" in step_lower:
            return {"action": "press", "key": "enter"}
        return {"action": "screenshot"}

    def _is_gui_action_safe(self, gui_action: Dict[str, Any]) -> bool:
        # Basic safety filter
        action = gui_action.get("action", "")
        if action == "type":
            text = gui_action.get("text", "")
            risky_keywords = ["password", "delete", "rm -rf", "format"]
            if any(kw in text.lower() for kw in risky_keywords):
                return False
        return True

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


if __name__ == "__main__":
    agent = LocalAgent(verbose=True)
    result = agent.execute_goal("Take a screenshot and click")
    print(result)
