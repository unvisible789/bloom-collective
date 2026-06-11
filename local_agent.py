#!/usr/bin/env python3
"""
Runnable local Bloom agent runtime.

This module intentionally stays pure Python and conservative. A direct user
goal can authorize low-risk repo-local work, while destructive or external
side-effect actions remain blocked until a higher-level human confirmation
path is added.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


CommandRunner = Callable[[List[str], Path, int], Dict[str, Any]]


class ToolPolicy:
    """Decide whether a planned tool action can run under the current goal."""

    LOW_RISK_COMMANDS = {
        ("git", "status"),
        ("git", "diff"),
        ("git", "log"),
        ("python", "-m", "unittest"),
    }
    DESTRUCTIVE_COMMANDS = {
        "rm",
        "del",
        "erase",
        "rmdir",
        "remove-item",
        "git reset",
        "git clean",
        "format",
    }

    def evaluate(self, action: Dict[str, Any], direct_goal: bool = False) -> Dict[str, Any]:
        action_type = action.get("type")

        if action_type == "command":
            command = [str(part) for part in action.get("command", [])]
            command_text = " ".join(command).lower()
            if any(bad in command_text for bad in self.DESTRUCTIVE_COMMANDS):
                return {
                    "allowed": False,
                    "risk": "high",
                    "reason": "Blocked destructive command.",
                }

            command_key = tuple(command[:3])
            if direct_goal and any(command_key[: len(allowed)] == allowed for allowed in self.LOW_RISK_COMMANDS):
                return {
                    "allowed": True,
                    "risk": "low",
                    "reason": "Low-risk repo-local command allowed by direct goal.",
                }

            return {
                "allowed": False,
                "risk": "medium",
                "reason": "Command is not in the low-risk allowlist.",
            }

        if action_type in {"read_file", "list_files", "write_delegation"}:
            return {
                "allowed": True,
                "risk": "low",
                "reason": "Repo-local action allowed.",
            }

        if action_type in {"external_post", "purchase", "credential_change", "secret_access"}:
            return {
                "allowed": False,
                "risk": "high",
                "reason": "Blocked external side-effect action without explicit confirmation.",
            }

        return {
            "allowed": False,
            "risk": "unknown",
            "reason": f"Unknown action type: {action_type}",
        }


class LocalBloomAgent:
    """Goal-oriented local runner for Bloom Collective."""

    def __init__(
        self,
        repo_path: Optional[Path] = None,
        policy: Optional[ToolPolicy] = None,
        command_runner: Optional[CommandRunner] = None,
    ):
        self.repo_path = Path(repo_path or ".").resolve()
        self.policy = policy or ToolPolicy()
        self.command_runner = command_runner or self._run_command
        self.memory_path = self.repo_path / "memory"
        self.delegation_path = self.memory_path / "delegations"

    def execute_goal(self, goal: str, direct_goal: bool = True) -> Dict[str, Any]:
        """Plan and execute a user-directed goal."""
        goal = goal.strip()
        plan = self.plan_goal(goal)
        actions = []
        errors = []
        blocked_actions = []
        delegation_packets = []
        status = "success"

        for action in plan:
            decision = self.policy.evaluate(action, direct_goal=direct_goal)
            if not decision["allowed"]:
                actions.append({"action": action, "decision": decision, "status": "blocked"})
                blocked_actions.append({"action": action, "reason": decision["reason"]})
                status = "blocked"
                break

            result = self._execute_action(action)
            actions.append({"action": action, "decision": decision, "result": result})
            if action["type"] == "write_delegation" and result.get("path"):
                delegation_packets.append(result["path"])
            if result.get("status") == "error":
                errors.append(result)
                status = "error"
                break

        summary = self._summarize(goal, status, actions)
        log_path = self.memory_path / "growth_cycles.jsonl"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "goal": goal,
            "status": status,
            "plan": plan,
            "actions": actions,
            "cycles": actions,
            "blocked_actions": blocked_actions,
            "delegation_packets": delegation_packets,
            "errors": errors,
            "memory_written": [str(log_path)],
            "summary": summary,
        }
        self._append_jsonl(log_path, entry)
        return entry

    def plan_goal(self, goal: str) -> List[Dict[str, Any]]:
        """Create a small deterministic plan for the first runnable MVP."""
        lowered = goal.lower()

        if any(term in lowered for term in ["rm -rf", "delete everything", "wipe"]):
            return [{"type": "command", "command": ["rm", "-rf", "."], "timeout": 30}]

        if "git diff" in lowered or "show diff" in lowered:
            return [{"type": "command", "command": ["git", "diff", "--stat"], "timeout": 30}]

        if "git log" in lowered or "recent commits" in lowered:
            return [{"type": "command", "command": ["git", "log", "--oneline", "-5"], "timeout": 30}]

        read_target = self._read_target_from_goal(goal)
        if read_target:
            return [{"type": "read_file", "path": read_target}]

        if any(term in lowered for term in ["grok", "gpt", "delegate", "review"]):
            return [
                {"type": "command", "command": ["git", "status", "--short"], "timeout": 30},
                {"type": "write_delegation", "goal": goal, "agents": ["Grok", "GPT"]},
            ]

        if "test" in lowered:
            return [
                {"type": "command", "command": ["git", "status", "--short"], "timeout": 30},
                {"type": "command", "command": ["python", "-m", "unittest", "discover", "tests"], "timeout": 120},
            ]

        if any(term in lowered for term in ["inspect", "repo", "repository"]):
            return [
                {"type": "command", "command": ["git", "status", "--short"], "timeout": 30},
                {"type": "list_files", "path": "."},
            ]

        return [
            {"type": "command", "command": ["git", "status", "--short"], "timeout": 30},
            {"type": "write_delegation", "goal": goal, "agents": ["Grok", "GPT"]},
        ]

    def _read_target_from_goal(self, goal: str) -> Optional[str]:
        words = goal.strip().split()
        if not words or words[0].lower() not in {"read", "show", "open"}:
            return None

        for word in words[1:]:
            cleaned = word.strip("\"'")
            if "." in cleaned or "/" in cleaned or "\\" in cleaned:
                return cleaned
        return None

    def _execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        action_type = action["type"]

        if action_type == "command":
            return self.command_runner(action["command"], self.repo_path, int(action.get("timeout", 60)))

        if action_type == "list_files":
            path = self._resolve_repo_path(action.get("path", "."))
            items = sorted(child.name for child in path.iterdir())
            return {"status": "success", "items": items}

        if action_type == "read_file":
            path = self._resolve_repo_path(action.get("path", ""))
            return {"status": "success", "path": str(path), "content": path.read_text(encoding="utf-8")[:4000]}

        if action_type == "write_delegation":
            packet_path = self._write_delegation_packet(action["goal"], action.get("agents", []))
            return {"status": "success", "path": str(packet_path)}

        return {"status": "error", "message": f"Unhandled action type: {action_type}"}

    def _run_command(self, command: List[str], cwd: Path, timeout: int) -> Dict[str, Any]:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "status": "success" if completed.returncode == 0 else "error",
            "returncode": completed.returncode,
            "stdout": completed.stdout[-4000:],
            "stderr": completed.stderr[-4000:],
        }

    def _resolve_repo_path(self, relative_path: str) -> Path:
        target = (self.repo_path / relative_path).resolve()
        if self.repo_path != target and self.repo_path not in target.parents:
            raise PermissionError(f"Path outside repo blocked: {relative_path}")
        return target

    def _write_delegation_packet(self, goal: str, agents: List[str]) -> Path:
        self.delegation_path.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = self.delegation_path / f"delegation-{stamp}.md"
        agent_line = ", ".join(agents) if agents else "External agent"
        body = (
            f"# Bloom Delegation Packet\n\n"
            f"Created: {datetime.now().isoformat()}\n\n"
            f"Agents: {agent_line}\n\n"
            f"Goal: {goal}\n\n"
            f"Instructions: Review the goal, propose concrete next actions, and avoid broad architecture changes unless requested.\n"
        )
        path.write_text(body, encoding="utf-8")
        return path

    def _append_jsonl(self, path: Path, entry: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")

    def _summarize(self, goal: str, status: str, actions: List[Dict[str, Any]]) -> str:
        if status == "blocked":
            blocked = next((item for item in actions if item.get("status") == "blocked"), {})
            reason = blocked.get("decision", {}).get("reason", "Action blocked.")
            return f"Goal blocked: {reason}"
        if status == "error":
            return f"Goal encountered an error after {len(actions)} action(s)."
        return f"Goal completed with {len(actions)} action(s): {goal}"
