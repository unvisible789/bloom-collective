#!/usr/bin/env python3
"""
Bloom Collective - MemoryCell (Fixed)
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import uuid

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class MemoryCell(BaseCell):
    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="MemoryCell", epigenetic=epigenetic)
        self._internal_state = {
            "version": "0.2.0",
            "memories": [],
        }

    @property
    def supported_tasks(self) -> List[str]:
        return ["memory", "store", "retrieve", "get_by_id", "get_all"]

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "MemoryCell is currently silenced."}

        action = input_data.get("action", "store")

        if action == "store":
            memory_id = str(uuid.uuid4())[:8]
            memory = {
                "id": memory_id,
                "version": 1,
                "timestamp": datetime.now().isoformat(),
                "content": input_data.get("content", {}),
                "tags": input_data.get("tags", []),
                "metadata": input_data.get("metadata", {}),
            }
            self._internal_state["memories"].append(memory)
            self.log(f"Stored memory {memory_id}")
            return {"status": "success", "id": memory_id, "stored": True}

        elif action == "retrieve":
            tag = input_data.get("tag")
            query = input_data.get("query", "").lower()
            results = []
            for mem in self._internal_state["memories"]:
                match = False
                if tag and tag in mem.get("tags", []):
                    match = True
                if query and (query in str(mem.get("content", "")).lower() or query in str(mem.get("tags", [])).lower()):
                    match = True
                if match:
                    results.append(mem)
            return {"status": "success", "count": len(results), "results": results}

        elif action == "get_by_id":
            mem_id = input_data.get("id")
            for mem in self._internal_state["memories"]:
                if mem.get("id") == mem_id:
                    return {"status": "success", "memory": mem}
            return {"status": "not_found"}

        elif action == "get_all":
            return {
                "status": "success",
                "count": len(self._internal_state["memories"]),
                "memories": self._internal_state["memories"],
            }

        return {"status": "unknown_action"}

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update({
            "memory_count": len(self._internal_state["memories"]),
            "version": self._internal_state.get("version"),
        })
        return base

    def get_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        return list(reversed(self._internal_state["memories"]))[:limit]
