#!/usr/bin/env python3
"""
Bloom Collective - Initial Seed (Updated with Epigenetic Integration)

A minimal self-reflecting, self-improving agent skeleton.
Now integrated with the EpigeneticState regulatory layer (Phase 2).

This version demonstrates the first connection between:
- Core reflection / growth cycle
- Epigenetic expression profile and developmental stage

The system now "knows" its current regulatory state during reflection.
"""

import json
import os
from datetime import datetime
from pathlib import Path

try:
    from epigenetic_state import EpigeneticState, DevelopmentalStage
except ImportError:
    # Fallback for standalone testing
    EpigeneticState = None
    DevelopmentalStage = None


class BloomSeed:
    def __init__(self, memory_path: str = "memory/seed_state.json"):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

        # Epigenetic / Regulatory Layer integration (Phase 2)
        if EpigeneticState is not None:
            self.epigenetic = EpigeneticState()
            # Ensure Seed stage defaults are applied on first run
            if self.epigenetic.stage == DevelopmentalStage.SEED.value:
                self.epigenetic.apply_seed_stage_regulation()
        else:
            self.epigenetic = None

    def _load_state(self):
        if self.memory_path.exists():
            with open(self.memory_path, "r") as f:
                return json.load(f)
        return {
            "version": "0.2.0-integrated",
            "created": datetime.now().isoformat(),
            "growth_cycles": 0,
            "reflections": [],
            "principles": [
                "Seek coherence and alignment (E.A.T. inspired)",
                "Prefer simple, elegant improvements over complex ones",
                "Maintain human oversight for all structural changes",
                "Log everything meaningful for future reflection"
            ]
        }

    def _save_state(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.state, f, indent=2)

    def reflect(self):
        """Basic self-reflection, now informed by current epigenetic state."""
        epigenetic_info = {}
        if self.epigenetic:
            epigenetic_info = {
                "stage": self.epigenetic.stage,
                "creativity": round(self.epigenetic.get_expression_level("creativity"), 2),
                "precision": round(self.epigenetic.get_expression_level("precision"), 2),
                "risk_tolerance": round(self.epigenetic.get_expression_level("risk_tolerance"), 2),
                "active_modules": self.epigenetic.get_active_modules(),
            }

        reflection = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.state["growth_cycles"],
            "observation": "This is the initial seed with epigenetic integration. The system now has access to its regulatory state.",
            "epigenetic_context": epigenetic_info,
            "strengths": [
                "Persistent memory foundation",
                "Clear principles",
                "Epigenetic regulatory layer active",
                "Simple and reviewable"
            ],
            "improvement_areas": [
                "Deepen integration between reflection and epigenetic expression",
                "Add actual code modification capability gated by epigenetic state",
                "Better evaluation of proposed changes using current expression profile",
                "Integration with tools (GitHub, memory systems)"
            ]
        }

        self.state["reflections"].append(reflection)
        self.state["growth_cycles"] += 1
        self._save_state()

        # Also persist epigenetic state
        if self.epigenetic:
            # Already saved inside epigenetic methods when changed
            pass

        return reflection

    def propose_improvement(self, focus_area: str):
        """Propose a concrete improvement, lightly colored by current epigenetic expression."""
        base_proposals = {
            "memory": "Enhance memory system to support versioning of past states and semantic search.",
            "reflection": "Add structured scoring for reflections using epigenetic expression levels.",
            "self_modification": "Implement safe, review-gated code rewriting using AST or diff-based approach.",
            "tool_use": "Add ability to interact with GitHub API for logging growth or fetching context.",
        }

        proposal = base_proposals.get(focus_area, "No specific proposal yet for this focus area.")

        # Light epigenetic influence on proposal tone
        if self.epigenetic:
            creativity = self.epigenetic.get_expression_level("creativity")
            if creativity > 0.6:
                proposal += " (Creative/high-expression angle: explore novel combinations and analogies.)"
            elif creativity < 0.4:
                proposal += " (Precision-focused: keep changes minimal, well-scoped, and easily reviewable.)"

        return proposal

    def run_growth_cycle(self):
        """Execute one full growth cycle with epigenetic awareness."""
        print("=== Bloom Seed Growth Cycle (Epigenetically Aware) ===")

        if self.epigenetic:
            print(f"Current Stage: {self.epigenetic.stage}")
            print(f"Expression Profile: creativity={self.epigenetic.get_expression_level('creativity'):.2f}, "
                  f"precision={self.epigenetic.get_expression_level('precision'):.2f}, "
                  f"risk={self.epigenetic.get_expression_level('risk_tolerance'):.2f}")
            print(f"Active Modules: {self.epigenetic.get_active_modules()}")
            print()

        reflection = self.reflect()
        print(f"Cycle {reflection['cycle']}: {reflection['observation']}")

        if reflection.get("epigenetic_context"):
            ctx = reflection["epigenetic_context"]
            print(f"Epigenetic Context → Stage: {ctx['stage']}, Creativity: {ctx['creativity']}, Precision: {ctx['precision']}")

        print("\nKey improvement areas identified:")
        for area in reflection["improvement_areas"]:
            print(f"  - {area}")
            # Use first word as rough focus key
            focus = area.split()[0].lower().replace(":", "").replace(",", "")
            proposal = self.propose_improvement(focus)
            print(f"    Proposal: {proposal}")

        print("\nState saved. Ready for next cycle or human/AI review.\n")
        return reflection


if __name__ == "__main__":
    seed = BloomSeed()
    seed.run_growth_cycle()