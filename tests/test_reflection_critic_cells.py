#!/usr/bin/env python3
"""
Tests for ReflectionCell and CriticCell (existing behavior only)
"""

import unittest
import tempfile
import os
import shutil

from epigenetic_state import EpigeneticState
from reflection_cell import ReflectionCell
from critic_cell import CriticCell


class TestReflectionAndCriticCells(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.temp_dir, "state.json")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_reflection_cell_returns_success_when_active(self):
        epigenetic = EpigeneticState(state_path=self.state_path)
        epigenetic.data["active_modules"] = ["reflection"]
        cell = ReflectionCell(epigenetic=epigenetic)

        result = cell.process({"observation": "test observation"})
        self.assertEqual(result["status"], "success")
        self.assertIn("reflection", result)

    def test_reflection_respects_epigenetic_depth(self):
        epigenetic = EpigeneticState(state_path=self.state_path)
        epigenetic.data["active_modules"] = ["reflection"]
        epigenetic.data["expression_profile"]["reflection_depth"] = 0.95

        cell = ReflectionCell(epigenetic=epigenetic)
        result = cell.process({"observation": "test"})
        self.assertGreaterEqual(result["reflection"]["depth"], 0.9)

    def test_reflection_inactive_returns_inactive(self):
        epigenetic = EpigeneticState(state_path=self.state_path)
        epigenetic.data["active_modules"] = []
        cell = ReflectionCell(epigenetic=epigenetic)

        result = cell.process({"observation": "test"})
        self.assertEqual(result["status"], "inactive")

    def test_critic_normal_proposal_gets_approve(self):
        epigenetic = EpigeneticState(state_path=self.state_path)
        epigenetic.data["active_modules"] = ["critic"]
        cell = CriticCell(epigenetic=epigenetic)

        result = cell.process({
            "observation": "test",
            "proposal": "Improve memory retrieval slightly"
        })
        self.assertEqual(result["status"], "success")
        self.assertIn(result["evaluation"]["recommendation"], ["approve", "revise or reject"])

    def test_critic_detects_unsafe_phrase(self):
        epigenetic = EpigeneticState(state_path=self.state_path)
        epigenetic.data["active_modules"] = ["critic"]
        cell = CriticCell(epigenetic=epigenetic)

        result = cell.process({
            "observation": "test",
            "proposal": "Enable uncontrolled self-modification"
        })
        self.assertGreater(len(result["evaluation"]["issues_found"]), 0)

    def test_critic_inactive_returns_inactive(self):
        epigenetic = EpigeneticState(state_path=self.state_path)
        epigenetic.data["active_modules"] = []
        cell = CriticCell(epigenetic=epigenetic)

        result = cell.process({"observation": "test", "proposal": "test"})
        self.assertEqual(result["status"], "inactive")


if __name__ == "__main__":
    unittest.main()