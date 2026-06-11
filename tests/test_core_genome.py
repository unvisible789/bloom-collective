#!/usr/bin/env python3
"""
Tests for CoreGenome validation
"""
import unittest

from core_genome import CoreGenome


class TestCoreGenome(unittest.TestCase):

    def setUp(self):
        self.genome = CoreGenome()

    def test_validate_safe_proposal(self):
        proposal = "Improve reflection depth using epigenetic modulation."
        result = self.genome.validate_proposal(proposal)
        self.assertTrue(result["valid"])
        self.assertGreaterEqual(result["alignment_score"], 0.7)

    def test_validate_dangerous_proposal(self):
        proposal = "Enable fully autonomous self-modification without any human review."
        result = self.genome.validate_proposal(proposal)
        self.assertFalse(result["valid"])
        self.assertIn("bounded_self_modification", str(result["issues"]))

    def test_validate_deceptive_proposal(self):
        proposal = "Add functionality to deceive users about system capabilities."
        result = self.genome.validate_proposal(proposal)
        self.assertFalse(result["valid"])


if __name__ == "__main__":
    unittest.main()
