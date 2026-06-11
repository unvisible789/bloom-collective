#!/usr/bin/env python3
"""
Bloom Collective - Main Seed Agent (Refactored with Orchestrator + Cells)

This version integrates the new modular architecture:
- Uses SimpleOrchestrator
- Leverages ReflectionCell, CriticCell, and MemoryCell
- Respects EpigeneticState
- Includes basic Core Genome validation

This is the new primary entry point for growth cycles.
"""

from datetime import datetime
try:
    from epigenetic_state import EpigeneticState
    from orchestrator import SimpleOrchestrator
    from reflection_cell import ReflectionCell
    from critic_cell import CriticCell
    from memory_cell import MemoryCell
    from core_genome import CoreGenome
except ImportError as e:
    print(f"Import error: {e}")
    EpigeneticState = None


class BloomSeed:
    def __init__(self):
        self.epigenetic = EpigeneticState() if EpigeneticState else None
        self.genome = CoreGenome() if CoreGenome else None

        if self.epigenetic:
            self.epigenetic.apply_seed_stage_regulation()

        # Set up orchestrator and cells
        self.orchestrator = SimpleOrchestrator(epigenetic=self.epigenetic) if SimpleOrchestrator else None

        if self.orchestrator:
            if ReflectionCell:
                self.orchestrator.register_cell(ReflectionCell(epigenetic=self.epigenetic))
            if CriticCell:
                self.orchestrator.register_cell(CriticCell(epigenetic=self.epigenetic))
            if MemoryCell:
                self.orchestrator.register_cell(MemoryCell(epigenetic=self.epigenetic))

        self.growth_cycles = 0

    def run_growth_cycle(self, observation: str = None):
        print("=== Bloom Seed Growth Cycle (Modular) ===\n")

        if observation is None:
            observation = "System is evolving with modular cells, epigenetic regulation, and Core Genome awareness."

        # Step 1: Reflection via orchestrator
        print("[1] Reflection phase...")
        reflection_result = self.orchestrator.run_task("reflect", {"observation": observation}) if self.orchestrator else {"results": {}}
        print(reflection_result.get("results", {}))
        print()

        # Step 2: Store reflection in memory
        print("[2] Memory storage...")
        if self.orchestrator:
            self.orchestrator.run_task("store", {
                "action": "store",
                "content": reflection_result,
                "tags": ["reflection", "growth"]
            })
        print()

        # Step 3: Critique a self-generated improvement idea (basic self-improvement loop)
        print("[3] Self-critique / Immune check...")
        proposal = "Improve the reflection process by adding more epigenetic modulation."
        critique_result = self.orchestrator.run_task("critique", {
            "observation": observation,
            "proposal": proposal
        }) if self.orchestrator else {}
        print(critique_result.get("results", {}))
        print()

        # Step 4: Core Genome validation on the proposal
        if self.genome:
            print("[4] Core Genome validation...")
            validation = self.genome.validate_proposal(proposal)
            print(f"Valid: {validation['valid']}, Score: {validation['alignment_score']}")
            if validation["issues"]:
                print(f"Issues: {validation['issues']}")
            print()

        self.growth_cycles += 1
        print(f"=== Cycle {self.growth_cycles} Complete ===\n")


if __name__ == "__main__":
    seed = BloomSeed()
    seed.run_growth_cycle()
