#!/usr/bin/env python3
"""
Tests for SimpleOrchestrator routing behavior (existing behavior only)
"""

import unittest
import tempfile
import os
import shutil

from epigenetic_state import EpigeneticState
from orchestrator import SimpleOrchestrator
from reflection_cell import ReflectionCell
from critic_cell import CriticCell
from memory_cell import MemoryCell


class TestOrchestratorRouting(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.temp_dir, "state.json")
        self.epigenetic = EpigeneticState(state_path=self.state_path)
        # Ensure required modules are active
        for mod in ["reflection", "critic", "memory"]:
            if mod not in self.epigenetic.data.get("active_modules", []):
                self.epigenetic.data["active_modules"].append(mod)

        self.orchestrator = SimpleOrchestrator(epigenetic=self.epigenetic)
        self.orchestrator.register_cell(ReflectionCell(epigenetic=self.epigenetic))
        self.orchestrator.register_cell(CriticCell(epigenetic=self.epigenetic))
        self.orchestrator.register_cell(MemoryCell(epigenetic=self.epigenetic))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_reflect_only_goes_to_reflection_cell(self):
        result = self.orchestrator.run_task("reflect", {"observation": "test"})
        self.assertIn("ReflectionCell", result["results"])
        self.assertNotIn("CriticCell", result["results"])
        self.assertNotIn("MemoryCell", result["results"])

    def test_critique_only_goes_to_critic_cell(self):
        result = self.orchestrator.run_task("critique", {"observation": "test", "proposal": "test proposal"})
        self.assertIn("CriticCell", result["results"])
        self.assertNotIn("ReflectionCell", result["results"])
        self.assertNotIn("MemoryCell", result["results"])

    def test_store_only_goes_to_memory_cell(self):
        result = self.orchestrator.run_task("store", {"action": "store", "content": {}})
        self.assertIn("MemoryCell", result["results"])
        self.assertNotIn("ReflectionCell", result["results"])
        self.assertNotIn("CriticCell", result["results"])

    def test_unsupported_task_does_not_broadcast(self):
        result = self.orchestrator.run_task("unknown_task_xyz", {"data": "test"})
        # Should not send to any cell
        self.assertEqual(len(result["results"]), 0)


if __name__ == "__main__":
    unittest.main()