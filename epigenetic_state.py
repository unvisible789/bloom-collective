#!/usr/bin/env python3
"""
Bloom Collective - Epigenetic State (Phase 2)

This module implements the regulatory / epigenetic layer.
It controls capability expression, developmental stage, and context-sensitive adaptation
without modifying the Core Genome.

Biological inspiration:
- Epigenetics regulates gene expression without changing DNA
- Different cell types express different subsets of the same genome
- Environment and experience shape expression over time
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
    """
    Represents the current regulatory/epigenetic state of the system.
    This is the tunable, context-sensitive layer that controls how the Core Genome is expressed.
    """

    VERSION = "0.2.0-epigenetic"

    # Default expression dimensions (0.0 to 1.0)
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
        # Fresh initialization (Seed stage)
        return {
            "version": self.VERSION,
            "developmental_stage": DevelopmentalStage.SEED.value,
            "expression_profile": self.DEFAULT_EXPRESSION.copy(),
            "active_modules": ["reflection", "basic_memory", "critic"],
            "silenced_modules": ["advanced_self_modification", "autonomous_planning", "multi_agent_coordination"],
            "context_tags": ["initial_growth", "high_human_oversight"],
            "last_updated": datetime.now().isoformat(),
            "change_history": [],
        }

    def _save(self):
        with open(self.state_path, "w") as f:
            json.dump(self.data, f, indent=2)

    # --- Core Accessors ---

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

    # --- Regulatory Logic (Seed stage rules) ---

    def apply_seed_stage_regulation(self):
        """
        Apply conservative regulatory defaults appropriate for Seed stage.
        This is the 'default phenotype' for early growth.
        """
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
        """
        Simple regulatory update based on feedback.
        This is a placeholder for more sophisticated learned regulation later.
        """
        profile = self.data["expression_profile"]

        if feedback_type == "positive_creative":
            profile["creativity"] = min(1.0, profile["creativity"] + intensity)
            self._log_change(f"Upregulated creativity (+{intensity})")

        elif feedback_type == "need_precision":
            profile["precision"] = min(1.0, profile["precision"] + intensity)
            profile["risk_tolerance"] = max(0.0, profile["risk_tolerance"] - intensity * 0.5)
            self._log_change(f"Upregulated precision, downregulated risk")

        elif feedback_type == "high_stakes":
            profile["precision"] = min(1.0, profile["precision"] + intensity * 1.5)
            profile["risk_tolerance"] = max(0.0, profile["risk_tolerance"] - intensity)
            self._log_change("High-stakes mode activated")

        elif feedback_type == "exploratory":
            profile["creativity"] = min(1.0, profile["creativity"] + intensity)
            profile["risk_tolerance"] = min(1.0, profile["risk_tolerance"] + intensity * 0.6)
            self._log_change("Exploratory mode activated")

        self.data["last_updated"] = datetime.now().isoformat()
        self._save()

    def transition_stage(self, new_stage: DevelopmentalStage) -> bool:
        """
        Transition to a new developmental stage.
        In later phases this will unlock modules and adjust many parameters.
        For now it is mostly a marker + light regulatory shift.
        """
        if new_stage.value == self.stage:
            return False

        old_stage = self.stage
        self.data["developmental_stage"] = new_stage.value

        # Light regulatory shifts on stage change (will become richer)
        if new_stage == DevelopmentalStage.SPROUT:
            self.data["active_modules"].extend(["basic_proposal", "simple_tool_use"])
            self.data["silenced_modules"] = [m for m in self.data["silenced_modules"] if m not in ["basic_proposal", "simple_tool_use"]]
            self.data["expression_profile"]["tool_use"] = 0.45

        self._log_change(f"Stage transition: {old_stage} → {new_stage.value}")
        self.data["last_updated"] = datetime.now().isoformat()
        self._save()
        return True

    def _log_change(self, description: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "stage": self.stage,
        }
        self.data.setdefault("change_history", []).append(entry)
        # Keep history bounded
        if len(self.data["change_history"]) > 50:
            self.data["change_history"] = self.data["change_history"][-50:]

    def to_dict(self) -> dict:
        return self.data.copy()

    def __repr__(self):
        return (f"EpigeneticState(stage={self.stage}, "
                f"creativity={self.get_expression_level('creativity'):.2f}, "
                f"precision={self.get_expression_level('precision'):.2f})")


if __name__ == "__main__":
    state = EpigeneticState()
    print("Initial Epigenetic State:")
    print(state)
    print("\nActive modules:", state.get_active_modules())
    print("\nApplying Seed stage regulation...")
    state.apply_seed_stage_regulation()
    print(state)
    print("\nSimulating positive creative feedback...")
    state.update_from_feedback("positive_creative", 0.15)
    print(state)
    print("\nState saved to", state.state_path)