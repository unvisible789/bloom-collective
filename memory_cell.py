#!/usr/bin/env python3
"""
Bloom Collective - MemoryCell (Phase 3 completion)

A cell responsible for storing, retrieving, and versioning experiences and states.
Works closely with EpigeneticState to determine what gets remembered strongly.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class MemoryCell(BaseCell):
    """
    Handles persistence and retrieval of experiences.
    In later versions this can evolve into semantic + episodic memory.
    """

    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="MemoryCell", epigenetic=epigenetic)
        self._internal_state = {
            "stored_items": 0,
            "memories": [],
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "MemoryCell is currently silenced."}

        action = input_data.get("action", "store")

        if action == "store":
            memory = {
                "timestamp": datetime.now().isoformat(),
                "content": input_data.get("content", {}),
                "tags": input_data.get("tags", []),
            }
            self._internal_state["memories"].append(memory)
            self._internal_state["stored_items"] += 1
            self.log(f"Stored new memory (total: {self._internal_state['stored_items']})")
            return {"status": "success", "stored": True}

        elif action == "retrieve":
            # Simple retrieval (can be improved with semantic search later)
            tag = input_data.get("tag")
            results = [m for m in self._internal_state["memories"] if tag in m.get("tags", [])]
            return {"status": "success", "results": results}

        return {"status": "unknown_action"}

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update({
            "stored_items": self._internal_state["stored_items"],
            "memory_count": len(self._internal_state["memories"]),
        })
        return base
