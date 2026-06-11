#!/usr/bin/env python3
"""
Bloom Collective - SimpleOrchestrator (Fixed routing)
"""

from typing import Any, Dict, List, Optional

try:
    from epigenetic_state import EpigeneticState
    from base_cell import BaseCell
except ImportError:
    EpigeneticState = None
    BaseCell = None


class SimpleOrchestrator:
    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        self.epigenetic = epigenetic
        self.cells: Dict[str, BaseCell] = {}
        self.log_entries: List[Dict[str, Any]] = []

    def register_cell(self, cell: BaseCell):
        self.cells[cell.name] = cell

    def get_active_cells(self) -> List[BaseCell]:
        if self.epigenetic is None:
            return list(self.cells.values())
        return [cell for cell in self.cells.values() if cell.is_active]

    def run_task(self, task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        active_cells = self.get_active_cells()

        for cell in active_cells:
            if task_type in getattr(cell, 'supported_tasks', []):
                if hasattr(cell, "process"):
                    try:
                        result = cell.process(input_data)
                        results[cell.name] = result
                    except Exception as e:
                        results[cell.name] = {"status": "error", "message": str(e)}

        return {
            "task": task_type,
            "active_cells_used": [c.name for c in active_cells if task_type in getattr(c, 'supported_tasks', [])],
            "results": results,
        }

    def _log(self, message: str):
        entry = {"timestamp": __import__("datetime").datetime.now().isoformat(), "message": message}
        self.log_entries.append(entry)
        print(f"[Orchestrator] {message}")