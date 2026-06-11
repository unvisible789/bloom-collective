#!/usr/bin/env python3
"""
Bloom Collective - Simple Orchestrator (Phase 3/4)

Coordinates active cells based on current EpigeneticState.
This is a lightweight central coordinator for early phases.
"""
from typing import Any, Dict, List, Optional

try:
    from epigenetic_state import EpigeneticState
    from base_cell import BaseCell
except ImportError:
    EpigeneticState = None
    BaseCell = None


class SimpleOrchestrator:
    """
    Simple orchestrator that:
    - Holds references to Core Genome and EpigeneticState
    - Determines which cells are currently active
    - Routes tasks to active cells
    - Collects and logs results
    """

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
        """
        Route a task to appropriate active cells.
        """
        results = {}
        active_cells = self.get_active_cells()

        self._log(f"Running task '{task_type}' with {len(active_cells)} active cells")

        for cell in active_cells:
            if task_type == "reflect" and "Reflection" in cell.name:
                result = cell.process(input_data)
                results[cell.name] = result
            elif task_type == "critique" and "Critic" in cell.name:
                result = cell.process(input_data)
                results[cell.name] = result
            else:
                # Default: let cell decide if it can handle it
                if hasattr(cell, "process"):
                    result = cell.process(input_data)
                    results[cell.name] = result

        return {
            "task": task_type,
            "active_cells_used": [c.name for c in active_cells],
            "results": results,
        }

    def _log(self, message: str):
        entry = {"timestamp": __import__("datetime").datetime.now().isoformat(), "message": message}
        self.log_entries.append(entry)
        print(f"[Orchestrator] {message}")
