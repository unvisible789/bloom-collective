#!/usr/bin/env python3
"""
Tests for improved MemoryCell features
"""
import unittest

from epigenetic_state import EpigeneticState

from memory_cell import MemoryCell


class TestMemoryImproved(unittest.TestCase):

    def setUp(self):
        self.epigenetic = EpigeneticState()
        self.memory = MemoryCell(epigenetic=self.epigenetic)

    def test_store_and_retrieve_by_id(self):
        result = self.memory.process({
            "action": "store",
            "content": {"key": "value"},
            "tags": ["test"]
        })
        mem_id = result["id"]

        retrieved = self.memory.process({"action": "get_by_id", "id": mem_id})
        self.assertEqual(retrieved["status"], "success")
        self.assertEqual(retrieved["memory"]["content"]["key"], "value")

    def test_retrieve_by_tag(self):
        self.memory.process({"action": "store", "content": {}, "tags": ["alpha"]})
        self.memory.process({"action": "store", "content": {}, "tags": ["beta"]})

        result = self.memory.process({"action": "retrieve", "tag": "alpha"})
        self.assertGreaterEqual(result["count"], 1)

    def test_get_recent(self):
        for i in range(5):
            self.memory.process({"action": "store", "content": {"num": i}})

        recent = self.memory.get_recent(3)
        self.assertEqual(len(recent), 3)


if __name__ == "__main__":
    unittest.main()
