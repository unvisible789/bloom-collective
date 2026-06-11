#!/usr/bin/env python3
"""
Basic integration test for core cells working together
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


class TestBasicIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.temp_dir, "state.json")
        self.epigenetic = EpigeneticState(state_path=self.state_path)

        # Activate required modules
        for mod in ["reflection", "critic", "memory"]:
            if mod not in self.epigenetic.data.get("active_modules", []):
                self.epigenetic.data["active_modules"].append(mod)

        self.orchestrator = SimpleOrchestrator(epigenetic=self.epigenetic)
        self.orchestrator.register_cell(ReflectionCell(epigenetic=self.epigenetic))
        self.orchestrator.register_cell(CriticCell(epigenetic=self.epigenetic))
        self.orchestrator.register_cell(MemoryCell(epigenetic=self.epigenetic))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_reflect_then_store_then_critique(self):
        # Step 1: Reflect
        reflect_result = self.orchestrator.run_task("reflect", {"observation": "integration test"})
        self.assertIn("ReflectionCell", reflect_result["results"])
        self.assertEqual(reflect_result["results"]["ReflectionCell"]["status"], "success")

        # Step 2: Store memory
        store_result = self.orchestrator.run_task("store", {
            "action": "store",
            "content": {"test": "integration"},
            "tags": ["integration"]
        })
        self.assertIn("MemoryCell", store_result["results"])
        self.assertEqual(store_result["results"]["MemoryCell"]["status"], "success")

        # Step 3: Critique
        critique_result = self.orchestrator.run_task("critique", {
            "observation": "test",
            "proposal": "Small safe improvement"
        })
        self.assertIn("CriticCell", critique_result["results"])
        self.assertEqual(critique_result["results"]["CriticCell"]["status"], "success")


if __name__ == "__main__":
    unittest.main()