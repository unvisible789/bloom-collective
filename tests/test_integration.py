#!/usr/bin/env python3
"""
Basic integration tests for the full stack
"""
import unittest

from bloom_seed import BloomSeed


class TestIntegration(unittest.TestCase):

    def test_bloom_seed_runs_without_error(self):
        seed = BloomSeed()
        # Should not raise
        try:
            seed.run_growth_cycle("Integration test observation")
            success = True
        except Exception as e:
            success = False
            print(f"Error: {e}")

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
