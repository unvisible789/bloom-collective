#!/usr/bin/env python3
"""
Bloom Collective - FileSystemCell (Expanded)

Now supports more file system operations:
- list, read, write
- create directory
- delete file/directory

All operations are logged.
"""
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class FileSystemCell(BaseCell):
    def __init__(self, epigenetic: Optional[EpigeneticState] = None, base_path: str = "."):
        super().__init__(name="FileSystemCell", epigenetic=epigenetic)
        self.base_path = Path(base_path).resolve()
        self._internal_state = {
            "operations_count": 0,
            "last_operation": None,
        }

    def _resolve(self, path: str) -> Path:
        return (self.base_path / path).resolve()

    def list_directory(self, path: str = ".") -> Dict[str, Any]:
        target = self._resolve(path)
        try:
            items = os.listdir(target)
            self._log_operation("list", str(target))
            return {"status": "success", "path": str(target), "items": items}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_file(self, filename: str) -> Dict[str, Any]:
        target = self._resolve(filename)
        try:
            with open(target, "r", encoding="utf-8") as f:
                content = f.read()
            self._log_operation("read", str(target))
            return {"status": "success", "path": str(target), "content": content[:3000]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def write_file(self, filename: str, content: str) -> Dict[str, Any]:
        target = self._resolve(filename)
        try:
            with open(target, "w", encoding="utf-8") as f:
                f.write(content)
            self._log_operation("write", str(target))
            return {"status": "success", "path": str(target), "bytes_written": len(content)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_directory(self, dirname: str) -> Dict[str, Any]:
        target = self._resolve(dirname)
        try:
            target.mkdir(parents=True, exist_ok=True)
            self._log_operation("mkdir", str(target))
            return {"status": "success", "path": str(target)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_path(self, path: str) -> Dict[str, Any]:
        target = self._resolve(path)
        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            self._log_operation("delete", str(target))
            return {"status": "success", "path": str(target)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _log_operation(self, operation: str, path: str):
        self._internal_state["operations_count"] += 1
        self._internal_state["last_operation"] = {
            "operation": operation,
            "path": path,
            "timestamp": datetime.now().isoformat()
        }
        self.log(f"{operation.upper()}: {path}")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "FileSystemCell is currently silenced."}

        action = input_data.get("action", "list")

        if action == "list":
            return self.list_directory(input_data.get("path", "."))
        elif action == "read":
            return self.read_file(input_data.get("filename", ""))
        elif action == "write":
            return self.write_file(input_data.get("filename", ""), input_data.get("content", ""))
        elif action == "mkdir":
            return self.create_directory(input_data.get("dirname", ""))
        elif action == "delete":
            return self.delete_path(input_data.get("path", ""))
        else:
            return {"status": "unknown_action", "available": ["list", "read", "write", "mkdir", "delete"]}

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
