#!/usr/bin/env python3
"""
Bloom Collective - BaseCell (Phase 3)

Abstract base class for all cell-like modular agents.

Every cell:
- Has access to Core Genome and current EpigeneticState
- Implements a common interface
- Can report whether it should be active based on epigenetic regulation
- Is observable and loggable
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

try:
    from epigenetic_state import EpigeneticState
except ImportError:
    EpigeneticState = None


class BaseCell(ABC):
    """
    Abstract base class for all modular cell-like agents.
    """

    def __init__(self, name: str, epigenetic: Optional[EpigeneticState] = None):
        self.name = name
        self.epigenetic = epigenetic
        self._internal_state: Dict[str, Any] = {}

    @property
    def is_active(self) -> bool:
        """
        Returns True if this cell should be active according to current epigenetic state.
        """
        if self.epigenetic is None:
            return True  # Default to active if no epigenetic state provided
        # Convert class name to module key (e.g. ReflectionCell -> reflection)
        module_key = self.name.lower().replace("cell", "").replace("_", "")
        return self.epigenetic.is_module_active(module_key)

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main work method. Subclasses must implement this.
        """
        pass

    def get_state(self) -> Dict[str, Any]:
        """
        Return current internal state. Can be overridden by subclasses.
        """
        return {
            "name": self.name,
            "active": self.is_active,
            "internal_state": self._internal_state.copy(),
        }

    def communicate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Default communication method. Can be overridden.
        """
        return {
            "from": self.name,
            "received": message,
            "response": "acknowledged",
        }

    def log(self, message: str):
        """Simple logging hook. Can be improved later."""
        print(f"[{self.name}] {message}")

    def __repr__(self):
        return f"{self.name}(active={self.is_active})"
