#!/usr/bin/env python3
"""
Bloom Collective - CommandCell

Safe execution of shell commands.
Designed to be used by the LocalAgent and other cells.
"""

import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class CommandCell(BaseCell):
    """
    Cell responsible for running shell commands safely.
    """

    # Basic allowlist of safe commands (can be expanded later)
    SAFE_COMMANDS = {
        "ls", "pwd", "cat", "head", "tail", "grep", "find",
        "git", "python", "python3", "pip", "pytest", "black",
        "echo", "mkdir", "touch", "rm"  # rm is risky but often needed
    }

    def __init__(self, epigenetic: Optional[EpigeneticState] = None, timeout: int = 30):
        super().__init__(name="CommandCell", epigenetic=epigenetic)
        self.timeout = timeout
        self._internal_state = {
            "commands_run": 0,
            "last_command": None,
        }

    @property
    def supported_tasks(self) -> List[str]:
        return ["command", "run", "execute", "shell", "terminal"]

    def is_command_allowed(self, command: List[str]) -> bool:
        if not command:
            return False
        cmd_name = command[0]
        # Allow common safe commands
        if cmd_name in self.SAFE_COMMANDS:
            return True
        # Allow python module execution
        if cmd_name in ("python", "python3") and len(command) > 1:
            return True
        return False

    def run_command(self, command: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Run a shell command and return structured result.
        """
        if not self.is_command_allowed(command):
            return {
                "status": "blocked",
                "command": command,
                "reason": "Command not in allowlist or considered unsafe",
                "success": False,
            }

        self._internal_state["commands_run"] += 1
        self._internal_state["last_command"] = command

        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )

            success = result.returncode == 0

            return {
                "status": "success" if success else "error",
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "command": command,
                "reason": f"Command timed out after {self.timeout} seconds",
                "success": False,
            }
        except Exception as e:
            return {
                "status": "error",
                "command": command,
                "reason": str(e),
                "success": False,
            }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "CommandCell is currently silenced."}

        command = input_data.get("command")
        if not isinstance(command, list):
            return {
                "status": "error",
                "reason": "'command' must be a list of strings (e.g. ['ls', '-la'])",
            }

        cwd = input_data.get("cwd")
        return self.run_command(command, cwd=cwd)

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
