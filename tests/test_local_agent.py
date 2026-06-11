#!/usr/bin/env python3
"""
Tests for the runnable local Bloom agent.
"""

import json
import tempfile
import unittest
from pathlib import Path

from local_agent import LocalBloomAgent, ToolPolicy


class FakeRunner:
    def __init__(self):
        self.calls = []

    def __call__(self, command, cwd, timeout):
        self.calls.append({"command": command, "cwd": str(cwd), "timeout": timeout})
        if command == ["python", "-m", "unittest", "discover", "tests"]:
            return {"returncode": 0, "stdout": "Ran 72 tests\nOK", "stderr": ""}
        if command == ["git", "status", "--short"]:
            return {"returncode": 0, "stdout": "", "stderr": ""}
        if command == ["git", "diff", "--stat"]:
            return {"returncode": 0, "stdout": "README.md | 2 +-", "stderr": ""}
        if command == ["git", "log", "--oneline", "-5"]:
            return {"returncode": 0, "stdout": "abc123 latest commit", "stderr": ""}
        return {"returncode": 0, "stdout": "ok", "stderr": ""}


class TestToolPolicy(unittest.TestCase):
    def test_allows_low_risk_repo_commands_for_direct_goal(self):
        policy = ToolPolicy()
        decision = policy.evaluate(
            {"type": "command", "command": ["git", "status", "--short"]},
            direct_goal=True,
        )
        self.assertTrue(decision["allowed"])
        self.assertEqual(decision["risk"], "low")

    def test_blocks_destructive_commands_even_with_direct_goal(self):
        policy = ToolPolicy()
        decision = policy.evaluate(
            {"type": "command", "command": ["rm", "-rf", "memory"]},
            direct_goal=True,
        )
        self.assertFalse(decision["allowed"])
        self.assertIn("destructive", decision["reason"].lower())

    def test_blocks_external_side_effects_without_explicit_confirmation(self):
        policy = ToolPolicy()
        decision = policy.evaluate(
            {"type": "external_post", "destination": "github"},
            direct_goal=True,
        )
        self.assertFalse(decision["allowed"])
        self.assertIn("external", decision["reason"].lower())

    def test_blocks_git_push_even_with_direct_goal(self):
        policy = ToolPolicy()
        decision = policy.evaluate(
            {"type": "command", "command": ["git", "push"]},
            direct_goal=True,
        )
        self.assertFalse(decision["allowed"])
        self.assertIn("allowlist", decision["reason"].lower())


class TestLocalBloomAgent(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_path = Path(self.temp_dir.name)
        (self.repo_path / "tests").mkdir()
        (self.repo_path / "README.md").write_text("# Demo\n", encoding="utf-8")
        self.runner = FakeRunner()
        self.agent = LocalBloomAgent(repo_path=self.repo_path, command_runner=self.runner)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_execute_goal_runs_tests_and_logs_growth_cycle(self):
        result = self.agent.execute_goal("inspect repo and run tests")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["goal"], "inspect repo and run tests")
        self.assertEqual(result["cycles"], result["actions"])
        self.assertEqual(result["errors"], [])
        self.assertIn(["python", "-m", "unittest", "discover", "tests"], [c["command"] for c in self.runner.calls])

        log_path = self.repo_path / "memory" / "growth_cycles.jsonl"
        self.assertTrue(log_path.exists())
        log_entry = json.loads(log_path.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(log_entry["goal"], "inspect repo and run tests")
        self.assertEqual(log_entry["status"], "success")
        self.assertTrue(log_entry["plan"])
        self.assertTrue(log_entry["actions"])
        self.assertIn(str(log_path), result["memory_written"])

    def test_delegation_packet_is_written_for_agent_goal(self):
        result = self.agent.execute_goal("ask grok and gpt to review the architecture")

        self.assertEqual(result["status"], "success")
        packets = sorted((self.repo_path / "memory" / "delegations").glob("*.md"))
        self.assertEqual(len(packets), 1)
        packet = packets[0].read_text(encoding="utf-8")
        self.assertIn("Grok", packet)
        self.assertIn("GPT", packet)
        self.assertIn("review the architecture", packet)
        self.assertEqual(result["delegation_packets"], [str(packets[0])])

    def test_blocked_action_is_logged_and_does_not_run(self):
        result = self.agent.execute_goal("delete everything with rm -rf")

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(self.runner.calls, [])
        self.assertIn("blocked", result["summary"].lower())
        self.assertTrue(result["blocked_actions"])

    def test_repo_path_escape_is_blocked(self):
        with self.assertRaises(PermissionError):
            self.agent._execute_action({"type": "read_file", "path": "../outside.txt"})

    def test_read_goal_reads_repo_file(self):
        result = self.agent.execute_goal("read README.md")

        self.assertEqual(result["status"], "success")
        read_results = [cycle["result"] for cycle in result["cycles"] if cycle["action"]["type"] == "read_file"]
        self.assertEqual(len(read_results), 1)
        self.assertIn("# Demo", read_results[0]["content"])

    def test_git_diff_goal_runs_diff_stat(self):
        result = self.agent.execute_goal("show git diff")

        self.assertEqual(result["status"], "success")
        self.assertIn(["git", "diff", "--stat"], [c["command"] for c in self.runner.calls])

    def test_git_log_goal_runs_recent_log(self):
        result = self.agent.execute_goal("show git log")

        self.assertEqual(result["status"], "success")
        self.assertIn(["git", "log", "--oneline", "-5"], [c["command"] for c in self.runner.calls])


if __name__ == "__main__":
    unittest.main()
