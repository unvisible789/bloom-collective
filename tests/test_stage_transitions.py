#!/usr/bin/env python3
"""
Tests for developmental stage transition logic
"""
import unittest

from epigenetic_state import EpigeneticState, DevelopmentalStage


class TestStageTransitions(unittest.TestCase):

    def setUp(self):
        self.state = EpigeneticState()
        self.state.apply_seed_stage_regulation()

    def test_initial_stage_is_seed(self):
        self.assertEqual(self.state.stage, DevelopmentalStage.SEED.value)

    def test_can_transition_from_seed_to_sprout(self):
        self.assertTrue(self.state.can_transition_to(DevelopmentalStage.SPROUT))

    def test_cannot_skip_stages(self):
        # From Seed, cannot jump directly to Sapling
        self.assertFalse(self.state.can_transition_to(DevelopmentalStage.SAPLING))

    def test_successful_transition_updates_stage(self):
        success = self.state.transition_to(DevelopmentalStage.SPROUT)
        self.assertTrue(success)
        self.assertEqual(self.state.stage, DevelopmentalStage.SPROUT.value)

    def test_expression_changes_on_transition(self):
        initial_tool_use = self.state.get_expression_level("tool_use")
        self.state.transition_to(DevelopmentalStage.SPROUT)
        new_tool_use = self.state.get_expression_level("tool_use")
        self.assertNotEqual(initial_tool_use, new_tool_use)


if __name__ == "__main__":
    unittest.main()
