#!/usr/bin/env python3
"""
Expanded tests for MemoryCell existing behavior
"""

import unittest
import tempfile
import os
import shutil

from epigenetic_state import EpigeneticState
from memory_cell import MemoryCell


class TestMemoryExpanded(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.temp_dir, "state.json")
        self.epigenetic = EpigeneticState(state_path=self.state_path)
        if "memory" not in self.epigenetic.data.get("active_modules", []):
            self.epigenetic.data["active_modules"].append("memory")
        self.memory = MemoryCell(epigenetic=self.epigenetic)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_store_with_tags_and_metadata(self):
        result = self.memory.process({
            "action": "store",
            "content": {"key": "value"},
            "tags": ["important", "test"],
            "metadata": {"source": "unit_test"}
        })
        self.assertEqual(result["status"], "success")
        mem_id = result["id"]

        retrieved = self.memory.process({"action": "get_by_id", "id": mem_id})
        self.assertEqual(retrieved["memory"]["tags"], ["important", "test"])
        self.assertEqual(retrieved["memory"]["metadata"]["source"], "unit_test")

    def test_retrieve_by_tag(self):
        self.memory.process({"action": "store", "content": {}, "tags": ["alpha"]})
        self.memory.process({"action": "store", "content": {}, "tags": ["beta"]})

        result = self.memory.process({"action": "retrieve", "tag": "alpha"})
        self.assertGreaterEqual(result["count"], 1)

    def test_retrieve_by_query(self):
        self.memory.process({"action": "store", "content": {"note": "important finding"}})
        result = self.memory.process({"action": "retrieve", "query": "important"})
        self.assertGreaterEqual(result["count"], 1)

    def test_get_by_id(self):
        store_result = self.memory.process({"action": "store", "content": {"id_test": True}})
        mem_id = store_result["id"]

        result = self.memory.process({"action": "get_by_id", "id": mem_id})
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["memory"]["content"]["id_test"])

    def test_get_recent_returns_newest_first(self):
        for i in range(3):
            self.memory.process({"action": "store", "content": {"num": i}})

        recent = self.memory.get_recent(2)
        self.assertEqual(len(recent), 2)
        # Newest should have higher num if we stored in order
        self.assertGreaterEqual(recent[0]["content"]["num"], recent[1]["content"]["num"])


if __name__ == "__main__":
    unittest.main()