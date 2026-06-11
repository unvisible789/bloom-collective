#!/usr/bin/env python3
"""
Bloom Collective - BaseCell (with supported_tasks)
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List


class BaseCell(ABC):
    def __init__(self, name: str, epigenetic: Optional["EpigeneticState"] = None):
        self.name = name
        self.epigenetic = epigenetic
        self._internal_state: Dict[str, Any] = {}

    @property
    def supported_tasks(self) -> List[str]:
        return []

    @property
    def is_active(self) -> bool:
        if self.epigenetic is None:
            return True
        module_key = self.name.lower().replace("cell", "").replace("_", "")
        return self.epigenetic.is_module_active(module_key)

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def get_state(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "active": self.is_active,
            "internal_state": self._internal_state.copy(),
        }

    def communicate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "from": self.name,
            "received": message,
            "response": "acknowledged",
        }

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def __repr__(self):
        return f"{self.name}(active={self.is_active})"