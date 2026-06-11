#!/usr/bin/env python3
"""
Bloom Collective - Epigenetic State (Fixed for MemoryCell activation)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from enum import Enum


class DevelopmentalStage(str, Enum):
    SEED = "seed"
    SPROUT = "sprout"
    SAPLING = "sapling"
    BLOOM = "bloom"
    ELDER = "elder"


class EpigeneticState:
    VERSION = "0.3.0-epigenetic"

    DEFAULT_EXPRESSION = {
        "creativity": 0.45,
        "precision": 0.75,
        "risk_tolerance": 0.25,
        "reflection_depth": 0.65,
        "tool_use": 0.35,
        "modularity": 0.40,
    }

    def __init__(self, state_path: str = "memory/epigenetic_state.json"):
        self.state_path = Path(state_path)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load_or_initialize()

    def _load_or_initialize(self) -> dict:
        if self.state_path.exists():
            with open(self.state_path, "r") as f:
                return json.load(f)
        return {
            "version": self.VERSION,
            "developmental_stage": DevelopmentalStage.SEED.value,
            "expression_profile": self.DEFAULT_EXPRESSION.copy(),
            "active_modules": ["reflection", "memory", "critic"],  # Fixed
            "silenced_modules": ["advanced_self_modification", "autonomous_planning", "multi_agent_coordination"],
            "context_tags": ["initial_growth", "high_human_oversight"],
            "last_updated": datetime.now().isoformat(),
            "change_history": [],
        }

    def _save(self):
        with open(self.state_path, "w") as f:
            json.dump(self.data, f, indent=2)

    @property
    def stage(self) -> str:
        return self.data["developmental_stage"]

    @property
    def expression(self) -> dict:
        return self.data["expression_profile"]

    def get_expression_level(self, dimension: str) -> float:
        return self.expression.get(dimension, 0.5)

    def is_module_active(self, module: str) -> bool:
        return module in self.data.get("active_modules", [])

    def get_active_modules(self) -> list:
        return self.data.get("active_modules", []).copy()

    def can_transition_to(self, new_stage: DevelopmentalStage) -> bool:
        current = DevelopmentalStage(self.stage)
        order = list(DevelopmentalStage)
        current_index = order.index(current)
        new_index = order.index(new_stage)
        return new_index == current_index + 1

    def transition_to(self, new_stage: DevelopmentalStage) -> bool:
        if not self.can_transition_to(new_stage):
            self._log_change(f"Blocked transition attempt: {self.stage} → {new_stage.value}")
            return False

        old_stage = self.stage
        self.data["developmental_stage"] = new_stage.value

        if new_stage == DevelopmentalStage.SPROUT:
            self.data["expression_profile"]["tool_use"] = 0.45
            self.data["expression_profile"]["modularity"] = 0.50
            if "basic_proposal" not in self.data["active_modules"]:
                self.data["active_modules"].extend(["basic_proposal", "simple_tool_use"])

        elif new_stage == DevelopmentalStage.SAPLING:
            self.data["expression_profile"]["creativity"] = 0.55
            self.data["expression_profile"]["reflection_depth"] = 0.75
            if "advanced_reflection" not in self.data["active_modules"]:
                self.data["active_modules"].extend(["advanced_reflection", "memory_retrieval"])

        elif new_stage == DevelopmentalStage.BLOOM:
            self.data["expression_profile"]["creativity"] = 0.65
            self.data["expression_profile"]["modularity"] = 0.70
            self.data["risk_tolerance"] = 0.40

        self._log_change(f"Stage transition: {old_stage} → {new_stage.value}")
        self.data["last_updated"] = datetime.now().isoformat()
        self._save()
        return True

    def apply_seed_stage_regulation(self):
        self.data["expression_profile"].update({
            "creativity": 0.40,
            "precision": 0.80,
            "risk_tolerance": 0.20,
            "reflection_depth": 0.70,
            "tool_use": 0.30,
            "modularity": 0.35,
        })
        self.data["context_tags"] = ["initial_growth", "high_human_oversight", "conservative"]
        self._log_change("Applied Seed stage regulatory defaults")

    def update_from_feedback(self, feedback_type: str, intensity: float = 0.1):
        profile = self.data["expression_profile"]

        if feedback_type == "positive_creative":
            profile["creativity"] = min(1.0, profile["creativity"] + intensity)

        elif feedback_type == "need_precision":
            profile["precision"] = min(1.0, profile["precision"] + intensity)
            profile["risk_tolerance"] = max(0.0, profile["risk_tolerance"] - intensity * 0.5)

        elif feedback_type == "high_stakes":
            profile["precision"] = min(1.0, profile["precision"] + intensity * 1.5)
            profile["risk_tolerance"] = max(0.0, profile["risk_tolerance"] - intensity)

        elif feedback_type == "exploratory":
            profile["creativity"] = min(1.0, profile["creativity"] + intensity)
            profile["risk_tolerance"] = min(1.0, profile["risk_tolerance"] + intensity * 0.6)

        self.data["last_updated"] = datetime.now().isoformat()
        self._save()

    def _log_change(self, description: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "stage": self.stage,
        }
        self.data.setdefault("change_history", []).append(entry)
        if len(self.data["change_history"]) > 50:
            self.data["change_history"] = self.data["change_history"][-50:]

    def to_dict(self) -> dict:
        return self.data.copy()

    def __repr__(self):
        return (f"EpigeneticState(stage={self.stage}, "
                f"creativity={self.get_expression_level('creativity'):.2f})")