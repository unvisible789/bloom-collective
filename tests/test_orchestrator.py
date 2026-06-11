#!/usr/bin/env python3
"""
Tests for SimpleOrchestrator
"""
import unittest

from epigenetic_state import EpigeneticState

from reflection_cell import ReflectionCell

from memory_cell import MemoryCell

from orchestrator import SimpleOrchestrator


class TestOrchestrator(unittest.TestCase):

    def setUp(self):
        self.epigenetic = EpigeneticState()
        self.epigenetic.apply_seed_stage_regulation()

        self.orchestrator = SimpleOrchestrator(epigenetic=self.epigenetic)
        self.orchestrator.register_cell(ReflectionCell(epigenetic=self.epigenetic))
        self.orchestrator.register_cell(MemoryCell(epigenetic=self.epigenetic))

    def test_active_cells_in_seed_stage(self):
        active = self.orchestrator.get_active_cells()
        names = [c.name for c in active]
        self.assertIn("ReflectionCell", names)
        self.assertIn("MemoryCell", names)

    def test_run_reflect_task(self):
        result = self.orchestrator.run_task("reflect", {"observation": "Test observation"})
        self.assertIn("results", result)
        self.assertIn("ReflectionCell", result["results"])

    def test_run_store_task(self):
        result = self.orchestrator.run_task("store", {
            "action": "store",
            "content": {"test": "data"},
            "tags": ["test"]
        })
        self.assertIn("results", result)


if __name__ == "__main__":
    unittest.main()
