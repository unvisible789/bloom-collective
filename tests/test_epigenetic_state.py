#!/usr/bin/env python3
"""
Tests for EpigeneticState
"""
import unittest
import tempfile
import os

from epigenetic_state import EpigeneticState, DevelopmentalStage


class TestEpigeneticState(unittest.TestCase):

    def setUp(self):
        # Use a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.temp_dir, "test_state.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        state = EpigeneticState(state_path=self.state_path)
        self.assertEqual(state.stage, DevelopmentalStage.SEED.value)
        self.assertIn("creativity", state.expression)

    def test_apply_seed_regulation(self):
        state = EpigeneticState(state_path=self.state_path)
        state.apply_seed_stage_regulation()
        self.assertLessEqual(state.get_expression_level("risk_tolerance"), 0.3)

    def test_update_from_feedback(self):
        state = EpigeneticState(state_path=self.state_path)
        initial_creativity = state.get_expression_level("creativity")
        state.update_from_feedback("positive_creative", 0.2)
        new_creativity = state.get_expression_level("creativity")
        self.assertGreater(new_creativity, initial_creativity)

    def test_is_module_active(self):
        state = EpigeneticState(state_path=self.state_path)
        # In Seed stage, basic modules should be active
        self.assertTrue(state.is_module_active("reflection"))


if __name__ == "__main__":
    unittest.main()
