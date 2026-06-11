#!/usr/bin/env python3
"""
Tests for BaseCell behavior (existing behavior only)
"""

import unittest
import tempfile
import os
import shutil

from epigenetic_state import EpigeneticState
from base_cell import BaseCell
from reflection_cell import ReflectionCell


class TestBaseCell(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.temp_dir, "state.json")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cell_with_no_epigenetic_defaults_active(self):
        # Create a simple subclass for testing
        class DummyCell(BaseCell):
            def process(self, input_data):
                return {"status": "ok"}

        cell = DummyCell(name="DummyCell", epigenetic=None)
        self.assertTrue(cell.is_active)

    def test_supported_tasks_defaults_to_empty(self):
        class DummyCell(BaseCell):
            def process(self, input_data):
                return {"status": "ok"}

        cell = DummyCell(name="DummyCell", epigenetic=None)
        self.assertEqual(cell.supported_tasks, [])

    def test_is_active_respects_epigenetic_state(self):
        epigenetic = EpigeneticState(state_path=self.state_path)
        # Only activate reflection
        epigenetic.data["active_modules"] = ["reflection"]

        cell = ReflectionCell(epigenetic=epigenetic)
        self.assertTrue(cell.is_active)

        # Now deactivate it
        epigenetic.data["active_modules"] = []
        self.assertFalse(cell.is_active)


if __name__ == "__main__":
    unittest.main()