#!/usr/bin/env python3
"""
Basic tests for cells
"""
import unittest

from epigenetic_state import EpigeneticState

from reflection_cell import ReflectionCell

from critic_cell import CriticCell


class TestCells(unittest.TestCase):

    def setUp(self):
        self.epigenetic = EpigeneticState()
        self.epigenetic.apply_seed_stage_regulation()

    def test_reflection_cell_active(self):
        cell = ReflectionCell(epigenetic=self.epigenetic)
        self.assertTrue(cell.is_active)

    def test_critic_cell_active(self):
        cell = CriticCell(epigenetic=self.epigenetic)
        self.assertTrue(cell.is_active)

    def test_reflection_cell_process(self):
        cell = ReflectionCell(epigenetic=self.epigenetic)
        result = cell.process({"observation": "Test observation"})
        self.assertEqual(result["status"], "success")
        self.assertIn("reflection", result)


if __name__ == "__main__":
    unittest.main()
