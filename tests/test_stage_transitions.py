#!/usr/bin/env python3
"""
Tests for developmental stage transition logic
"""
import unittest
import tempfile
import os

from epigenetic_state import EpigeneticState, DevelopmentalStage


class TestStageTransitions(unittest.TestCase):

    def setUp(self):
        # Use temporary file for test isolation - prevents mutating shared runtime state
        self.test_dir = tempfile.mkdtemp()
        self.test_path = os.path.join(self.test_dir, "test_epigenetic_state.json")
        self.state = EpigeneticState(self.test_path)
        self.state.apply_seed_stage_regulation()

    def tearDown(self):
        # Clean up temporary test state file and directory
        if os.path.exists(self.test_path):
            os.unlink(self.test_path)
        if os.path.exists(self.test_dir):
            try:
                os.rmdir(self.test_dir)
            except OSError:
                pass  # Directory may not be empty in some cases

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

    # ==================== New tests for explicit transition decisions with reasons ====================

    def test_transition_decision_allowed_next_stage(self):
        """Test that transition_decision returns allowed=True with reason for valid next stage"""
        decision = self.state.transition_decision(DevelopmentalStage.SPROUT)
        self.assertTrue(decision["allowed"])
        self.assertIn("Valid forward transition", decision["reason"])
        self.assertEqual(decision["current_stage"], "seed")
        self.assertEqual(decision["requested_stage"], "sprout")

    def test_transition_decision_skipped_stage_blocked(self):
        """Test that skipping stages is blocked with clear reason"""
        decision = self.state.transition_decision(DevelopmentalStage.SAPLING)
        self.assertFalse(decision["allowed"])
        self.assertIn("skip blocked", decision["reason"].lower())
        self.assertEqual(decision["current_stage"], "seed")
        self.assertEqual(decision["requested_stage"], "sapling")

    def test_transition_decision_same_stage_blocked(self):
        """Test that same-stage transition is blocked with reason"""
        decision = self.state.transition_decision(DevelopmentalStage.SEED)
        self.assertFalse(decision["allowed"])
        self.assertIn("Same stage", decision["reason"])

    def test_transition_decision_regression_blocked(self):
        """Test that regression (going back) is blocked with reason"""
        # Advance to sprout first
        self.state.transition_to(DevelopmentalStage.SPROUT)
        decision = self.state.transition_decision(DevelopmentalStage.SEED)
        self.assertFalse(decision["allowed"])
        self.assertIn("Regression blocked", decision["reason"])


if __name__ == "__main__":
    unittest.main()
