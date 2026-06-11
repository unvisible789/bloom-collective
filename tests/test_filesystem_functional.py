#!/usr/bin/env python3
"""
Functional tests for FileSystemCell (existing behavior)
"""

import unittest
import tempfile
import os
import shutil

from epigenetic_state import EpigeneticState
from file_system_cell import FileSystemCell


class TestFileSystemFunctional(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = os.path.join(self.temp_dir, "base")
        os.makedirs(self.base_path)

        self.epigenetic = EpigeneticState(state_path=os.path.join(self.temp_dir, "state.json"))
        if "filesystem" not in self.epigenetic.data.get("active_modules", []):
            self.epigenetic.data["active_modules"].append("filesystem")

        self.cell = FileSystemCell(epigenetic=self.epigenetic, base_path=self.base_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_write_and_read_file(self):
        result = self.cell.process({
            "action": "write",
            "filename": "test.txt",
            "content": "hello world"
        })
        self.assertEqual(result["status"], "success")

        read_result = self.cell.process({
            "action": "read",
            "filename": "test.txt"
        })
        self.assertEqual(read_result["status"], "success")
        self.assertIn("hello world", read_result["content"])

    def test_list_directory(self):
        self.cell.process({"action": "write", "filename": "a.txt", "content": ""})
        result = self.cell.process({"action": "list", "path": "."})
        self.assertEqual(result["status"], "success")
        self.assertIn("a.txt", result["items"])

    def test_create_directory(self):
        result = self.cell.process({"action": "mkdir", "dirname": "subdir"})
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.isdir(os.path.join(self.base_path, "subdir")))


if __name__ == "__main__":
    unittest.main()